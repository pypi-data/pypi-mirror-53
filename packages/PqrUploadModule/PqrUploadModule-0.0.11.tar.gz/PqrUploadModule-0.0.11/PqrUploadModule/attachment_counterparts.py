# from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import ast
import requests
import base64
from attachments import make_attachment_in_at
import xmltodict
import io
import pandas as pd 
from suds.sax.text import Raw

# from . import tickets
# from . import attachments 

from tickets import get_non_compl_tickets
from attachments import get_all_attachments_for_list_of_ids
from tickets import get_list_of_at_tickets
from attachments import get_all_attachments_from_td
from attachments import get_at_attachment_content

def add_attachment_ids_to_dict():
    #First get the list of all non completed tickets from Autotask

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
            if len(keys_to_add) == 0:
                continue

            ticket.ChangeInfoField2 = str(attachm_dict)
            tickets_to_update.append(ticket)

    if len(tickets_to_update) == 0:
        print ('Nothing to update')

    else:
        try:
            at.update(tickets_to_update).execute()
            print( 'Relation dictionaries updated successfully')
        except:
            print ('There was an error in updating relation dictionaries')



    

    attachments,at_tickets = get_all_attachments_from_td()

    df_tickets , at_tickets1 = get_list_of_at_tickets(at_tickets)
    
    #check in the TD ids, are in the AT ticket rel_dict
    for ind,ticket in enumerate(at_tickets1):

        tickets_to_update1 = []

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
                    print('')
                    # print('For this AT ticket: ', ticket['TicketNumber'],'\n')
                    # print('TD attachment: ',td_attachment_id,'\n')
                    # print('it is already connected')
                else:
                    # print('For this AT ticket: ', ticket['TicketNumber'],'\n')
                    # print('TD attachment: ',td_attachment_id,'\n')
                    # print('make connection')

                    #since this attachment id from TD is not in the rel_dic,

                    # first we need to download attachment, attach it to the AT ticket, 
                    # and than, update rel_dict

                    # extract link to download attachment from TD
                    td_att_downl = td_base_url +list(atach_.values())[0]['downloadUrl']

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

                    at_tickets1[ind]['ChangeInfoField2'] = str(rel_dict)

                    tickets_to_update1.append(at_tickets1[ind])

    try:
        at.update(tickets_to_update1).execute()
        return 'Successfully created Topdes counterparts attachments'
    except:

        return 'There was an arror in updating at tickets'
    

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
            content_of_att_id=get_at_attachment_content(att_id)
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


    
    if len(at_tickets_to_update) == 0:
        return 'Nothing to update'
    
    else:
        
        try:
            at.update(at_tickets_to_update).execute()

            return at_tickets_to_update

        except:
            
            return 'Rel.dicts were not updated'


def make_td_attachments_counterparts():
    
    attachments, cleaned_list = get_all_attachments_from_td()

    df_, at_tickets = get_list_of_at_tickets(cleaned_list)
    
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

            if list(atach_.keys())[0]==ticket.TicketNumber:

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
    
