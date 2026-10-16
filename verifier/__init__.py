"""Verifier package for travel planning plugin."""

from pathlib import Path
import json
from . import task as task_verifier


def verify_input(tool, value):
    """Verify tool input.

    Args:
        tool: The tool enum value
        value: The input value to verify

    Returns:
        None if valid, raises exception otherwise
    """
    # Input validation is handled by contract types
    return None


def verify_output(tool, input_value, output_value, workspace):
    """Verify tool output.

    Args:
        tool: The tool enum value
        input_value: The input that was provided
        output_value: The output to verify
        workspace: Path to workspace directory

    Returns:
        None if valid, raises exception otherwise
    """
    # Output validation is handled by contract types
    return None


def verify_task(task, arguments, reference, workspace, action_trace):
    """Verify task completion.

    Args:
        task: The task enum value
        arguments: Task input arguments
        reference: Reference/expected output
        workspace: Path to workspace directory
        action_trace: List of action trace events

    Returns:
        Verdict string ("PASS" or "FAIL\\n..." with errors)
    """
    workspace_path = Path(workspace)

    # Load required files
    output_file = workspace_path / "output.json"
    trace_file = workspace_path / "action_trace.json"
    request_file = workspace_path / "request.json"
    options_file = workspace_path / "options.json"

    # Check files exist
    if not output_file.exists():
        return "FAIL\noutput.json not found"
    if not trace_file.exists():
        return "FAIL\naction_trace.json not found"
    if not request_file.exists():
        return "FAIL\nrequest.json not found"
    if not options_file.exists():
        return "FAIL\noptions.json not found"

    # Call the main verifier
    try:
        errors = task_verifier.verify(
            str(output_file),
            str(request_file),
            str(options_file),
            str(trace_file)
        )

        if not errors:
            return "PASS"
        else:
            return "FAIL\n" + "\n".join(errors)
    except Exception as e:
        return f"FAIL\nverifier error: {e}"
