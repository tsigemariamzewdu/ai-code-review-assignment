# Write your corrected implementation for Task 3 here.
# Do not modify `task3.py`.
def average_valid_measurements(values):
    """
    Calculates the average of valid numeric measurements, 
    ignoring None and non-numeric values.
    """
    if not values:
        return 0.0

    total = 0.0
    valid_count = 0

    for v in values:
        if v is not None:
            try:
                total += float(v)
                valid_count += 1
            except (ValueError, TypeError):
                # Skip values that cannot be converted to a float
                continue

    if valid_count == 0:
        return 0.0

    return total / valid_count