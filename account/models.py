from django.db import models

# Create your models here.
class CatalystCount(models.Model):
    name = models.CharField(("name"), max_length=250)
    domain = models.CharField(("domain"), max_length=200)
    year_founded = models.CharField(("year founded"), max_length=20)
    industry = models.CharField(("industry"), max_length=250)
    locality = models.CharField(("locality"), max_length=250, null=True,  blank=True)
    country = models.CharField(("country"), max_length=250, null=True,  blank=True)
    linkedin_url = models.CharField(("linkedin url"), max_length=250, null=True, blank=True)
    employees_from = models.CharField(("employees_from"), max_length=250, null=True, blank=True)
    employees_to = models.CharField(("employees_to"), max_length=250, null=True, blank=True )