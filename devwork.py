import requests
import json
import urllib3
import re
import time
def get_auth_token():
    global url1
    https = "https://"
    url1 = input('enter IP of DSS Slave:\n')
    url2 = "/secretssafe/api/v1/connect/token/internal"
    url = https + url1 + url2
    username= input('name\n')
    password= input('Password\n')
    payload = "{\"username\":\"%s\",\"password\":\"%s\"}" '' %(username,password)
    headers = {
  'accept': 'text/plain',
  'Content-Type': 'application/json'
}
    r = requests.request("POST", url,headers=headers,data=payload, verify=False)
    json_data=r.json()
    global tokenclean
    for x in json_data :
        token = []
        format = json_data['access_token']
        tokenclean= re.sub(r'\(\d*\D+\d*\)\s+','',re.sub(r'\{.+?\#(\d+)\.\d+\)}',r'(\1)',format))
get_auth_token()
def create_app():
    global clean
    """create application in DSS -- retrieve API KEY """
    https = "https://"
    url2 = "/secretssafe/api/v1/principal/internal/application"
    url = https + url1 + url2
    payload =  "{\"name\":\"acmeapp\"}"
    headers = {
'Accept':'*/*',
'Authorization':"Bearer " + tokenclean,
'Content-Type': 'application/json'
}
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response)
    response1=response.json()
    for key in response1:
        appkey=[]
        mykey=response1['ApiKey']
        clean= re.sub(r'\(\d*\D+\d*\)\s+','',re.sub(r'\{.+?\#(\d+)\.\d+\)}',r'(\1)',mykey))
create_app()

def create_secret():
    """Create Secret for my Application """
    https = "https://"
    url2 = "/secretssafe/api/v1/secret/secret%2Ftest1%3Atest1"
    url = https + url1 + url2
    payload = "testmysecret"
    headers = {
  'accept': '*/*',
  'Authorization':"Bearer " + tokenclean,
  'Content-Type': 'text/plain'
}

    responsesecret = requests.request("POST", url, headers=headers, data = payload, verify=False)
create_secret()
def allow_secret():
    """Allow Secret for my Application """
    """Wait for 5 seconds"""
    time.sleep(5)
    global applicationname
    https = "https://"
    url2 = "/secretssafe/api/v1/authorize"
    url = https + url1 + url2
    payload = "{\"principalUri\":\"/principal/internal/application/acmeapp\",\"resourceUri\":\"secret/secret/test1:test1\",\"operations\":[\"read\"],\"access\":\"allow\"}"
    headers = {
  'accept': '*/*',
  'Authorization':"Bearer " + tokenclean,
  'Content-Type': 'application/json'
}

    responseallow = requests.request("POST", url, headers=headers, data = payload, verify=False)
    responseallow1=responseallow.json()

    print(responseallow1)
    print("API KEY FOR APP", clean)
allow_secret()
def login_app():
    global clean
    https = "https://"
    url2 = "/secretssafe/api/v1/connect/api_key_token"
    url = https + url1 + url2
    payload = "{\"application_name\":\"acmeapp\",\"api_key\":\"%s\"}"''%(clean)
    headers = {
  'accept': 'text/plain',
  'Authorization':"Bearer " + tokenclean,
  'Content-Type': 'application/json'
}
    response_p = requests.request("POST", url, headers=headers, data = payload, verify=False)
    print("login request",response_p.status_code)
login_app()
def get_my_secret():
    time.sleep(3)
    https = "https://"
    url2 = "/secretssafe/api/v1/secret/secret%2Ftest1%3Atest1?verbose=true&depth=1&page_size=50&page_number=1"
    url = https + url1 + url2
    payload = {}
    headers = {
  'accept': '*/*',
  'Authorization':"Bearer " + tokenclean,
}
    response_secret = requests.request("GET", url, headers=headers, data = payload, verify=False)
    print(response_secret.text.encode('utf-8'))
get_my_secret()
