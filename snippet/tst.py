import simplejson as json
import webbrowser
import httplib2
import re

from apiclient import discovery
from oauth2client import client
from apiclient.discovery import build
from apiclient.discovery import build

class model():

  flow = client.flow_from_clientsecrets(
    '/home/eduardo/Documents/fusion/client/client_secrets.json',
    scope='https://www.googleapis.com/auth/fusiontables',
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

	def __init__(self):
 		  auth_uri = self.step1_get_authorize_url()
  webbrowser.open(auth_uri)



if __name__ == '__main__':

  flow = client.flow_from_clientsecrets(
    '/home/eduardo/Documents/fusion/client/client_secrets.json',
    scope='https://www.googleapis.com/auth/fusiontables',
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

  auth_uri = flow.step1_get_authorize_url()
  webbrowser.open(auth_uri)

  auth_code = raw_input('Enter the auth code: ')

  credentials = flow.step2_exchange(auth_code)
  http_auth = credentials.authorize(httplib2.Http())

  fusion_service = discovery.build('fusiontables', 'v2'	, http_auth)

  json_result = fusion_service.query().sql(sql="SELECT * FROM 19P8oeOLsHiGEfdXv5dm_OU_CJ4A8xPOAvJRKEe9I").execute()
 
  string_result = json.dumps(json_result)

  dic_result = json.loads(string_result)
 	
  print dic_result['rows'].translate

  
