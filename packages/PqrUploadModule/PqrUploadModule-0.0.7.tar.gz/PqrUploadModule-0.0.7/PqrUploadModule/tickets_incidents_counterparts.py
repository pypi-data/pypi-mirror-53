
from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import requests
import json
import pandas as pd

from . import tickets
from . import incidents

from tickets import get_non_compl_tickets
from incidents import get_all_non_compl_incidents_from_td
from incidents import make_incident
from tickets import create_new_ticket_in_at


def list_at_ticket_for_counterparts():

    '''
    Returns all non completed tickets in Autotask (those still open), and filters those that do not have     
    TD counterparts. (Tickets that need to be created in Topdesk)
    
    Parameters:
    None
    
    Returns:
    
    Tuple: (Python DataFrame, list of Autotask tickets for which we need to create counterparts in Topdesk.
    '''

    df,tickets= get_non_compl_tickets()

    # df[df['ChangeInfoField1']!='']
    ids = list(df[df['ChangeInfoField1']==''].id)
    tickets_to_create_in_TD = []
    
    for ticket in tickets:
        if ticket.id in list(ids):
            tickets_to_create_in_TD.append(ticket)       
    df_ = pd.DataFrame([dict(ticket) for ticket in tickets_to_create_in_TD])
     
    return df_, tickets_to_create_in_TD


def create_at_tickets_counterparts():
    '''
    Every ticket in Autotask is connected to Topdesk ticket via field ChangeInfoField1. In ChangeInfoField1, there should
    be Topdesk ticket number.
    
    This function will first check for the Autotask tickets withouth ChangeInfoField1. For these ticket, it will 
    create Topdesk tickets. Upon creation of Topdesk tickets, it will update ChangeInfoField1. That way, relations
    between tickets are mentained. 
    
    Parameters:
    
    None:
    
    Returns:
    
    Messsage [str]: "Tickets updated", if it was successful. "There was an mistake in updateing :" otherwise.   
    ''' 
    _,tickets_to_create_in_TD = list_at_ticket_for_counterparts()
    
    for ind, ticket in enumerate(tickets_to_create_in_TD):
        request=ticket.Title
        at_ticket_number = ticket.TicketNumber
        try:
            brief_descr = ticket.Description     
        except:
            brief_descr="No brief description"
        try:
            r_inc = make_incident(request=request,brief_descr=brief_descr,at_ticket_number=at_ticket_number)
            td_ticket_number=r_inc.json()['number']
            tickets_to_create_in_TD[ind].ChangeInfoField1= td_ticket_number      
        except: 
            continue
    try:
        at.update(tickets_to_create_in_TD).execute()
        
        return ("Tickets updated")
    
    except Exception as e:
        
        return ("There was an mistake in updateing :", e)


def list_td_incidents_for_counterparts():
    td_incidents = get_all_non_compl_incidents_from_td()

    td_tickets_without_at_counterparts=[]
    
    


    for ticket in td_incidents.json():
        if ticket['externalNumber']=='':
            td_tickets_without_at_counterparts.append(ticket)
            
    return td_tickets_without_at_counterparts


def create_td_tickets_counterparts():
    
    
    ticket_to_be_updated=list_td_ticket_for_counterparts()


    number=0
    for ticket in ticket_to_be_updated:
        
       
        try:
            # we take few infos about the ticket in TD, and create new ticket with ChangeInfoField1= TD number
            
            # define title 
            
            if ticket['briefDescription'][:254]=='':
                ticket['briefDescription'] = "No brief description"
                
            title= ticket['briefDescription'][:254]

            descr = ticket['request'][:7900]

            ChangeInfoField1 = ticket['number']

            #Here we create new ticket in AT, with reference to TD
            at_ticket = create_new_ticket_in_at(title=title,descr=descr,ChangeInfoField1=ChangeInfoField1)

            #now we need to write 'external number' in TD ticket (reflecting AT id)
            ticket["externalNumber"] =at_ticket.TicketNumber

            #here we need to perfom updating ticket in TD 

            # address for updateing tickets: 

            url_ = "https://nieuwkoop.topdesk.net/tas/api/incidents/id/{}".format(ticket["id"])

            body_={'externalNumber': str(at_ticket.TicketNumber)}

            r=requests.put(url=url_,data=json.dumps(body_), headers=get_headers) 

            
        except:
            
            number=+1
            continue
        
        
        return number


def create_counterparts():
    
    """
    This is the key function for checking both system for tickets without counterparts.
    In the case it finds such tickets, this function will create their counterparts, thus synchronising
    both systems.
    
    """

    try: 
        
        create_td_tickets_counterparts()
        
        create_at_tickets_counterparts()
        
        
        return 'All counterparts created successfully '
        
        
    except:
        
        return 'There was an error in making counterparts'
        

