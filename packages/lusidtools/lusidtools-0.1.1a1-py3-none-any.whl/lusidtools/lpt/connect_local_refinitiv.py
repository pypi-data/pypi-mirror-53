import json
import os
import lusidtr as lusid
from . import lpt
from .record import Rec

from datetime import datetime

import requests
from urllib.request import quote
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from msrest.authentication import BasicTokenAuthentication

# This is a connector for using the refinitiv sdk with a local
# running instance.
# It is similar to the regular LUSID connector, but uses the 
# Refinitiv (TR) sdk

def connect(config,**kwargs):

    # Variation of the BasicTokenAuthentication class that will refresh credentials
    # if LUSID responds with a 401 failure
    class RefreshingTokenAuthentication(BasicTokenAuthentication):

        def __init__(self, get_token_fn):
            self.scheme = 'Bearer'
            self.get_token_fn = get_token_fn
            # Initial Okta authentication
            self._refresh_token()

        def _refresh_token(self):
            self.token_acquisition_time = datetime.now()
            self.token = self.get_token_fn()
            self.token_age_limit = int(self.token.get('expires_in',3600))

        # Method is called in response to a TokenExpiredError
        def refresh_session(self):
            # Get refreshed tokens and return a new session
            self._refresh_token()
            return self.signed_session()

        def signed_session(self):
            # See how long it has been since we got the tokens
            # add on 5 seconds as a buffer
            age = (datetime.now() - self.token_acquisition_time).total_seconds() + 5

            if age > self.token_age_limit:
               self._refresh_token()

            session = super(RefreshingTokenAuthentication,self).signed_session()

            # hook function to check for unauthorised response from LUSID
            # Raises an error to trigger the refresh_session() logic
            def intercept_unauth_error(r,*args,**kwargs):
                if r.status_code == 401:
                   # Unauthorised. Raise a TokenExpiredError
                   # this will result in a resubmit of the request
                   raise TokenExpiredError()
            
            session.hooks['response'].append(intercept_unauth_error)
            return session


    token_url = os.getenv("FBN_TOKEN_URL", config["api"]["tokenUrl"])
    username = os.getenv("FBN_USERNAME", config["api"]["username"])
    password = quote(os.getenv("FBN_PASSWORD", config["api"]["password"]), '*!')
    client_id = quote(os.getenv("FBN_CLIENT_ID", config["api"]["clientId"]), '*!')
    client_secret = quote(os.getenv("FBN_CLIENT_SECRET", config["api"]["clientSecret"]), '*!')
    api_url = os.getenv("FBN_LUSID_API_URL", config["api"]["apiUrl"])

    token_request_body = ("grant_type=password&username={0}".format(username) +
                          "&password={0}&scope=openid client groups".format(password) +
                          "&client_id={0}&client_secret={1}".format(client_id, client_secret))

    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}

    def get_token():
        okta_response = requests.post(token_url, data=token_request_body, headers=headers)
        if okta_response.status_code != 200:
           lpt.display_error(
              Rec(
                status=okta_response.status_code,
                reason=okta_response.reason,
                code=okta_response.status_code,
                message="OKTA response assertion failed",
                detailed_message=okta_response.text,
                body = okta_response.request.body or "<empty>",
                url = okta_response.request.url,
                items = []
              )
           )
           exit()
 
        return dict(okta_response.json())
        
    credentials = RefreshingTokenAuthentication(get_token)

    return (lusid.LusidTr(credentials, api_url), lusid.models)
