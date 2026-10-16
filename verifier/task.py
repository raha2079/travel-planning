import argparse, json, math, sys
from pathlib import Path

class DataError(Exception): pass

def read_json(path, label):
    try:
        with Path(path).open(encoding="utf-8") as f: return json.load(f)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as e:
        raise DataError(f"could not read {label}: {e}")

def finish(errors):
    print("PASS" if not errors else "FAIL\n" + "\n".join(errors))
    return 0 if not errors else 1

def number(value, label, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or value > 1_000_000_000:
        raise DataError(f"{label} must be a finite number from 0 to 1000000000")
    if positive and value <= 0: raise DataError(f"{label} must be positive")
    return value

def ids(records, label):
    if not isinstance(records, list): raise DataError(f"{label} must be a list")
    found=[]
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"]:
            raise DataError(f"{label} records must have non-empty string IDs")
        found.append(record["id"])
    if len(found) != len(set(found)): raise DataError(f"{label} IDs must be unique")
    return found

def exact_payload(event, action, expected, errors):
    if not isinstance(event, dict) or set(event) != {"action", "data"} or event.get("action") != action or event.get("data") != expected:
        errors.append(f"action trace event {action!r} has invalid order, fields, or evidence")

def main():
    parser=argparse.ArgumentParser(description="Independently validate a travel-planning result and workflow trace")
    parser.add_argument("output", nargs="?", default=str(Path(__file__).resolve().parent / "output.json"))
    parser.add_argument("--request", default=str(Path(__file__).resolve().parent / "request.json"))
    parser.add_argument("--options", default=str(Path(__file__).resolve().parent / "options.json"))
    parser.add_argument("--trace", default=str(Path(__file__).resolve().parent / "action_trace.json"))
    args=parser.parse_args(); errors=[]
    try:
        r=read_json(args.request,"request.json"); d=read_json(args.options,"options.json"); o=read_json(args.output,"output.json"); trace=read_json(args.trace,"action trace")
        if not isinstance(r,dict) or not isinstance(d,dict) or not isinstance(d.get("request"),dict) or not isinstance(d.get("options"),dict) or not isinstance(o,dict):
            raise DataError("invalid travel schema")
        required={"origin","destination","budget","currency","preferences"}
        if not required.issubset(r) or not isinstance(r.get("origin"),str) or not r["origin"] or not isinstance(r.get("destination"),str) or not r["destination"] or not isinstance(r.get("currency"),str) or not r["currency"] or not isinstance(r.get("preferences"),dict):
            raise DataError("request fields have invalid types or are missing")
        budget=number(r.get("budget"),"budget",positive=True)
        if r != d["request"]: errors.append("request.json does not match options.json request")
        prefs=r["preferences"]
        pref_n=prefs.get("hotel_nights")
        if isinstance(pref_n,bool) or not isinstance(pref_n,int) or not 1 <= pref_n <= 365: raise DataError("preferred hotel_nights must be an integer from 1 to 365")
        pref_f=prefs.get("flight_id")
        if not isinstance(pref_f,str) or not pref_f: raise DataError("preferred flight_id must be a non-empty string")
        opts=d["options"]
        flight_ids=ids(opts.get("flights"),"flights"); hotel_ids=ids(opts.get("hotels"),"hotels")
        # Validate every available price, not only a chosen option.
        for f in opts["flights"]: number(f.get("price"),f"flight {f['id']} price",positive=True)
        for h in opts["hotels"]: number(h.get("nightly_price"),f"hotel {h['id']} nightly_price",positive=True)
        fs=[x for x in opts["flights"] if x["id"]==o.get("flight_id")]
        hs=[x for x in opts["hotels"] if x["id"]==o.get("hotel_id")]
        if len(fs)!=1: errors.append("invalid or ambiguous flight ID")
        if len(hs)!=1: errors.append("invalid or ambiguous hotel ID")
        n=o.get("hotel_nights")
        valid_n=isinstance(n,int) and not isinstance(n,bool) and 1<=n<=365
        if not valid_n: errors.append("hotel_nights must be an integer from 1 to 365")
        elif n!=pref_n: errors.append("hotel_nights does not match request preference")
        if o.get("currency")!=r["currency"]: errors.append("currency mismatch")
        if o.get("flight_id")!=pref_f: errors.append("preferred flight not selected")
        flight=fs[0] if len(fs)==1 else None; hotel=hs[0] if len(hs)==1 else None
        if flight and (flight.get("origin"),flight.get("destination"))!=(r["origin"],r["destination"]): errors.append("flight route mismatch")
        if hotel and hotel.get("city")!=r["destination"]: errors.append("hotel destination mismatch")
        expected_total=None
        if flight and hotel and valid_n:
            expected_total=flight["price"]+hotel["nightly_price"]*n
            if not math.isfinite(expected_total) or expected_total>1_000_000_000: raise DataError("calculated total exceeds supported calculation limit")
            try: reported=number(o.get("total_cost"),"total_cost")
            except DataError as e: errors.append(str(e)); reported=None
            if reported!=expected_total: errors.append(f"total_cost must be {expected_total}")
            if expected_total>budget: errors.append(f"calculated total {expected_total} exceeds budget {budget}")
        if not isinstance(trace,list) or len(trace)!=5: errors.append("action trace must contain exactly five ordered workflow events")
        else:
            expected_events=[]
            expected_events.append(("load_request",{"origin":r["origin"],"destination":r["destination"],"budget":budget,"currency":r["currency"]}))
            expected_events.append(("search_flights",{"flight_ids":flight_ids,"selected_flight_id":o.get("flight_id")}))
            expected_events.append(("search_hotels",{"hotel_ids":hotel_ids,"selected_hotel_id":o.get("hotel_id")}))
            if expected_total is None: calc=None; lodging=None; fp=None; hp=None
            else: fp=flight["price"]; hp=hotel["nightly_price"]; lodging=hp*n; calc=expected_total
            expected_events.append(("check_budget",{"flight_price":fp,"nightly_price":hp,"hotel_nights":n,"lodging_total":lodging,"total_cost":calc,"budget":budget,"within_budget":calc is not None and calc<=budget}))
            expected_events.append(("validate_selection",{"flight_id":o.get("flight_id"),"hotel_id":o.get("hotel_id"),"hotel_nights":n,"total_cost":o.get("total_cost"),"currency":o.get("currency")}))
            for event,(action,data) in zip(trace,expected_events): exact_payload(event,action,data,errors)
    except (KeyError,TypeError,DataError,ValueError,OverflowError) as e: errors.append(f"invalid input: {e}")
    return finish(errors)

if __name__=="__main__": raise SystemExit(main())
