def num_to_nepali_words(num):
    """Convert number to Nepali words"""
    try:
        num = float(num)
    except (TypeError, ValueError):
        return "शून्य"

    if num == 0:
        return "शून्य रुपैयाँ"

    ones = ["", "एक", "दुई", "तीन", "चार", "पाँच", "छ", "सात", "आठ", "नौ",
            "दश", "एघार", "बाह्र", "तेह्र", "चौध", "पन्ध्र", "सोह्र", "सत्र",
            "अठार", "उन्नाइस"]
    tens = ["", "दश", "बीस", "तीस", "चालिस", "पचास", "साठी", "सत्तरी", "असी", "नब्बे"]

    def convert_below_100(n):
        if n < 20:
            return ones[n]
        return tens[n // 10] + (" " + ones[n % 10] if n % 10 else "")

    def convert_below_1000(n):
        if n < 100:
            return convert_below_100(n)
        hundreds = ones[n // 100] + " सय"
        remainder = n % 100
        return hundreds + (" " + convert_below_100(remainder) if remainder else "")

    n = int(num)
    if n < 1000:
        return convert_below_1000(n) + " रुपैयाँ"

    parts = []
    crore = n // 10000000
    n %= 10000000
    lakh = n // 100000
    n %= 100000
    hazar = n // 1000
    n %= 1000

    if crore:
        parts.append(convert_below_1000(crore) + " करोड")
    if lakh:
        parts.append(convert_below_1000(lakh) + " लाख")
    if hazar:
        parts.append(convert_below_1000(hazar) + " हजार")
    if n:
        parts.append(convert_below_1000(n))

    return " ".join(parts) + " रुपैयाँ"