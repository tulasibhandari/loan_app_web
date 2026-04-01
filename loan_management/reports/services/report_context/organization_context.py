def get_organization_context(org):
    return {
        'company_name': org.company_name if org else '',
        'company_address': org.address if org else '',
    }