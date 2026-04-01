from .utils import np

def get_collateral_context(member):

    collateral_basic = getattr(member, 'collateral_basic', None)

    properties = member.collateralproperty_set.all() or []
    family_details = member.collateralfamilydetail_set.all() or []

    return {
        'monthly_saving': np(collateral_basic.monthly_saving if collateral_basic else ''),
        'child_saving': np(collateral_basic.child_saving if collateral_basic else ''),
        'total_saving': np(collateral_basic.total_saving if collateral_basic else ''),
        'share_amount': np(collateral_basic.share_amount if collateral_basic else ''),

        'properties': [
            {
                'owner_name': p.owner_name,
                'district': p.district,
                'municipality_vdc': p.municipality_vdc,
                'ward_no': np(p.ward_no),
                'sheet_no': np(p.sheet_no),
                'plot_no': np(p.plot_no),
                'area': np(p.area),
                'land_type': p.land_type,
            }
            for p in properties
        ],

        'family_members': [
            {
                'name': f.name,
                'age': np(f.age),
                'relation': f.relation,
                'occupation': f.occupation,
                'monthly_income': np(f.monthly_income),
            }
            for f in family_details
        ],
    }