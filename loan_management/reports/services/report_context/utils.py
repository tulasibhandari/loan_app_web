from utils.nepali_number import to_nepali_digits

def np(value):
    return to_nepali_digits(value)

def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0