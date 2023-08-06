# Here is the list of modules we need to import
import atws
import atws.monkeypatch.attributes
import pandas as pd
import numpy as np
import datetime
import binascii
import base64
import requests, base64
import imageio
import os
import ast
import io
import pytz
import suds
import xmltodict
from requests.auth import HTTPBasicAuth
from suds.sax.text import Raw
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder



########################################################################################################
########################################################################################################
# un = "rapportage_api@PQRSB82219.NL"
# up='vyHPa57nuRqZ5LfqWTza'

un = os.environ['UN_AUTOTASK']
up = os.environ['UP_AUTOTASK']



at = atws.connect(username=un,password=up,apiversion=1.6,
                  support_file_path='/Users/Petar.Jovanovic/documents/pqrprojects/autotask/AutotaskAPI',
                  integrationcode='FLVV64YRHYOBF7HNHIVHMXTVOHA')




# For making requests against Autotask ( raw requests - SOAP messages)

at_url="https://webservices19.autotask.net/ATServices/1.6/atws.asmx"

userpass = un+":"+up
encoded_u = base64.b64encode(userpass.encode("ascii")).decode("ascii")
headers_at = {"Authorization" : "Basic %s" % encoded_u} 
headers_at['content-type']= 'text/xml'


#Here we prepare what we need for making TOPDESK requests


# user_top_desk = "PQR"
# passw_top_desk = "yzlno-4uz4d-cgenx-vqncz-uqpso"

user_top_desk = os.environ['UN_TOPDESK']
passw_top_desk = os.environ['UP_TOPDESK']

userpass = user_top_desk+":"+passw_top_desk
encoded_u_td = base64.b64encode(userpass.encode("ascii")).decode("ascii")

td_base_url = "https://nieuwkoop.topdesk.net"
get_headers={'Authorization':"Basic %s" % encoded_u_td}

# #########################################################################################################
###########################################################################################################

# Query TicketNotes

def get_ticket_notes_at(id_=[0],at=at):
    """
    Returns all notes, belonging to the tickets from the given list. 
    
    Parameters:
    
    id_ [list]: list of Autotask ticket ids
    at [Autotask connect object] : Autotask atws.connect object
    Returns:
    
    Tuple: (Python DataFrame, list of notes) 
    """

    query_notes=atws.Query('TicketNote')
    
    if len(id_)==1:
        query_notes.WHERE('TicketID',query_notes.Equals,id_[0])
    else:
        query_notes.WHERE('TicketID',query_notes.Equals,id_[0])
        for element in id_:
            query_notes.OR('TicketID',query_notes.Equals,element)
    notes = at.query(query_notes).fetch_all()
    df = pd.DataFrame([dict(note) for note in notes])

    return df,notes


# Query all  'not sompleted' tickets from 294

def get_non_compl_tickets(account_id=294):
    """
    Retrieves non closed tickets, belonging to the account_id.( excluding tickets that belong to the Queues: 
    QueueID = [29683485,29683487]
      
    Parameters:
    
    account_id [int]: Autotask AccountID
    
    Returns:
    
    Tuple: (Python DataFrame, list of tickets)
    """
    query_non_compl_tickets=atws.Query('Ticket')
    query_non_compl_tickets.WHERE('AccountID',query_non_compl_tickets.Equals,account_id)
    query_non_compl_tickets.AND("Status",query_non_compl_tickets.NotEqual,at.picklist['Ticket']['Status']['Complete'])
    query_non_compl_tickets.AND("QueueID",query_non_compl_tickets.NotEqual,29683485)
    query_non_compl_tickets.AND("QueueID",query_non_compl_tickets.NotEqual,29683487)
    tickets = at.query(query_non_compl_tickets).fetch_all()
    df = pd.DataFrame([dict(ticket) for ticket in tickets])
    
    return df,tickets


def get_all_attachments_for_list_of_ids(id_=[0]):
    '''
    Returns all Autotask attachments, belonging to the tickets in the given list of ids.
    
    Parameters:
    
    id_ [list] : List of Autotask ticket ids, for which we want to retrieve attachments
    
    Returns:
    
    Tuple: (Python DataFrame, list of attachments)
    '''
    attachmentInfo = atws.Query('AttachmentInfo')
    if len(id_)==1:
        attachmentInfo.WHERE('ParentID',attachmentInfo.Equals,id_[0])   
    else:
        attachmentInfo.WHERE('ParentID',attachmentInfo.Equals,id_[0])
        for element in id_[1:]:
            attachmentInfo.OR('ParentID',attachmentInfo.Equals,element)
    attachments = at.query(attachmentInfo).fetch_all()
    df = pd.DataFrame([dict(att) for att in attachments])
    return df,attachments


def make_attachment_in_at(full_path='full_path',ParentID='ParentID',Title='Title',Data='Data'):
    '''
    Creates Attachment in Autotask ticket, defined by ParentID parameter
    
    Parameters:
    
    full_path [str]: full_path, in the case that attachment is somwhere on the web.
    
    ParentID [int]: Autotask TicketID, to which we assign new attachment.
    
    Title [str]: Title of attachment
    
    Data [base64.encodebytes(data).decode('utf-8')] : base64 encoded binary data (data is binary content of attachment)
    
    Returns:
    
    response [http response]  
    
    '''

    create_attach = Raw("""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <soap:Header>
        <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
          <IntegrationCode>FLVV64YRHYOBF7HNHIVHMXTVOHA</IntegrationCode>
        </AutotaskIntegrations>
      </soap:Header>
      <soap:Body>
        <CreateAttachment xmlns="http://autotask.net/ATWS/v1_6/">
          <attachment>
            <Info>
              <FullPath xsi:type="xsd:string">{}</FullPath>
              <ParentID xsi:type="xsd:string">{}</ParentID>
              <ParentType xsi:type="xsd:string">4</ParentType>
              <Publish xsi:type="xsd:string">2</Publish>
              <Title xsi:type="xsd:string">{}</Title>
              <Type xsi:type="xsd:string">FILE_ATTACHMENT</Type>
            </Info>
            <Data>{}</Data>
          </attachment>
        </CreateAttachment>
      </soap:Body>
    </soap:Envelope>""".format(full_path,ParentID,Title,Data))
    
    response = requests.post(at_url,data=create_attach,headers=headers_at)

    if response.status_code ==200:
        dict1 = xmltodict.parse(at_attachment.text)
        at_attachment_id = dict1['soap:Envelope']['soap:Body']['CreateAttachmentResponse']['CreateAttachmentResult']
    
    else: 
        at_attachment_id = 'Attachment was not created'

    return at_attachment_id


def get_attachment_content(attachment_id=0):
    '''
    Returns content of attachment, for givnet attachment_id
    
    Parameters:
    
    attachment_id [int]: Autotask AttachmentID, 
    
    Returns: 
    Attachment content (base64 string)   
    '''
    
    get_attachment = Raw("""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soap:Header>
            <AutotaskIntegrations xmlns="http://autotask.net/ATWS/v1_6/">
                <IntegrationCode>FLVV64YRHYOBF7HNHIVHMXTVOHA</IntegrationCode>
            </AutotaskIntegrations>
        </soap:Header>
        <soap:Body>
            <GetAttachment xmlns="http://autotask.net/ATWS/v1_6/">
                <attachmentId>{}</attachmentId>
            </GetAttachment>
        </soap:Body>
    </soap:Envelope>""".format(attachment_id))
    
    response = requests.post(at_url,data=get_attachment,headers=headers_at)
    dict1 = xmltodict.parse(response.text)
    
    content_data = dict1['soap:Envelope']['soap:Body']['GetAttachmentResponse']['GetAttachmentResult']['Data']
    
    return content_data



def create_new_ticket_in_at(title='Ticket Title',descr = 'Short description', account_id = 294,ChangeInfoField1=""):
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
    ticket.Title = title
    ticket.Description = descr
    ticket.AccountID = account_id
    ticket.ChangeInfoField1 = ChangeInfoField1
    ticket.DueDateTime = datetime.datetime.now()
    ticket.Priority = at.picklist['Ticket']['Priority']['(P3) Normaal']
    ticket.Status = at.picklist['Ticket']['Status']['New']
    ticket.QueueID = at.picklist['Ticket']['QueueID']['1e lijns Service Team']
    ticket.create()
    
    return ticket


def list_at_ticket_for_counterparts():
    '''
    Returns all non completed tickets in Autotask (those still open), and filters those that do not have     
    TD counterparts. (Tickets that need to be created in Topdesk)
    
    Parameters:
    
    None
    
    Returns:
    
    Tuple: (Python DataFrame, list of Autotask tickets.
    '''
    df,tickets= get_non_compl_tickets()
    df[df['ChangeInfoField1']!='']
    ids = df[df['ChangeInfoField1']==''].id
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


def add_attachment_ids_to_dict():
    '''
    Story:
    Every attachment is assigned to ticket. This function will itterate over Autotask tickets, list attachments 
    for each, and update relation dictionary at field: ChangeInfoField2. 
    '''
    # get all non completed tickets from Autotask
    df_,tickets =get_non_compl_tickets()
    #now we extract list of ids of interested_tickets.we need this list to get all attachments
    tickets_ids_for_attachment_check = list(df_.id)
    df_attach , at_attachments = get_all_attachments_for_list_of_ids(tickets_ids_for_attachment_check)
    list_of_ticket_ids = list(df_attach.ParentID.unique())

    tickets_to_update = []

    for ticket in tickets:
        if ticket.id in list_of_ticket_ids:
            attachment_ids = list(df_attach[df_attach.ParentID==ticket.id].id)
        else:
            continue


    #now, we need to check if there is a dictionary in ChangeInfoField2. If there is not, we need to create one.
    # dictionary will have attachment_ids as keys, and '' as values. 

    #if there is, we need to check if all attachment_ids are in its keys. 

    # If all attachment_ids are in keys, we do continue. If not, we need to add them to the dictionary 

        if ticket.ChangeInfoField2 =='':
            #if this field is empty, we need to create dictionary
            attachm_dict = {}
            for id_ in attachment_ids:
                attachm_dict[id_] = ''
            ticket.ChangeInfoField2 = str(attachm_dict)
            tickets_to_update.append(ticket)
        else:
            #First extract existing dictionary, with its keys and values
            attachm_dict = ast.literal_eval(ticket.ChangeInfoField2)
            #make a set of its keys:
            already_existing_keys = set(attachm_dict.keys())
            set_of_new_keys = set(attachment_ids)
            #keys to add to dictionary:
            keys_to_add = list(set_of_new_keys -already_existing_keys)

            for id_ in keys_to_add:
                attachm_dict[id_] = ''

            #Now we make string representation of  attachm_dict, and save it to the   ChangeInfoField2
            ticket.ChangeInfoField2 = str(attachm_dict)
            tickets_to_update.append(ticket)

    if len(tickets_to_update) !=0:
        try:
            at.update(tickets_to_update).execute()
            return 'Relation dictionaries updated'
        except ExceptionValue as e:
            
            return 'Error during rel_dicts updating: ',e
    else:
        
        return 'Relation dictionaries are already up to date'
    
    
def make_at_attachments_counterparts():
    
    df_,tickets =get_non_compl_tickets()

    #now we extract list of ids of interested_tickets.we need this list to get all attachments
    tickets_ids_for_attachment_check = list(df_.id)
    df_attach , at_attachments = get_all_attachments_for_list_of_ids(tickets_ids_for_attachment_check)
    list_of_ticket_ids = list(df_attach.ParentID.unique())
    at_tickets_to_update = []

    for ind,ticket in enumerate(tickets):
        #Find related incident number in TD
        related_incident_number= ticket.ChangeInfoField1
        if ticket.ChangeInfoField2 == '':
            continue 
        else:    
            attachm_dict = ast.literal_eval(ticket.ChangeInfoField2)
        
        non_rel_attachments_ids = []
        
        for k, v in attachm_dict.items():
            if (v=='') | (v[:3]=='err'):
                non_rel_attachments_ids.append(k)
                
        for att_id in non_rel_attachments_ids:
            # print('Here I am',att_id)
            # first we need to 'download' the content of the attachment from AT 
            content_of_att_id=get_attachment_content(att_id)
            #here we create content for TD incident attachment
            cont_binary = base64.decodebytes(content_of_att_id.encode())
            f = io.BytesIO(cont_binary).read()

            Descr = df_attach[df_attach.id==att_id].Title.values[0]
            ContentType = df_attach[df_attach.id==att_id].ContentType.values[0]
            File_name = df_attach[df_attach.id==att_id].FullPath.values[0]
            
            files={'file': (File_name, f,"multipart/form-data")}

            url_='https://nieuwkoop.topdesk.net/tas/api/incidents/number/{}/attachments'.format(related_incident_number)

            inc_attachment = requests.post(url_,files=files, headers={'Authorization':"Basic %s" % encoded_u_td})

            if inc_attachment.status_code!=200:
                attachm_dict[att_id] = "error" + " " + ContentType
                tickets[ind].ChangeInfoField2 = str(attachm_dict)
                at_tickets_to_update.append(tickets[ind])
            else:
                #update dictionary in AT, and make reference with TD attachment id
                attachm_dict[att_id] = inc_attachment.json()["id"]
                tickets[ind].ChangeInfoField2 = str(attachm_dict)
                at_tickets_to_update.append(tickets[ind])

        # After we have itterate over all attahments, and after we updated relation dictionary in AT, 
        # we need to update tickets.(Only those with changed relation dictionary)
        # THINK ABOUT POSITION OF THIS LINE at.update(tickets[ind])

 
    # After we itterate through all ticket, we update those with update rel.dict:
    
    if len(at_tickets_to_update) == 0:
        return 'Nothing to update'
    
    else:
        
        try:
            at.update(at_tickets_to_update).execute()

            return at_tickets_to_update

        except:
            
            return 'Rel.dicts were not updated'
        
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
    
def get_td_incident(number=0):
    '''
    Returns Topdesk incident, for incident number given.
    
    Parameters:
    
    number [str]: Topdesk incident number
    
    Return:
    incident [http response]:
    '''
    url_incident = "https://nieuwkoop.topdesk.net/tas/api/incidents/number/{}".format(number)
    incident = requests.get(url_incident, headers={'Authorization':"Basic %s" % encoded_u_td})

    return incident

def get_incident_attachment(number_):
    '''
    Returns Topdesk incident, for given incident number
    
    Parameters:
    number [str]: Topdesk incident number
    
    Returns:
    Attachment [http response]
    '''
    
    url_incident_attachment = "https://nieuwkoop.topdesk.net/tas/api/incidents/number/{}/attachments".format(number_)
    attachment_ids = requests.get(url_incident_attachment, headers={'Authorization':"Basic %s" % encoded_u_td})


    return attachment_ids

def get_all_attachments_from_td(): 
    
    '''
    Returns all attachments from Topdesk, that belong to non closed incidents for PQR.
    
    Parameters:
    None
    
    Returns:
    
    Tuple: ( list of Topdesk attachments, list of Autotask ticket numbers - counterpart tickets for attachments)  
    '''
    
    td_tickets = get_all_non_compl_incidents_from_td()
    td_tickets.json()[:1]
    attachments = []

    for td_ticket in td_tickets.json():
        external_number = td_ticket['externalNumber']
        attachments_link = td_base_url+td_ticket['attachments']
        r= requests.get(attachments_link,headers=get_headers)

        if r.status_code==204:
            continue

        if r.status_code ==200:
            for at1 in r.json():
                ss = {external_number : at1}
                attachments.append(ss) 
        else:
            continue
            
    if len(attachments) != 0:
        #these are AT ticket numbers that I need to take, and check their attachments 
        at_ticket_numbers = list(set([list(it.keys())[0] for it in attachments]))
    else:
        at_ticket_numbers = []
        
    cleaned_list = []
    
    for num in at_ticket_numbers:
        if num[:2] !='T2':
            continue
        else:
            cleaned_list.append(num)
    
    return attachments, cleaned_list
    
   
    
