# AI Code Review Assignment (Python)

## Candidate
- Name: Tsigemariam Zewdu
- Approximate time spent: 70 minutes

---

# Task 1 — Average Order Value

## 1) Code Review Findings
### Critical bugs
- Logic Error (SKewed Average): The function divides `len(orders)` (all orders) instead of the count of non-cancelled orders. This results in  a mathematically incorrect average that is lower than the true value.
- ZeroDivisionErro: If the input `orders` is empty, the code attempts to divide by zero, causing a runtime crash.

### Edge cases & risks
- All Orders Cancelled: If the list contains orders but every single one is "cancelled", then `total` remains 0 and the code will crash because it tries to divide by the orginal length.
- Schema Sensetivity : The code assumes every item in the list is a dictionary containing the keys `status` and `amount` . A missing key or a `None` entry would raise a `key Error` or `Type Error`.
### Code quality / design issues
- Improper Variable Naming : The variable `count` is misleading as it represents the total input size not the sample size used for the average.
- Lack of input validation: There is no check to ensure `orders` is actually a list before processing.

## 2) Proposed Fixes / Improvements
### Summary of changes
- Corrected Denominator : Introduced `vaid_count` to track only the orders included in the sum.
- Zero-check : added a check to reutrn `0.0` if no valid orders exist, preventing crashes.
-Defensive Access : Used `.get()` for dictionary access to prevent `keyError` on malformed data.
- Data consistency : Initialized `total` as a float to ensure consistent return types.

### Corrected code
See `correct_task1.py`

> Note: The original AI-generated code is preserved in `task1.py`.

 ### Testing Considerations
If you were to test this function, what areas or scenarios would you focus on, and why?

- Mathematical Accuracy (The Denominator Fix): Test with a mix of cancelled and active orders (e.g., 2 active, 2 cancelled). Verify the divisor is `2`, not` 4`.
- Empty and Null Inputs: Test with an empty list [] and a None input to ensure the guard clauses return 0.0 instead of crashing.
- All Orders Cancelled: Ensure that if 100% of orders are filtered out, the valid_count == 0 check prevents a ZeroDivisionError.
- Malformed Dictionaries: Provide dictionaries missing the "amount" or "status" keys. This tests the robustness of the .get() method and ensures the function uses the default value of 0 rather than raising a KeyError.

## 3) Explanation Review & Rewrite
### AI-generated explanation (original)
> This function calculates average order value by summing the amounts of all non-cancelled orders and dividing by the number of orders. It correctly excludes cancelled orders from the calculation.

### Issues in original explanation
- Inaccurate Logic : It claims to correctly exclude cancelled orders but the orignal code only excluded their value not their count leading to a wrong average 


### Rewritten explanation
- This function calculates the average value of orders by filtering for those without a "cancelled" status. It calculates the mean by dividing the total sum of valid order amounts by the specific count of those non-cancelled orders. It includes safety checks to handle empty inputs or datasets containing only cancelled orders.

## 4) Final Judgment
- Decision: Reject
- Justification:The code contains a fundamental logical flaw (averaging a subset of values using the count of the whole set) and will crash on empty input. It produces mathematically incorrect results.
- Confidence & unknowns:High confidence in the logic error and the fix. Unknown: Whether the business logic requires a specific return value (like None or an Exception) for empty datasets, but 0.0 is the most common safe default for an averaging utility.

---

# Task 2 — Count Valid Emails

## 1) Code Review Findings
### Critical bugs
- Validation Logic Failure: The original code considered any string with an @ symbol to be a valid email (e.g., "@@@", "user@"). This is a massive false-positive rate.
- Type Incompatibility: The original code would crash with a TypeError if the list contained None or an integer, as the in operator on an integer is invalid.
- Zero Division Risk (Structural): While the original function returns a count, the logical failure to validate the input structure makes it unreliable for any subsequent operations.
### Edge cases & risks
- Empty Strings/Whitespace: The original code counts " @ " as a valid email
- Non-String Objects: Lists often contain un clean data (nulls from databases). The original code does not handle these safely
- Malformed Domains: An email like user@domain (missing the .com or extension) was incorrectly accepted.
### Code quality / design issues
- Inefficiency: The original code's explanation claimed "safety" that didn't exist in the implementation.
- Lack of Sanitization: The original code didn't strip() whitespace, meaning an otherwise valid email with a trailing space would be treated differently depending on the implementation.

## 2) Proposed Fixes / Improvements
### Summary of changes
- Regex Validation: Introduced a compiled Regular Expression to ensure a local_part@domain.extension structure.
- Type Guarding: Added isinstance(email, str) to skip non-string entries without crashing.
- Data Cleaning: Added .strip() to handle accidental leading/trailing whitespace.

### Corrected code
See `correct_task2.py`

> Note: The original AI-generated code is preserved in `task2.py`. 


### Testing Considerations
If you were to test this function, what areas or scenarios would you focus on, and why?
- Regex Pattern Boundaries: Test  strings like user@domain (missing extension) or @domain.com (missing local part) to ensure the regex is strict enough.
- Type Safety: Include None, integers, or lists inside the emails list. This confirms the isinstance(email, str) check prevents `NoneType` object has no attribute `strip` errors.

- Sanitization: Test emails with leading/trailing spaces (e.g., " user@test.com "). This verifies that strip() is correctly applied before regex matching.

- Multiple Delimiters: Test strings with multiple @ symbols (e.g., user@domain@company.com) to ensure the regex correctly rejects them.

## 3) Explanation Review & Rewrite
### AI-generated explanation (original)
> This function counts the number of valid email addresses in the input list. It safely ignores invalid entries and handles empty input correctly.

### Issues in original explanation
- False Claims: It did not "safely ignore" invalid entries, it crashed on non-string entries.

- Oversimplification: It ignored the fact that the validation logic was effectively non-existent (only checking for @).

### Rewritten explanation
- This function counts valid emails by enforcing a local_part@domain.extension pattern via regular expressions. It provides robustness by skipping non-string data types and trimming whitespace from entries. It returns a count of zero for empty or non-list inputs.

## 4) Final Judgment
- Decision: Reject
- Justification:The original code provides an illusory check that fails to distinguish between a valid email and a random string containing an "@" symbol. The lack of type checking makes it dangerous for production use where data may be inconsistent.
- Confidence & unknowns:High confidence. While no regex is 100% perfect for all global email standards, the proposed fix is  more secure and reliable than the original logic.

---

# Task 3 — Aggregate Valid Measurements

## 1) Code Review Findings
### Critical bugs
- Skewed Average (Mathematical Logic Error): The count is fixed at `len(values)` at the start. If some values are None, they are skipped in the total, but the denominator still includes them. This results in a  average that is lower than the true average of the valid measurements.

- ZeroDivisionError: If the values list is empty, `len(values)` is 0, causing a crash.

- ZeroDivisionError (Filtered): Even if the list isn't empty, if all entries are `None`, the code will still attempt to divide 0 by the length of the list, which technically avoids a crash but returns an inaccurate 0.0 when it should perhaps be handled as a "no data" state.

### Edge cases & risks
- Non-Numeric Strings: The code uses float(v). If a value is a string that cannot be converted (e.g., "N/A" or "error"), the function will crash with a ValueError.

- None-Only Input: If the input is [None, None], the function returns 0.0. In data science, the average of "nothing" is usually undefined or None, not 0.0.

### Code quality / design issues
- Misleading Explanation: The AI claims it "ensures an accurate average," which is objectively false due to the denominator bug.

- Type Flexibility: While it claims to handle mixed types, it relies on a risky float() cast without any error catching.

## 2) Proposed Fixes / Improvements
### Summary of changes
- Dynamic Counter: Moved the count increment inside the if v is not None block so that only valid measurements contribute to the denominator.

- Type Guarding: Added a try-except block around the float(v) conversion to handle "dirty" data (like strings) gracefully.

- Zero-Check: Added a final check to return 0.0 (or None) if no valid measurements were processed to prevent division by zero.

### Corrected code
See `correct_task3.py`

> Note: The original AI-generated code is preserved in `task3.py`.

### Testing Considerations
If you were to test this function, what areas or scenarios would you focus on, and why?

- Data Handling: Test a list containing strings that look like numbers ("10.5"), strings that don't ("N/A"), and None values. This verifies that the try-except block correctly converts what it can and skips what it can't.

- Inconsistent Types: Include nested objects like [10, [20], {"val": 30}]. This tests if the TypeError catch in your implementation prevents a crash when float() is called on a non-convertible type.

- Zero Values: Test with [0, 0, 0] to ensure that valid zeros are counted in the average and not mistakenly treated as "missing" data.

- Extreme Values: Test with very large floats or very small decimals to ensure Python’s standard float precision is maintained during summation.

## 3) Explanation Review & Rewrite
### AI-generated explanation (original)
> This function calculates the average of valid measurements by ignoring missing values (None) and averaging the remaining values. It safely handles mixed input types and ensures an accurate average

### Issues in original explanation
- Mathematically False: It does not ensure an accurate average because it includes the "None" slots in the count.

- Safety Overstatement: It does not safely handle "mixed input types"; any non-numeric string will cause a crash.

### Rewritten explanation
- This function calculates the mean of numeric measurements by filtering out None values and non-numeric entries. Unlike the original version, it correctly updates the divisor to reflect only the number of valid items processed, ensuring a mathematically accurate average. It also includes error handling to skip malformed data that cannot be converted to a float.

## 4) Final Judgment
- Decision: Reject
- Justification: The function fails its primary purpose: providing an accurate average. By using the total length of the input list as the denominator while skipping values in the numerator, the result is mathematically invalid. Additionally, the lack of error handling for type conversion makes the "mixed input" claim in the explanation dangerous and incorrect.
- Confidence & unknowns: High confidence. The denominator bug is a common error in data processing scripts, and the fix is a standard requirement for robust data aggregation.
