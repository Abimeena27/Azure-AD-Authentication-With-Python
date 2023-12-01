import json
import requests
from msal import ConfidentialClientApplication

client_id ="45ad3485-3466-429a-9b2d-dde3b53656fe"
client_secret= "FPz8Q~dOqMyILUejgocJRq2Cd-ljSJan-sMw.dq8"
tenant_id = "5fe5e79b-0daf-404f-9bde-0a3bff7b1328"

msal_authority =f"https://login.microsoftonline.com/{tenant_id}"

msal_scope=["https://graph.microsoft.com/.default"]


msal_app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=msal_authority,    

)

result = msal_app.acquire_token_for_client(scopes=msal_scope)

if "access_token" in result:
    access_token = result["access_token"]
else:
    raise Exception("No access token")

headers={
    "Authorization":f"Bearer {access_token}",
    "Content-Type":"application/json",
}

response = requests.get(
    url="https://graph.microsoft.com/v1.0/users",
    headers=headers,
)

json_new=json.dumps(response.json())


data = json.loads(json_new)

# Extract the userPrincipalName from each user object
user_principal_names = [user['userPrincipalName'] for user in data['value']]

#print(user_principal_names)
