from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import requests
import json


def make_incident(request="This is the simple request from PQR",action_="Initial action when created by PQR API", brief_descr = 'Brief Description',at_ticket_number="",caller_id = 0,status = ""):
    

    if caller_id == 0:
        caller_id = "24b3bc61-1979-44c8-ad54-d65b8910fb4b" #Pqr API id (used as default one )
    

    
    data_ = {"request" : request,
             "action" : action_,
             "briefDescription":brief_descr,
             "callerLookup" : { "id" : caller_id  }, 
             "operatorGroup" :  {"id" : "7b234055-a0d2-4998-9419-4f7166486371"},
             "externalNumber": at_ticket_number}
    
    if status != "":
        data_["processingStatus"] = { "id" : "8228e2f3-1e1f-4563-a970-51487483e7dc" } # Reactie ontvangen'


    url_incident = "https://nieuwkoop.topdesk.net/tas/api/incidents"
    #headers={'Authorization':"Basic %s" % encoded_u_td}
    r= requests.post(url_incident, data=json.dumps(data_), headers=get_headers )

    return r

def get_all_non_compl_incidents_from_td():
    '''
    Returns all incidents from TopDesk, created by PQR
    '''
       
    url_ = "https://nieuwkoop.topdesk.net/tas/api/incidents?page_size=500&closed=false&operator=7b234055-a0d2-4998-9419-4f7166486371&"
    r= requests.get(url_,headers=get_headers)

    return r

def list_td_ticket_for_counterparts():

    td_incidents = get_all_non_compl_incidents_from_td()

    td_tickets_without_at_counterparts=[]
    
    for ticket in td_incidents.json():
        if ticket['externalNumber']=='':
            td_tickets_without_at_counterparts.append(ticket)
            
    return td_tickets_without_at_counterparts

def get_td_incident(number=''):

    url_incident = "https://nieuwkoop.topdesk.net/tas/api/incidents/number/{}".format(number)
    print(url_incident)
    
    incident = requests.get(url_incident, headers=get_headers)
    
    return incident

