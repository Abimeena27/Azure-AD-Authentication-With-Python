# from flask import Flask, render_template, request,url_for
# from azure.common.credentials import ServicePrincipalCredentials
# import requests
# import json
# import jsuser


# app = Flask(__name__)

# # Azure AD app details
# CLIENT_ID ="45ad3485-3466-429a-9b2d-dde3b53656fe"
# CLIENT_SECRET= "FPz8Q~dOqMyILUejgocJRq2Cd-ljSJan-sMw.dq8"
# TENANT_ID= "5fe5e79b-0daf-404f-9bde-0a3bff7b13"
# #  = 'd3629e15-7497-4c83-9004-0c093d3a9c7c'
# #  = 'Od48Q~D4ey7Pztu.AGN9VoUO8gJIyqKNOos.QcJ1'
# #  = 'acea1646-8cfb-44f2-af12-702118922049'

# @app.route('/')
# def index():
#     return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     email = request.form['user']
#     #password = request.form['password']
        
#     # Authenticate with Azure AD using a client secret credential
#     credential = ServicePrincipalCredentials(
#         client_id=CLIENT_ID,
#         secret=CLIENT_SECRET,
#         tenant=TENANT_ID
#     )
#     access_token = credential.token['access_token']
#     #return access_token

#     url = 'https://login.microsoftonline.com/acea1646-8cfb-44f2-af12-702118922049/oauth2/v2.0/authorize'
#     headers = {'Authorization': 'Bearer ' + access_token}
#     # headers={
#     #     'Authorization' :f"Bearer"
#     # }
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         #data = json.loads(jsuser.json_new)
        
#         # user_data=response.json()
#         # user_email = user_data['mail']
#         if email not in jsuser.user_principal_names:
#             return render_template('error.html')
#         else:
#             return render_template('Shopify.html')
#     else:
#         return str(response.status_code)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, redirect, url_for
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

oauth = OAuth(app)

# Azure AD app details
CLIENT_ID ="45ad3485-3466-429a-9b2d-dde3b53656fe"
CLIENT_SECRET= "FPz8Q~dOqMyILUejgocJRq2Cd-ljSJan-sMw.dq8"
TENANT_ID= "5fe5e79b-0daf-404f-9bde-0a3bff7b13"

msgraph = oauth.remote_app(
    'msgraph',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': 'User.Read'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/{0}/oauth2/v2.0/token'.format(TENANT_ID),
    authorize_url='https://login.microsoftonline.com/{0}/oauth2/v2.0/authorize'.format(TENANT_ID)
)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return msgraph.authorize(callback=url_for('login', _external=True))

@app.route('/login/authorized')
def authorized():
    resp = msgraph.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error'], request.args['error_description']
        )
    # Save the access token in session
    session['msgraph_token'] = (resp['access_token'], '')
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'msgraph_token' in session:
        # Use the access token to make requests to Microsoft Graph API
        response = msgraph.get('me')
        return 'Logged in as: {0}'.format(response.data['displayName'])
    return redirect(url_for('login'))

@msgraph.tokengetter
def get_msgraph_oauth_token():
    return session.get('msgraph_token')

if __name__ == '__main__':
    app.run(debug=True)
