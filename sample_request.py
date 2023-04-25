import requests
import netsuite_oath as auth

HTTP_METHOD = "GET"
LIMIT = 1000
OFFSET = 0

BASE_URL = "https://<Account ID>.suitetalk.api.netsuite.com/services/rest/record/v1/salesorder" # this works
BASE_URL = f"https://<Account ID>.suitetalk.api.netsuite.com/services/rest/record/v1/salesorder?offset={OFFSET}&limit={LIMIT}"
# the latter url fails.. i get invalid login credentials.. but if i use postman it works perfectly..


# Make initial request to get the first batch of sales orders
response = requests.request(HTTP_METHOD, BASE_URL, headers=auth.createHeader(HTTP_METHOD, BASE_URL))
data = response.json()
data_dict = dict(data)

print(data_dict)