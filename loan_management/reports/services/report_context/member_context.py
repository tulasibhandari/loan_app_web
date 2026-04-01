from .utils import np
from utils.nepali_date_utils import calculate_age_bs_np

def get_member_context(member):
    age = calculate_age_bs_np(member.dob_bs)

    return {
        'member_number': np(member.member_number),
        'member_name': member.member_name,
        'phone': np(member.phone or ''),
        'email': member.email or '',
        'citizenship_no': np(member.citizenship_no or ''),
        'father_name': member.father_name or '',
        'grandfather_name': member.grandfather_name or '',
        'spouse_name': member.spouse_name or '',
        'spouse_phone': np(member.spouse_phone or ''),
        'address': member.address or '',
        'ward_no': np(member.ward_no or ''),
        'profession': member.profession or '',
        'dob_bs': np(member.dob_bs or ''),
        'business_name': member.business_name or '',
        'business_address': member.business_address or '',
        'job': member.job or '',
        'job_address': member.job_address or '',
        'age': np(age) if age else '',
    }