from django.db import models

class OrganatizationProfile(models.Model):
    """Organization details"""
    company_name = models.CharField(max_length=200)
    address = models.TextField()
    logo_path = models.ImageField(upload_to='logos/', blank=True, null=True)

    class Meta:
        db_table = 'organization_profile'
    
    def __self__(self):
        return self.company_name