import math
import random
import urllib.parse
import base64
import hmac
import hashlib
import time


# Authentication Credentials
NETSUITE_ACCOUNT_ID = "XXXXXXX"
CONSUMER_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CONSUMER_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TOKEN_ID = "7XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TOKEN_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

SIGN_METHOD = "HMAC-SHA256"
# HTTP_METHOD = "POST"  # used with suiteql querying...
OAUTH_VERSION = "1.0"

# In case of SuiteSQL, base url: https://<ACCOUNT_ID>.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql
# BASE_URL = "https://<Account ID>.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"  # while using suiteql querying


# function to generate a cryptographic nonce for NetSuite
def getAuthNonce():
    nonce_text = ""
    length = 11
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(length):
        nonce_text += possible[math.floor(random.uniform(0, 1) * len(possible))]

    return nonce_text


def getSignature(BASE_URL, HTTP_METHOD, OAUTH_NONCE, TIME_STAMP):
    data = 'oauth_consumer_key' + "=" + CONSUMER_KEY + "&"
    data += 'oauth_nonce' + "=" + OAUTH_NONCE + "&"
    data += 'oauth_signature_method' + "=" + SIGN_METHOD + "&"
    data += 'oauth_timestamp' + "=" + str(TIME_STAMP) + "&"
    data += 'oauth_token' + "=" + TOKEN_ID + "&"
    data += 'oauth_version' + "=" + OAUTH_VERSION

    signatureValue = HTTP_METHOD + '&' + urllib.parse.quote(BASE_URL, safe='~()*!.\'') + '&' + urllib.parse.quote(data,
                                                                                                               safe='~()*!.\'')
    signatureKey = urllib.parse.quote(CONSUMER_SECRET, safe='~()*!.\'') + '&' + urllib.parse.quote(TOKEN_SECRET,
                                                                                                safe='~()*!.\'')
    signatureValue = bytes(signatureValue, 'utf-8')
    signatureKey = bytes(signatureKey, 'utf-8')
    shaData = hmac.new(signatureKey, signatureValue, digestmod=hashlib.sha256).digest()

    base64EncodedData = base64.b64encode(shaData)
    oauth_signature = base64EncodedData.decode('utf-8')
    oauth_signature = urllib.parse.quote(oauth_signature, safe='~()*!.\'')

    return oauth_signature


# Function to generate header
def createHeader(HTTP_METHOD, BASE_URL):
    OAUTH_NONCE = getAuthNonce()
    TIME_STAMP = round(time.time())

    oauth_signature = getSignature(BASE_URL, HTTP_METHOD, OAUTH_NONCE, TIME_STAMP)
    OAuthHeader = 'OAuth '
    OAuthHeader += 'realm="' + NETSUITE_ACCOUNT_ID + '",'
    OAuthHeader += 'oauth_token="' + TOKEN_ID + '",'
    OAuthHeader += 'oauth_consumer_key="' + CONSUMER_KEY + '",'
    OAuthHeader += 'oauth_nonce="' + OAUTH_NONCE + '",'
    OAuthHeader += 'oauth_timestamp="' + str(TIME_STAMP) + '",'
    OAuthHeader += 'oauth_signature_method="' + SIGN_METHOD + '",'
    OAuthHeader += 'oauth_version="1.0",'
    OAuthHeader += 'oauth_signature="' + oauth_signature + '"'

    headers = {
     "Authorization": OAuthHeader,
     "prefer": "transient",
     "Cookie": "NS_ROUTING_VERSION=LAGGING"
    }

    return headers