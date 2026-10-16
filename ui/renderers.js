/**
 * UI renderers for travel planning plugin results
 */

export function renderResult(result) {
  if (!result) return '';

  return `
    <div class="travel-result">
      <h3>Travel Booking Summary</h3>
      <div class="booking-details">
        <div class="detail-row">
          <span class="label">Flight ID:</span>
          <span class="value">${result.flight_id || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="label">Hotel ID:</span>
          <span class="value">${result.hotel_id || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="label">Hotel Nights:</span>
          <span class="value">${result.hotel_nights || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="label">Total Cost:</span>
          <span class="value">${result.currency || ''} ${result.total_cost || 'N/A'}</span>
        </div>
      </div>
    </div>
  `;
}

export function renderVerdict(verdict) {
  if (!verdict) return '';

  const isPass = verdict.includes('PASS');
  const className = isPass ? 'verdict-pass' : 'verdict-fail';

  return `
    <div class="verdict ${className}">
      <div class="verdict-status">${isPass ? '✓ PASS' : '✗ FAIL'}</div>
      <pre class="verdict-details">${verdict}</pre>
    </div>
  `;
}
