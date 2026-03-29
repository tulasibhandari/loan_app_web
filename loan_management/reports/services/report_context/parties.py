from .utils import np

def get_parties_context(member):
    witnesses = getattr(member, 'witnessinfo_set', []).all() if hasattr(member, 'witnessinfo_set') else []
    guarantors = getattr(member, 'guarantordetails_set', []).all() if hasattr(member, 'guarantordetails_set')else []

    return{
        'witnesses': [
            {
                'name': w.name,
                'relation': w.relation,
                'age': np(w.age),
            }
            for w in witnesses
        ],

        'guarantor': [
            {
                'guarantor_name': g.guarantor_name,
                'guarantor_phone': np(g.guarantor_phone),
                'guarantor_age': np(g.guarantor_age),
            }
            for g in guarantors
        ],
    }