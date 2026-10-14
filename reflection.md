# Reflection — Static Code Analysis

> Note: The ZIP included the README and source file, but not the separate lab handout containing the exact four reflection questions. The answers below address four standard reflection themes for this exercise; align the headings with the handout if its wording differs.

## 1. What did the static analysis tools help identify?
Static analysis is useful for finding maintainability and reliability problems before a program is exercised with every possible input. Pylint can flag naming, documentation, unused imports, and general code-quality issues; Flake8 checks style and common Python errors; Bandit focuses on security-sensitive patterns. In this program, the most important issues were unsafe temporary-file creation, a bare exception handler, mutable default state, and insufficient input validation.

## 2. Which issues were most important, and why?
The unsafe `tempfile.mktemp()` pattern was important because another process could create the same path before the program opens it. The broad exception handler was also important because it conceals unexpected failures. Invalid dates and a negative service interval could make inspection checks fail or produce misleading alerts. These issues affect security, correctness, and trust in the maintenance report, so they take priority over naming and formatting.

## 3. What changes were made, and how do they improve the program?
The updated program validates asset IDs and dates, rejects future service dates and non-positive intervals, and handles unknown assets without crashing. It removes the mutable default argument, writes files with context managers and UTF-8 encoding, uses a safely created named temporary file, renames `printAlerts` to `print_alerts`, and adds a main guard so importing the module does not prompt the user or write files. These changes make behavior more predictable and the code easier to test and maintain.

## 4. What are the limitations of static analysis?
Static analysis cannot prove that a program is correct or that every runtime scenario is safe. Tools may miss business-logic defects, produce false positives, or fail to understand requirements such as the intended inspection interval. For that reason, their findings should be reviewed and combined with execution tests, boundary-case tests, and code review. For this lab, useful manual tests include blank and duplicate IDs, malformed dates, future dates, unknown asset IDs, invalid intervals, and overdue versus not-yet-overdue assets.
