import re

def increment_ending_number(s: str) -> str:
    match = re.search(r'(\d+)$', s)
    if match:
        number = int(match.group(1))
        new_number = str(number + 1)
        return s[:match.start(1)] + new_number
    else:
        return s + '1'