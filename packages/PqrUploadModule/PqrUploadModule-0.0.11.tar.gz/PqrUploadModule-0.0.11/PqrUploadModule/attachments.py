# from . import authorizations

from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import xmltodict
import atws
import atws.monkeypatch.attributes
import pandas as pd
import requests
from suds.sax.text import Raw

# from . import incidents
# from . import tickets

from incidents import get_all_non_compl_incidents_from_td
from tickets import get_list_of_at_tickets

# Autotask attachment functions

def get_all_attachments_for_list_of_ids(id_):
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
    
    response [int]  
    
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
              <Publish xsi:type="xsd:string">1</Publish>
              <Title xsi:type="xsd:string">{}</Title>
              <Type xsi:type="xsd:string">FILE_ATTACHMENT</Type>
            </Info>
            <Data>{}</Data>
          </attachment>
        </CreateAttachment>
      </soap:Body>
    </soap:Envelope>""".format(full_path,ParentID,Title,Data))
    
    response = requests.post(at_url,data=create_attach,headers=headers_at)

    # if response.status_code ==200:
    #     dict1 = xmltodict.parse(at_attachment.text)
    #     at_attachment_id = dict1['soap:Envelope']['soap:Body']['CreateAttachmentResponse']['CreateAttachmentResult']
    #     at_attachment_id = int(at_attachment_id)
    
    # else: 
    #     at_attachment_id == 0

    #     # Perform some logging here!!!!

    return response

def get_at_attachment_content(attachment_id=0):
    '''
    Returns content of Autotask attachment, for givnet attachment_id
    
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
    
    if response.status_code == 200:
        dict1 = xmltodict.parse(response.text)
        
        content_data = dict1['soap:Envelope']['soap:Body']['GetAttachmentResponse']['GetAttachmentResult']['Data']
    
    else:

        content_data = 'No content'



    return content_data




    
#Topdesk attachment functions

def get_incident_attachment(number_):
    '''
    Returns Topdesk incident attachments, for given incident number
    
    Parameters:
    number [str]: Topdesk incident number
    
    Returns:
    Attachment [http response]
    '''
    
    url_incident_attachment = "https://nieuwkoop.topdesk.net/tas/api/incidents/number/{}/attachments".format(number_)
    attachment_ids = requests.get(url_incident_attachment, headers=get_headers)

    if attachment_ids.status_code==200:
        return attachment_ids
    else:
        return 0


    
    """
    Retrieves all AT tickets based on list of AT ticket number list! 
    """
    

    if len(at_ticket_numbers) ==0:
        return 'No AT ticket number list provided'
    
    cleaned_list = at_ticket_numbers
    
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

    

    # here we can call the function to get Autotask tickets from the list 
    
    at_tickets = get_list_of_at_tickets(cleaned_list)

    return attachments, at_tickets


    
    
    
    #check in the TD ids, are in the AT ticket rel_dict
    for ind,ticket in enumerate(at_tickets):

        try:
            rel_dict = ast.literal_eval(ticket.ChangeInfoField2)
            print(rel_dict)
        except:

            rel_dict = {}

            #here we need to create 


        td_ids_in_values = list(rel_dict.values())

        #check
        for atach_ in attachments:

            if list(atach_.keys())[0]==ticket['TicketNumber']:

                td_attachment_id = list(atach_.values())[0]['id']

                if td_attachment_id in td_ids_in_values:
                    print('For this AT ticket: ', ticket['TicketNumber'],'\n')
                    print('TD attachment: ',td_attachment_id,'\n')
                    print('it is already connected')
                else:
                    print('For this AT ticket: ', ticket['TicketNumber'],'\n')
                    print('TD attachment: ',td_attachment_id,'\n')
                    print('make connection')

                    #since this attachment id from TD is not in the rel_dic,

                    # first we need to download attachment, attach it to the AT ticket, 
                    # and than, update rel_dict

                    # extract link to download attachment from TD
                    td_att_downl = base +list(atach_.values())[0]['downloadUrl']

                    file_=requests.get(td_att_downl,headers=get_headers)


                    if file_.status_code ==200: # it means it was successfull.

                        file_binary_content = file_.content

                    else:
                        continue


                    #transform binary date to base64 encoded

                    data_ = base64.encodebytes(file_binary_content).decode('utf-8')

                    #define parameters, to create attachment in AT

                    full_path = list(atach_.values())[0]['fileName']

                    Title = list(atach_.values())[0]['description']

                    ParentID=ticket['id']

                    # make request

                    at_attachment = make_attachment_in_at(full_path=full_path, ParentID=ParentID, Title=Title, Data=data_)


                    if at_attachment.status_code ==200:

                        dict1 = xmltodict.parse(at_attachment.text)

                        at_attachment_id = dict1['soap:Envelope']['soap:Body']['CreateAttachmentResponse']['CreateAttachmentResult']


                    else:

                        continue


                    # Now, when we have at_attachment id, we need to update rel_dict

                    rel_dict[int(at_attachment_id)] = td_attachment_id

                    at_tickets[ind]['ChangeInfoField2'] = str(rel_dict)


    at.update(at_tickets).execute()
    

def get_all_attachments_from_td(): 
    
    '''
    Returns all tuple consisting of: (attachments from TD, list of AT ticket numbers, representing TD counterparts.  
    '''
    td_tickets = get_all_non_compl_incidents_from_td()

    

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
    #these are AT ticket numbers that I need to take, and check their attachments 
    at_ticket_numbers = list(set([list(it.keys())[0] for it in attachments]))
    
    
    cleaned_list = []
    
    for num in at_ticket_numbers:
        if (num[:2] !='T2') | (len(num)<14) | (len(num)==15):
            continue
        else:
            
            cleaned_list.append(num)
            
    
    return attachments, cleaned_list 
    