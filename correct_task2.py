# Write your corrected implementation for Task 2 here.
# Do not modify `task2.py`.
import re
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def count_valid_emails(emails):
    """
    Counts valid email addresses using regex validation and type safety.
    """
    if not isinstance(emails, list):
        return 0

    count = 0
    for email in emails:
        # Skip non-string entries (None, int, etc.) to prevent crashes
        if not isinstance(email, str):
            continue

        # Clean whitespace and validate against regex
        cleaned_email = email.strip()
        if EMAIL_REGEX.match(cleaned_email):
            count += 1

    return count