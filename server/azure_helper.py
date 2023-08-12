import datetime
from config import config
from azure.storage.blob import (AccountSasPermissions, generate_account_sas, ResourceTypes)


_account_key = open("./keys/azure_storage_key", "r").read()
_account_name = config['azure']['account_name']


def create_account_sas():
    # Create an account SAS that's valid for one day
    start_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = start_time + datetime.timedelta(minutes=2)

    # Define the SAS token permissions
    sas_permissions=AccountSasPermissions(write=True)

    # Define the SAS token resource types
    # For this example, we grant access to service-level APIs
    sas_resource_types=ResourceTypes(object=True)

    sas_token = generate_account_sas(
        account_name=_account_name,
        account_key=_account_key,
        resource_types=sas_resource_types,
        permission=sas_permissions,
        expiry=expiry_time,
        start=start_time
    )

    return sas_token