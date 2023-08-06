from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws
import atws.monkeypatch.attributes
import pandas as pd
import requests
import datetime
import xmltodict

def get_non_compl_tickets(account_id=294):
    """
    Retrieves non closed tickets, belonging to the account_id.( excluding tickets that belong to the Queues: 
    QueueID = [29683485,29683487]
      
    Parameters:
    
    account_id [int]: Autotask AccountID
    
    Returns:
    
    Tuple: (Python DataFrame, list of tickets)
    """

    

    # checking_date = datetime.datetime.now()-datetime.timedelta(2)


    query_non_compl_tickets=atws.Query('Ticket')
    query_non_compl_tickets.WHERE('AccountID',query_non_compl_tickets.Equals,account_id)
    query_non_compl_tickets.AND("Status",query_non_compl_tickets.NotEqual,at.picklist['Ticket']['Status']['Complete'])
    query_non_compl_tickets.AND("QueueID",query_non_compl_tickets.NotEqual,29683485)
    query_non_compl_tickets.AND("QueueID",query_non_compl_tickets.NotEqual,29683487)
    # query_non_compl_tickets.AND('LastActivityDate',query_non_compl_tickets.GreaterThanorEquals,checking_date)
    tickets = at.query(query_non_compl_tickets).fetch_all()
    df = pd.DataFrame([dict(ticket) for ticket in tickets])
    
    return df,tickets

def create_new_ticket_in_at(title='Ticket Title',descr = 'Short description', account_id = 294,Reference_NWK="No",status="",contact_id = 0):

    '''
    Creates new ticket in AUTOTASK.
    
    Parameters:
    
    title (str): Title of Autotask ticket
    descr (str): Short description of ticket
    account_id (int): Autotask AccountID, to which we assign the new ticket
    
    ChangeInfoField1 (str): Do not use this parameter /it is used when the function is called from automatic code
    Returns:
    
    Autotask ticket.
    '''

    ticket = at.new('Ticket')

    if contact_id != 0:
        try:
            ticket.ContactID = contact_id
        except:
            pass
    #there is still open question about CONTRACTS!!!??

    ticket.Title = title
    ticket.Description = descr
    ticket.AccountID = account_id

    ticket.set_udf('Reference_NWK',Reference_NWK)
    # ticket.ChangeInfoField1 = ChangeInfoField1
    # ticket.DueDateTime = datetime.datetime.now()
    ticket.Priority = at.picklist['Ticket']['Priority']['(P3) Normaal']

    if status == "":
        ticket.Status = at.picklist['Ticket']['Status']['New']
    else:
        ticket.Status = at.picklist['Ticket']['Status']['Customer Note Added']
        
    ticket.QueueID = at.picklist['Ticket']['QueueID']['1e lijns Service Team']
    ticket.create()
    
    return ticket


def get_at_ticket(id_=0):

    '''
    Returns Autotask ticket, for given id number.
    
    Parameters:
    
    id_ [int]: Autotask TicketID
    
    Returns:
    
    ticket [Autotask ticket]
    '''
    query_non_compl_tickets=atws.Query('Ticket')
    query_non_compl_tickets.WHERE('id',query_non_compl_tickets.Equals,id_)
    ticket = at.query(query_non_compl_tickets).fetch_all()
    
    return ticket


# get the Autotask ticket list, based on list of AT ticket numbers

def get_list_of_at_tickets(at_ticket_numbers=[]):
    
    """
    Retrieves all AT tickets based on list of AT ticket number list! 
    """
    
    
    if len(at_ticket_numbers) ==0:
        return 'No AT ticket number list provided'
    
    cleaned_list = []
    
    for num in at_ticket_numbers:
        if (num[:2] !='T2') | (len(num)==15) | (len(num)<14):
            continue
        else:
            
            cleaned_list.append(num)
            
            
    
    

    query_non_compl_tickets=atws.Query('Ticket')


    if len(cleaned_list) == 0:
        return 'Nothing to process'

    if len(cleaned_list) == 1:

        query_non_compl_tickets.WHERE('TicketNumber',query_non_compl_tickets.Equals,cleaned_list[0])
    
    else:
        
        
        query_non_compl_tickets.WHERE('TicketNumber',query_non_compl_tickets.Equals,cleaned_list[0])

        for number in cleaned_list[1:]:
            query_non_compl_tickets.OR('TicketNumber',query_non_compl_tickets.Equals,number)



    tickets = at.query(query_non_compl_tickets).fetch_all()
    
    df = pd.DataFrame([dict(ticket) for ticket in tickets])
    
    return df,tickets

def get_ticket_for_ticket_number(ticket_number):
    query_non_compl_tickets=atws.Query('Ticket')
    query_non_compl_tickets.WHERE('TicketNumber',query_non_compl_tickets.Equals,ticket_number)
    ticket = at.query(query_non_compl_tickets).fetch_one()

    return ticket