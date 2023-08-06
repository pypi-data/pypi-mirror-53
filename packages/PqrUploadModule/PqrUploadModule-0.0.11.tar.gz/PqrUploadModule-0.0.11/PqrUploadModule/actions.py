from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws
import atws.monkeypatch.attributes
import pandas as pd
import requests

# from . import incidents
# from incidents import get_all_non_compl_incidents_from_td


def get_all_actions_from_td():
    
    
    r=get_all_non_compl_incidents_from_td()

    if r.status_code!=200:
        return 'Error in getting actions from Topdesk'
    else:

        action_list = []

        for incident in r.json():
            incident_number = incident['number']
            
            ticket_number = incident['externalNumber']
            
            act_url = td_base_url + "/tas/api/incidents/number/{}/actions".format(incident_number)
            incident_actions = requests.get(act_url, headers=get_headers)
            
            if incident_actions.status_code==200:
                if incident_actions.status_code==200:
                    for action in incident_actions.json():
                        ss = {ticket_number : action}

                        action_list.append(ss)

                else:
                    continue
            else:
                continue

        at_ticket_numbers = list(set([list(it.keys())[0] for it in action_list]))

        cleaned_list = []
    
        for num in at_ticket_numbers:
            if num[:2] !='T2' or len(num)>14:
                continue
            else:

                cleaned_list.append(num)

    return action_list, cleaned_list


def get_actions_for_incident_number(number=""):
    url_ = td_base_url + "/tas/api/incidents/number/{}/actions".format(number)

    r=requests.get(url_,headers=get_headers)

    if r.status_code==200:
        return r.json()

    else:
        return 'no actions'