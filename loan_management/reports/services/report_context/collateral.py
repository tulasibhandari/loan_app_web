from .utils import np

def get_collateral_context(member):
    basic = member.collateralbasic_set.first()

    properties = member.collateralproperty_set.all()
    family = member.collateralfamilydetail_set.all()

    return {
        'monthly_saving': np(basic.monthly_saving) if basic else '',
        'total_saving': np(basic.total_saving) if basic else '',

        'properties': [
            {
                'owner_name': p.owner_name,
                'ward_no': np(p.ward_no),
                'sheet_no': np(p.sheet_no),
                'plot_no': np(p.plot_no),
                'area': np(p.area),
            }
            for p in properties
        ],

        'family': [
            {
                'name': f.name,
                'age':np(f.age),
                'relation': f.relation,
                'monthly_income': np(f.monthly_income),
            }
            for f in family
        ],
    }