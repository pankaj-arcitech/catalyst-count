from import_export import resources
from account.models import CatalystCount

class CatalystCountResources(resources.ModelResource):
    class meta:
        model = CatalystCount