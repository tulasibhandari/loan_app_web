from .utils import np, safe_float

def get_financial_context(member):
    items = member.collateralincomeexpense_set.all()

    income = [i for i in items if i.type == 'income']
    expense = [i for i in items if i.type == 'expense']

    total_income = sum(safe_float(i.amount) for i in income)
    total_expense = sum(safe_float(i.amount) for i in expense)

    return {
        'income_items': [
            {'field': i.field, 'amount': np(i.amount)}
            for i in income
        ],
        'expense_items': [
            {'field': i.field, 'amount': np(i.amount)}
            for i in expense
        ],
        
        'total_income': np(total_income),
        'total_expense': np(total_expense),
    }
