import os
from msrest.authentication import Authentication
import lusidtr

class CertificateAuthentication(Authentication):

    cert_path = None

    def __init__(self, cert_path):
        self.cert_path = cert_path

    def signed_session(self):
        session = super(CertificateAuthentication, self).signed_session()
        session.cert = self.cert_path
        return session


def connect(config,**kwargs):
        api_url = os.getenv("FBN_LUSID_API_URL", config["api"]["apiUrl"])

        user_id = os.getenv("FBN_REFINITIV_USER_ID", config.get("user"))

        certificate = os.getenv("FBN_TR_CERTIFICATE", config.get("cert"))

        custom_headers={"x-tr-uuid":user_id} if user_id else None
        credentials = CertificateAuthentication(certificate)

        return (lusidtr.LusidTr(credentials, api_url), lusidtr.models, custom_headers)
