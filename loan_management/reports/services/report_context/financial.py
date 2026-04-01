from .utils import np

def get_financial_context(member):

    income_expenses = member.collateralincomeexpense_set.all() or []

    income = [i for i in income_expenses if i.type == 'income']
    expense = [i for i in income_expenses if i.type == 'expense']

    return {
        'income_items': [{'field': i.field, 'amount': i.amount} for i in income],
        'expense_items': [{'field': i.field, 'amount': i.amount} for i in expense],

        'total_income': np(sum(float(i.amount or 0) for i in income)),
        'total_expense': np(sum(float(i.amount or 0) for i in expense)),
    }