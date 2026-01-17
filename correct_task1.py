# Write your corrected implementation for Task 1 here.
# Do not modify `task1.py`.
def calculate_average_order_value(orders):
    """
    Calculates the average value of non-cancelled orders.
    """
    if not isinstance(orders, list) or len(orders) == 0:
        return 0.0

    total = 0.0
    valid_count = 0

    for order in orders:
        # Filter for valid, non-cancelled orders
        if isinstance(order, dict) and order.get("status") != "cancelled":
            total += order.get("amount", 0)
            valid_count += 1

    # Avoid division by zero if all orders were filtered out
    if valid_count == 0:
        return 0.0

    return total / valid_count
