from .utils import np
from .num_to_words import num_to_nepali_words

def get_loan_context(loan):
    return {
        'loan_type': loan.loan_type,
        'interest_rate': np(loan.interest_rate),
        'loan_duration': np(loan.loan_duration),
        'repayment_duration': np(loan.repayment_duration),
        'loan_amount': np(loan.loan_amount),
        'loan_amount_in_words': loan.loan_amount_in_words or num_to_nepali_words(loan.loan_amount),
        'loan_status': loan.status,
        'loan_completion_year': np(loan.loan_completion_year or ''),
        'loan_completion_month': np(loan.loan_completion_month or ''),
        'loan_completion_day': np(loan.loan_completion_day or ''),
    }