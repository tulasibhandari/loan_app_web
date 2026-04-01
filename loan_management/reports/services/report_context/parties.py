from .utils import np

def get_parties_context(member):
    witnesses = member.witnessinfo_set.all() or []
    guarantors = member.guarantordetails_set.all() or []


    return {
        'witnesses': [
            {
                'name': w.name,
                'relation': w.relation,
                'address': w.address,
                'ward': np(w.ward),
                'age': np(w.age),
            }
            for w in witnesses
        ],

        'guarantors': [
            {
                'guarantor_name': g.guarantor_name,
                'guarantor_address': g.guarantor_address,
                'guarantor_ward': np(g.guarantor_ward),
                'guarantor_phone': np(g.guarantor_phone),
                'guarantor_age': np(g.guarantor_age),
            }
            for g in guarantors
        ],
    }