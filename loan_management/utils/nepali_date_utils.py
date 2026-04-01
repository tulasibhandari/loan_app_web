from datetime import date

try:
    from nepali_datetime import date as nepali_date
    HAS_NEPALI = True
except ImportError:
    HAS_NEPALI = False


def calculate_age_bs(dob_bs):
    print("DOB RECEIVED:", dob_bs)

    """ Calculate age from BS date"""

    if not dob_bs:
        print("DOB EMPTY ❌")
        return ''
    
    try:
        from utils.nepali_number import to_english_digits

        dob_bs = to_english_digits(dob_bs)
        print("DOB AFTER COVERSION:", dob_bs)

        # Normalize format
        dob_bs = dob_bs.replace('-', '/')
        year, month, day = map(int, dob_bs.split('/'))

        print("PARSED:", year, month, day)

        if HAS_NEPALI:
            today = nepali_date.today()
            print("TODAY BS:", today)

            age = today.year - year
            
            # Adjusting if birthday has not reached this year
            if (today.month, today.day) < (month, day):
                age -= 1
            
            print("AGE CALCULATED:", age)
            return age
        
        else:
            # Fallback (approximate age)
            today = date.today()
            age = today.year - year
            print("AGE FALLBACK:", age)
            return age

    except Exception as e:
        print("AGE ERROR:", e)
        return ''
    

from utils.nepali_number import to_nepali_digits

def calculate_age_bs_np(dob_bs):
    age = calculate_age_bs(dob_bs)
    return to_nepali_digits(age) if age != '' else ''


