import atws
import atws.monkeypatch.attributes
import base64
import requests, base64
import os
from start_settings import return_start_time



un = os.environ['UN_AUTOTASK']
up = os.environ['UP_AUTOTASK']


at = atws.connect(username=un, password=up, apiversion=1.6, integrationcode='FLVV64YRHYOBF7HNHIVHMXTVOHA')




# For making requests against Autotask ( raw requests - SOAP messages)

at_url="https://webservices19.autotask.net/ATServices/1.6/atws.asmx"




userpass = un+":"+up
encoded_u = base64.b64encode(userpass.encode("ascii")).decode("ascii")
headers_at = {"Authorization" : "Basic %s" % encoded_u} 
headers_at['content-type']= 'text/xml'

# TOPDESK Secrets

user_top_desk = os.environ['UN_TOPDESK']
passw_top_desk = os.environ['UP_TOPDESK']

userpass = user_top_desk+":"+passw_top_desk
encoded_u_td = base64.b64encode(userpass.encode("ascii")).decode("ascii")

td_base_url = "https://nieuwkoop.topdesk.net"
get_headers={'Authorization':"Basic %s" % encoded_u_td}