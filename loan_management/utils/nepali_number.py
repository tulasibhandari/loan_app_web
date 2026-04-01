NEPALI_DIGITS = {
    '0': '०',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
}


def to_nepali_digits(value):
    """
    Convert any number/string to Nepali (Devanagari) digits.
    Handles int, float, str safely.
    """
    if value is None:
        return ''

    value_str = str(value)

    return ''.join(NEPALI_DIGITS.get(ch, ch) for ch in value_str)


NEPALI_TO_ENGLISH = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',
}

def to_english_digits(value):
    return ''.join(NEPALI_TO_ENGLISH.get(ch, ch) for ch in str(value))