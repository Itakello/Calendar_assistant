import random

import requests
from flask import Flask, redirect, request

from main import main

app = Flask(__name__)
app.secret_key = 'dtC8Q~mWLE2MgoTfNCwdfJ70-~nKUeZ-Dpwi2caQ'

# Replace these with your app's credentials
AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/'
client_id = '1d60f500-61ef-4479-b8c1-e552956ba986'
client_secret = 'dtC8Q~mWLE2MgoTfNCwdfJ70-~nKUeZ-Dpwi2caQ'
redirect_uri = 'http://localhost:5000/auth-callback'
scope = 'Calendars.Read Calendars.ReadWrite openid profile User.Read offline_access email'
state_val = random.randint(0, 1000000)

@app.route('/')
def home():
    authorize_url = f'{AUTH_URL}/authorize'
    return redirect(f'{authorize_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope={scope}&state={state_val}')

@app.route('/auth-callback')
def auth_callback():
    resp_state = int(request.args.get('state'))
    assert resp_state == state_val
    token_url = f'{AUTH_URL}/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(token_url, data=token_data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        main(access_token)
    else:
        return 'Error retrieving token: {0} - {1}'.format(response.status_code, response.text)

if __name__ == '__main__':
    app.run(port=5000)
