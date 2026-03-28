from django.core.cache import cache
from dashboard.models import OrganatizationProfile

def get_organization_context():
    org = cache.get('org_profile')

    if not org:
        org = OrganatizationProfile.objects.first()
        cache.set('org_profile', org, 3600)

    return {
        'company_name': org.company_name if org else '',
        'comapany_address': org.address if org else '',
    }