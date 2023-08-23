import datetime
from config import config
from azure.storage.blob import (AccountSasPermissions, generate_account_sas, ResourceTypes)
from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential



_storage_account_key = open("./keys/azure_storage_key", "r").read()
_storage_account_name = config['azure']['storage_account_name']

_comm_account_key = AzureKeyCredential(open("./keys/azure_communication_services_key", "r").read())
_comm_endpoint = config['azure']['communication_services_endpoint']

_sender_email_address = config['azure']['sender_email_address']

email_client = EmailClient(_comm_endpoint, _comm_account_key)


def create_account_sas():
    # Create an account SAS that's valid for 2 minutes
    start_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = start_time + datetime.timedelta(minutes=2)

    # Define the SAS token permissions
    sas_permissions=AccountSasPermissions(write=True)

    # Define the SAS token resource types
    sas_resource_types=ResourceTypes(object=True)

    sas_token = generate_account_sas(
        account_name=_storage_account_name,
        account_key=_storage_account_key,
        resource_types=sas_resource_types,
        permission=sas_permissions,
        expiry=expiry_time,
        start=start_time
    )

    return sas_token




def send_email(title, recipients, text_message, html_message):
    
    # recipients should have the form 
    # recipients = [
    #     {
    #         "address": "emailaddress",
    #         "displayName": "recipientName"
    #     }
    # ]
    if title is None:
        raise Exception({'error_code': 'email_format_error', 'error_message': 'subject empty'}) from None
    if (text_message is None) and (html_message is None):
        raise Exception({'error_code': 'email_format_error', 'error_message': 'body empty'}) from None
    if (recipients is None) or len(recipients) == 0:
        raise Exception({'error_code': 'email_format_error', 'error_message': 'no recipient'}) from None

    
    message = {
        "content": {
            "subject": title,
            "plainText": text_message,
            "html": html_message
        },
        "recipients": {
            "to": recipients
        },
        "senderAddress": _sender_email_address
    }

    poller = email_client.begin_send(message)
