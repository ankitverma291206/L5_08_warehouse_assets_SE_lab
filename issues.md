# Static Code Analysis — Issues Register

Line numbers refer to the original `maintenance_system.py` supplied with the lab. Severity is an assessment of likely impact, not a tool-generated rating.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe temporary file creation | Security (High) | 29 | `tempfile.mktemp()` returns a name without securely creating the file, leaving a race condition. | Use `NamedTemporaryFile` to create the file safely and uniquely. |
| Bare exception handler | Reliability (High) | 15–17 | `except:` catches every exception and hides the underlying cause, including programming errors. | Catch the expected `ValueError` during date parsing and explicitly handle unknown asset IDs. |
| Mutable default argument | Correctness (Medium) | 9–12 | `logs=[]` is shared across calls, so state leaks between registrations. | Remove the default mutable list; derive the count from the registry instead. |
| File handles not managed safely | Reliability (Medium) | 26–28, 32–34 | Files are opened and closed manually; an exception can prevent closure. | Use `with` context managers and specify UTF-8 encoding. |
| Invalid asset IDs accepted | Correctness (Medium) | 38–41 | Empty IDs are registered and duplicate IDs overwrite existing records. | Reject blank and duplicate IDs before changing the registry. |
| Invalid dates accepted until later | Correctness (Medium) | 14–17 | Arbitrary date strings can be stored and then crash inspection checks. | Parse and validate dates before storing them; reject future dates. |
| Negative inspection interval | Correctness (Medium) | 23–25, 46 | A negative interval makes assets appear overdue immediately. | Require the interval to be a positive integer. |
| Unconditional module execution | Maintainability (Low) | 51 | Importing the module immediately runs prompts and writes files. | Call `main()` only under `if __name__ == "__main__":`. |
| Non-PEP 8 function name | Style (Low) | 36 | `printAlerts` uses mixed case rather than snake_case. | Rename it to `print_alerts`. |
| Unused import | Style | 3 | `logging` is imported but never used. | Remove the unused import. |

## Fixes implemented

The cleaned `maintenance_system.py` addresses the issues above: it removes the shared mutable default, validates asset IDs and service dates, prevents invalid intervals, uses context managers, replaces `mktemp()` with `NamedTemporaryFile`, uses snake_case, removes the unused import, and adds a main guard and type annotations.
