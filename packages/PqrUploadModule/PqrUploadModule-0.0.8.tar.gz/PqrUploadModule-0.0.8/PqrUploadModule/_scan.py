
from . import authorizations

from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws
import atws.monkeypatch.attributes
import pandas as pd
import requests
import datetime
import xmltodict
import datetime
import json
import ast
import base64
import io
import logging
import re


from . import start_settings
from . import tickets
from . import attachments
from . import incidents
from .import notes
from . import contacts


from start_settings import return_start_time
from tickets import create_new_ticket_in_at, get_list_of_at_tickets
from tickets import get_non_compl_tickets as get_all_open_tickets
from attachments import make_attachment_in_at,get_at_attachment_content
from incidents import make_incident
from incidents import get_all_non_compl_incidents_from_td as get_all_open_incidents
from notes import get_ticket_notes_at,make_note_in_at,get_notes_for_list_of_note_ids
from contacts import get_contact_id_for_extID, get_contact_extID_for_id

from tickets import get_non_compl_tickets as get_all_open_tickets
from incidents import get_all_non_compl_incidents_from_td as get_all_open_incidents
from incidents import get_all_non_compl_incidents_from_td 



class HelpScan():

                
    def get_all_non_compl_tickets_from_at(self):

        """
        Retrieves non closed tickets, belonging to the account_id.( excluding tickets that belong to the Queues: 
        QueueID = [29683485,29683487]
        
        Parameters:
        
        account_id [int]: Autotask AccountID
        
        Returns:
        
        Tuple: (Python DataFrame, list of tickets)
        """
      
        account_id = self.account_id

        checking_date =  self.start_time  #datetime.datetime.now()-datetime.timedelta(2)


        query_non_compl_tickets=atws.Query('Ticket')
        query_non_compl_tickets.WHERE('AccountID',query_non_compl_tickets.Equals,account_id)
        query_non_compl_tickets.AND("Status",query_non_compl_tickets.NotEqual,at.picklist['Ticket']['Status']['Complete'])
        query_non_compl_tickets.AND("QueueID",query_non_compl_tickets.NotEqual,29683485)
        query_non_compl_tickets.AND("QueueID",query_non_compl_tickets.NotEqual,29683487)
        query_non_compl_tickets.AND('LastActivityDate',query_non_compl_tickets.GreaterThanorEquals,checking_date)
        
        tickets = at.query(query_non_compl_tickets).fetch_all()
        df = pd.DataFrame([dict(ticket) for ticket in tickets])
        
        return df,tickets

    def get_all_non_compl_incidents_from_td(self):
        '''
        Returns all incidents from TopDesk, created by PQR
        '''
        
        url_ = "https://nieuwkoop.topdesk.net/tas/api/incidents?page_size=500&modification_date_start={}&closed=false&operator=7b234055-a0d2-4998-9419-4f7166486371&".format(self.start_time[:10])
        r= requests.get(url_,headers=get_headers)

        if r.status_code==200:
            return r
        else:
            return []

    def get_all_attachments_from_at(self):


        '''
        Returns all Autotask attachments, belonging to the tickets in the given list of ids.

        Parameters:

        id_ [list] : List of Autotask ticket ids, for which we want to retrieve attachments

        Returns:

        Tuple: (Python DataFrame, list of attachments)
        '''
        id_ = [ticket.id for ticket in self.open_at_tickets[1]]

        if len(id_)==0:
            return pd.DataFrame(),[]

        attachmentInfo = atws.Query('AttachmentInfo')
        if len(id_)==1:
            attachmentInfo.WHERE('ParentID',attachmentInfo.Equals,id_[0])   
        else:
            attachmentInfo.WHERE('ParentID',attachmentInfo.Equals,id_[0])
            for element in id_[1:]:
                attachmentInfo.OR('ParentID',attachmentInfo.Equals,element)
        attachments = at.query(attachmentInfo).fetch_all()

        if len(attachments)==0:
            return pd.DataFrame(),[]
        else:

            df = pd.DataFrame([dict(att) for att in attachments])
            return df,attachments     

    def get_all_attachments_from_td(self): 

    
        '''
        Returns all tuple consisting of: (attachments from TD, list of AT ticket numbers, representing TD counterparts.  
        '''
        td_tickets = self.open_td_incidents

        if td_tickets.status_code != 200:
            return [],[]

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

                    # eliminate Topdesk system created attachments

                    if at1['fileName'] == "Oorspronkelijke aanvraag.pdf":
                        continue

                    ss = {external_number : at1}

                    attachments.append(ss) 



            else:
                continue
        #these are AT ticket numbers that I need to take, and check their attachments 
        at_ticket_numbers = list(set([list(it.keys())[0] for it in attachments]))
        
        
        cleaned_list = []
        
        for num in at_ticket_numbers:
            if num[:2] !='T2':
                continue
            else:
                
                cleaned_list.append(num)
                
        
        return attachments, cleaned_list 
    
    def list_at_ticket_for_counterparts(self):

        '''
        Returns all non completed tickets in Autotask (those still open), and filters those that do not have     
        TD counterparts. (Tickets that need to be created in Topdesk)
        
        Parameters:
        None
        
        Returns:
        
        Tuple: (Python DataFrame, list of Autotask tickets for which we need to create counterparts in Topdesk.
        '''

        df,tickets= self.open_at_tickets

        if len(tickets)==0:
            return []

        # df[df['ChangeInfoField1']!='']
        # ids = []

        # for ticket in tickets:
        #     ref = ticket.get_udf('Reference_NWK') =='No':
        #     ids.append(ticket.id)



        # ids = list(df[df['ChangeInfoField1']==''].id)
        tickets_to_create_in_TD = []
        
        for ticket in tickets:
            try:
                ref = ticket.get_udf('Reference_NWK')
            except:
                ref = 'old ticket'

                
            if ref == 'No':
                tickets_to_create_in_TD.append(ticket)  

        # df_ = pd.DataFrame([dict(ticket) for ticket in tickets_to_create_in_TD])
        
        return tickets_to_create_in_TD

    def list_td_incidents_for_counterparts(self):


        td_incidents = self.open_td_incidents


        if type(td_incidents)==list:
            return []

        if td_incidents.status_code != 200:
            return []

        td_tickets_without_at_counterparts=[]

                
        for ticket in td_incidents.json():
            if ticket['externalNumber']=='':
                td_tickets_without_at_counterparts.append(ticket)
                
        return td_tickets_without_at_counterparts

    def create_at_tickets_counterparts(self):
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

        tickets_to_create_in_TD = self.list_at_ticket_for_counterparts()

        if len(tickets_to_create_in_TD)==0:

            return 'Nothing to update'

        # _,tickets_to_create_in_TD = self.list_at_ticket_for_counterparts # list_at_ticket_for_counterparts()
        
        for ind, ticket in enumerate(tickets_to_create_in_TD):

            try: 
                request=ticket.Description 
            except:
                request = 'Default description'

            at_ticket_number = ticket.TicketNumber
            try:
                brief_descr = ticket.Title[:99]    
            except:
                brief_descr="No brief description"
            
            try:


                caller_id = get_contact_extID_for_id(ticket.ContactID)

                
            except:

                caller_id = 0 #in the make_incident, default caller_id value will be used

            
            
            status = ""

            try:
                r_inc = make_incident(request=request,brief_descr=brief_descr,at_ticket_number=at_ticket_number, caller_id=caller_id,status=status)
                td_ticket_number=r_inc.json()['number']

                #here we need to update udf Reference_NWK

                tickets_to_create_in_TD[ind].set_udf('Reference_NWK',td_ticket_number)

                # tickets_to_create_in_TD[ind].ChangeInfoField1= td_ticket_number      
            except: 
                continue
        


        try:
            at.update(tickets_to_create_in_TD).execute()

            
            
            return ("Tickets updated",tickets_to_create_in_TD)
        
        except Exception as e:
            
            return ("There was an mistake in updateing :", e)
    
    def create_td_incidents_counterparts(self):
    
    
        ticket_to_be_updated =  self.td_incidents_for_counterparts #list_td_ticket_for_counterparts()


        number=0
        for ticket in ticket_to_be_updated:
            
        
            try:
                # we take few infos about the ticket in TD, and create new ticket with ChangeInfoField1= TD number
                
                # define title 
                
                if ticket['briefDescription'][:254]=='':
                    ticket['briefDescription'] = "No brief description"
                    
                title= ticket['briefDescription'][:254]

                descr = ticket['request'][:7900]

                Reference_NWK = ticket['number']

                try: 
                    caller_id = ticket['caller']['id']

                    contact_id = get_contact_id_for_extID(caller_id) #try to get contact ID
                    print(contact_id)
                    logging.info(contact_id)
                
                except:
                    contact_id = "" # this field will be skipped in "create_new_ticket_in_at"

                #Here we create new ticket in AT, with reference to TD

                at_ticket = create_new_ticket_in_at(title=title,descr=descr,Reference_NWK=Reference_NWK,status="",contact_id=contact_id)

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
            

            
        return ('Topdesk tickets-counterparts created',ticket_to_be_updated, 'Number of errors: ', number)




    def add_attachment_ids_to_dict(self):
        #First get the list of all non completed tickets from Autotask

        df_,tickets =self.open_at_tickets #get_non_compl_tickets()

        #now we extract list of ids of interested_tickets.we need this list to get all attachments

        

        tickets_ids_for_attachment_check = [ticket.id for ticket in tickets] #list(df_.id)

        if len(tickets_ids_for_attachment_check) == 0:
            return ('Nothing to update')
            

        df_attach , at_attachments = self.get_all_attachments_from_at()  #get_all_attachments_for_list_of_ids(tickets_ids_for_attachment_check)

        try:
            list_of_ticket_ids = list(df_attach.ParentID.unique())
        except:
            list_of_ticket_ids=[]



        tickets_to_update = []

        for ticket in tickets:
            if ticket.id in list_of_ticket_ids:

                try:

                    attachment_ids = list(df_attach[df_attach.ParentID==ticket.id].id)
                except:
                    continue
            else:
                continue
            #now, we need to check if there is a dictionary in ChangeInfoField2. If there is not, we need to create one.
            # dictionary will have attachment_ids as keys, and '' as values. 

            #if there is, we need to check if all attachment_ids are in its keys. 

            # If all attachment_ids are in keys, we do continue. If not, we need to add them to the dictionary 

            #get the reference dictionary for attachments.. (UDF)
            try: 

                attach_dictionary = ticket.get_udf("Attachment_NWK")

            except:

                attach_dictionary = 'No'



            if  attach_dictionary=='No':   #there are no attachment references created        #ticket.ChangeInfoField2 =='':
                #if this field is empty, we need to create dictionary
                attachm_dict = {}
                for id_ in attachment_ids:
                    attachm_dict[id_] = ''

                ticket.set_udf("Attachment_NWK",str(attachm_dict))
                # ticket.ChangeInfoField2 = str(attachm_dict)
                tickets_to_update.append(ticket)
            else:
                #First extract existing dictionary, with its keys and values

                try:
                    attachm_dict = ast.literal_eval(attach_dictionary) #ticket.ChangeInfoField2)
                except:
                    continue

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

                else:
                    ticket.set_udf("Attachment_NWK",str(attachm_dict))
                    # ticket.ChangeInfoField2 = str(attachm_dict)
                    
                    tickets_to_update.append(ticket)

        if len(tickets_to_update) == 0:
            print ('Nothing to update ')

        else:
            try:
                at.update(tickets_to_update).execute()
                print( 'Relation dictionaries updated successfully')
            except:
                print ('There was an error in updating relation dictionaries')



        
        #Now we take all attachments from Topdesk, and get the list of related autotask tickets
        attachments,at_tickets = self.get_all_attachments_from_td()
        try:

            df_tickets , at_tickets1 = get_list_of_at_tickets(at_tickets)
        except:

            df_tickets, at_tickets1 = pd.DataFrame(),[]

        tickets_to_update1 = []

        #check in the TD ids, are in the AT ticket rel_dict
        for ind,ticket in enumerate(at_tickets1):

            

            try:

                rel_dict = ast.literal_eval(ticket.get_udf("Attachment_NWK"))


                # rel_dict = ast.literal_eval(ticket.ChangeInfoField2)
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
                            rel_dict[int(at_attachment_id)] = td_attachment_id

                            
                            at_tickets1[ind].set_udf("Attachment_NWK",str(rel_dict))

                            # at_tickets1[ind]['ChangeInfoField2'] = str(rel_dict)
                            at_tickets1[ind]["Status"] = at.picklist['Ticket']['Status']['Customer Note Added']
                            tickets_to_update1.append(at_tickets1[ind])

                        else:

                            continue


                        # Now, when we have at_attachment id, we need to update rel_dict

                        # rel_dict[int(at_attachment_id)] = td_attachment_id

                        # at_tickets1[ind]['ChangeInfoField2'] = str(rel_dict)
                        # at_tickets1[ind]["Status"] = at.picklist['Ticket']['Status']['Customer Note Added']
                        # tickets_to_update1.append(at_tickets1[ind])

        if len(tickets_to_update1)==0:
            return 'Nothing to update'

        
        
        try:
            at.update(tickets_to_update1).execute()
            self.open_at_tickets = self.get_all_non_compl_tickets_from_at()
            self.open_td_incidents = self.get_all_non_compl_incidents_from_td()
            return ('Successfully created Topdes counterparts attachments: ', tickets_to_update1)
        except:

            return 'There was an arror in updating at tickets'
        
    def make_at_attachments_counterparts(self):
        
        df_,tickets =self.open_at_tickets  #get_non_compl_tickets()

        #now we extract list of ids of interested_tickets.we need this list to get all attachments
        # tickets_ids_for_attachment_check = list(df_.id)


        df_attach , at_attachments = self.get_all_attachments_from_at()  #get_all_attachments_for_list_of_ids(tickets_ids_for_attachment_check)
        
        try:
            list_of_ticket_ids = list(df_attach.ParentID.unique())
        except:
            list_of_ticket_ids=[]

        
        at_tickets_to_update = []

        for ind,ticket in enumerate(tickets):
            #Find related incident number in TD

            related_incident_number= ticket.get_udf("Reference_NWK")






            # related_incident_number= ticket.ChangeInfoField1

            #extract attachment rel dictionary
            try:
                attachm_dict = ast.literal_eval(ticket.get_udf("Attachment_NWK"))

                # if attachm_dict == 'No':
                #     continue
            
            except:
                attachm_dict = "No"


            

            if attachm_dict == 'No':
                continue 
            

    
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

                #here we need to update the statos of incident to " Reactie ontvangen"

                url_ = td_base_url + "/tas/api/incidents/number/{}".format(related_incident_number)
                data_status = {"processingStatus" : {"id": "8228e2f3-1e1f-4563-a970-51487483e7dc"}}

                r2= requests.patch(url_, data=json.dumps(data_status), headers=get_headers)





                if inc_attachment.status_code!=200:

                    attachm_dict[att_id] = "error"

                    tickets[ind].set_udf("Attachment_NWK",str(attachm_dict))


                    # tickets[ind].ChangeInfoField2 = str(attachm_dict)

                    at_tickets_to_update.append(tickets[ind])


                else:

                    #update dictionary in AT, and make reference with TD attachment id

                    attachm_dict[att_id] = inc_attachment.json()["id"]

                    tickets[ind].set_udf("Attachment_NWK",str(attachm_dict))




                    # tickets[ind].ChangeInfoField2 = str(attachm_dict)

                    at_tickets_to_update.append(tickets[ind])


        
        if len(at_tickets_to_update) == 0:
            return 'Nothing to update'
        
        else:
            
            try:
                at.update(at_tickets_to_update).execute()

                return ('Updated Autotask tickets: ',at_tickets_to_update)

            except:
                
                return 'Rel.dicts were not updated'

    #here we have methods about notes/actions

    def get_all_actions_from_td(self):

        r=self.get_all_non_compl_incidents_from_td()

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
                    # if incident_actions.status_code==200:
                    for action in incident_actions.json():
                        ss = {ticket_number : action}

                        action_list.append(ss)

                    # else:
                    #     continue
                else:
                    continue

            at_ticket_numbers = list(set([list(it.keys())[0] for it in action_list]))

            cleaned_list = []
        
            for num in at_ticket_numbers:
                if (num[:2] !='T2') | (len(num)<14) | (len(num)==15):
                    continue
                else:

                    cleaned_list.append(num)

        return action_list, cleaned_list

    def update_note_rel_dict(self):  

        df_,tickets=self.open_at_tickets #get_non_compl_tickets()

        if len(tickets)==0:
            return 'No tickets to update'

        logging.warning("the length of tickets is: {}".format(len(tickets)))
        try: 
            list_at_ids =[ticket.id for ticket in tickets]

            df_notes,notes = get_ticket_notes_at(list_at_ids)
            
            list_of_ticket_ids = list(df_notes.TicketID.unique())

            logging.warning("ticket ids: {}".format(list_of_ticket_ids))

        except:            
            tickets =[]

        
        note_errors=0

        tickets_to_update=[]

        for ticket in tickets:

            if ticket.id in list_of_ticket_ids:
                notes_ids = list(df_notes[df_notes.TicketID==ticket.id].id)

                logging.warning("note ids: {}".format(notes_ids))
            else:
                continue
            #now, we need to check if there is a dictionary in ChangeInfoField3. If there is not, we need to create one.
            # dictionary will have note_ids as keys, and '' as values. 

            #if there is, we need to check if all attachment_ids are in its keys. 

            # If all attachment_ids are in keys, we do continue. If not, we need to add them to the dictionary 
            try:
                note_rel_dict = ticket.get_udf("Note_NWK")
            except:

                note_rel_dict = "No"


            if  note_rel_dict == "No": #ticket.ChangeInfoField3 =='':
                #if this field is empty, we need to create dictionary
                notes_dict = {}
                for id_ in notes_ids:
                    notes_dict[id_] = ''

                ticket.set_udf("Note_NWK",str(notes_dict))
                # ticket.ChangeInfoField3 = str(notes_dict)

                logging.warning('For ticket_id: {}, dictionary is: {}'.format(ticket.id,notes_dict))
                tickets_to_update.append(ticket)
            else:
                #First extract existing dictionary, with its keys and values


                notes_dict = ast.literal_eval(note_rel_dict) #ticket.ChangeInfoField3)
                #make a set of its keys:
                already_existing_keys = set(notes_dict.keys())
                set_of_new_keys = set(notes_ids)
                #keys to add to dictionary:
                keys_to_add = list(set_of_new_keys -already_existing_keys)

                logging.warning('these are keys to be {} added, and total {}'.format(keys_to_add, len(keys_to_add)))

                if len(keys_to_add) == 0:
                    continue

                for id_ in keys_to_add:
                    notes_dict[id_] = ''
                #Now we make string representation of  attachm_dict, and save it to the   ChangeInfoField2
                
                ticket.set_udf("Note_NWK",str(notes_dict)) 
                # ticket.ChangeInfoField3 = str(notes_dict)

                tickets_to_update.append(ticket)
        
        logging.warning("Tickets to be update are: {}".format(tickets_to_update))
            



        if len(tickets_to_update) == 0:
                print('Nothing to update')

        else:
            try:
                at.update(tickets_to_update).execute()
                print('Relation notes dictionaries updated successfully')
            except:
                print ('There was an error in updating relation notes dictionaries')


        #Now we are taking actions from Topdesk, and list list of Autotask tickets, 
        #those actions are related to



        # self.open_at_tickets = self.get_all_non_compl_tickets_from_at()
        # self.open_td_incidents = self.get_all_non_compl_incidents_from_td()

        actions,at_tickets = self.get_all_actions_from_td()
      
        #df_tickets,at_tickets1 = self.get_all_non_compl_tickets_from_at() # it was this line

        try:
            df_tickets,at_tickets1 = get_list_of_at_tickets(at_tickets)
        except:
            df_tickets,at_tickets1 = pd.DataFrame(), []

        tickets_to_update = []

        for ind,ticket in enumerate(at_tickets1):


            try:
                #try first to get the status of counterpart incident
                url_incident = "https://nieuwkoop.topdesk.net/tas/api/incidents?external_number={}".format(ticket['TicketNumber'])
                            
                incident_for_status_checking = requests.get(url_incident, headers=get_headers)

                if incident_for_status_checking == 200:
                    counterpart_incident_status_id = incident.json()[0]['processingStatus']['id']
                else:

                    counterpart_incident_status_id= "3a43942b-ab8e-4fcf-b57d-e29783eba4d1"



            except:

                counterpart_incident_status_id= "3a43942b-ab8e-4fcf-b57d-e29783eba4d1"


            try:

                rel_dict = ast.literal_eval(ticket.get_udf("Note_NWK"))  #ticket.ChangeInfoField3)

            except:

                rel_dict = {}
                #here we need to create 

            td_ids_in_values = list(rel_dict.values())


            #check
            for action in actions:

                if list(action.keys())[0]==ticket['TicketNumber']:

                    td_action_id = list(action.values())[0]['id']

                    if td_action_id in td_ids_in_values:
                        continue
                        # print('For this AT ticket: ', ticket['TicketNumber'],'\n')
                        # print('TD attachment: ',td_attachment_id,'\n')
                        # print('it is already connected')
                    else:
                        # extract dictionary of action

                        act1 = list(action.values())[0]

                        #now we need to create this action as Autotask note

                        descr = act1['memoText']

                        if descr[:14]== "Initial action":
                            # print('it was just intitially created ticket')
                            continue 


                        ticket_id=ticket.id

                        try:

                            note=make_note_in_at(descr=descr,ticket_id=ticket_id)
                            print('note created')
                            note_id = note.id


                            rel_dict[note_id] = td_action_id

                            at_tickets1[ind].set_udf("Note_NWK", str(rel_dict))

                            #here we need to check the status of incidents, and update the status of ticket
                            #acordingly. 
                            # first we fatch incident where the externalNumber equals ticket['TicketNumber'],
                            # and extract its status

                            if counterpart_incident_status_id == '70b2967d-e248-4ff9-a632-ec044410d5a6': # if the inc_status is Afgemeld
                                at_tickets1[ind]["Status"] = at.picklist['Ticket']['Status']['Complete']

                            else:

                                at_tickets1[ind]["Status"] = at.picklist['Ticket']['Status']['Customer Note Added']


                            tickets_to_update.append(at_tickets1[ind])

                        except:

                            note_errors +=1 

                            continue

                        # Now, when we have at_attachment id, we need to update rel_dict

                        #rel_dict[note_id] = td_action_id
                        # print(ticket.id,rel_dict)

            
            # at_tickets1[ind].set_udf("Note_NWK", str(rel_dict))
            # # at_tickets1[ind]['ChangeInfoField3'] = str(rel_dict)
            # at_tickets1[ind]["Status"] = at.picklist['Ticket']['Status']['Customer Note Added']

        # tickets_to_update.append(at_tickets1[ind])



        if len(tickets_to_update)==0:
            return ('Nothing to update',note_errors)

        try:

            at.update(tickets_to_update).execute()
            self.open_at_tickets = self.get_all_non_compl_tickets_from_at()
            self.open_td_incidents = self.get_all_non_compl_incidents_from_td()

            return('All dicts were update succesfully',note_errors)
        except:
            return('There was an error in updateing dict')

    def make_at_notes_counterparts(self):

        self.open_at_tickets = self.get_all_non_compl_tickets_from_at()
        self.open_td_incidents = self.get_all_non_compl_incidents_from_td()


        df_,tickets =self.open_at_tickets #self.open_at_tickets  #get_non_compl_tickets()

        #now we extract list of ids of interested_tickets.we need this list to get all attachments
        
        tickets_ids_for_notes_check =[ticket.id for ticket in tickets] #list(df_.id)

        if len(tickets_ids_for_notes_check)==0:
            return 'No thickets  to update'


        df_notes,notes = get_ticket_notes_at(tickets_ids_for_notes_check)


        # df_attach , at_attachments = get_all_attachments_for_list_of_ids(tickets_ids_for_attachment_check)

        try: 
            list_of_ticket_ids = list(df_notes.TicketID.unique())
        except:
            list_of_ticket_ids = []

        
        at_tickets_to_update = []


        for ind,ticket in enumerate(tickets):
            #Find related incident number in TD



            related_incident_number= ticket.get_udf("Reference_NWK") #ticket.ChangeInfoField1

            try: 
                note_rel_dict = ticket.get_udf("Note_NWK")
            except:

                note_rel_dict = "No"


            if note_rel_dict == 'No':
                continue 
            else:    
                notes_dict = ast.literal_eval(note_rel_dict)

    
            non_rel_notes_ids = []
            for k, v in notes_dict.items():
                if v=='':

                    non_rel_notes_ids.append(k)

            for att_id in non_rel_notes_ids:

                df_non_rel_notes,non_rel_notes= get_notes_for_list_of_note_ids([att_id])
                        
                for note in non_rel_notes:

                    #now we need to create notes counterparts in Topdesk 

                    memo_text=note.Description



                    url_ = td_base_url + "/tas/api/incidents/number/{}".format(related_incident_number)

                    data_ = {"action": memo_text}

                    r = requests.patch(url_, data=json.dumps(data_), headers=get_headers)

                    #here we need to update the statos of incident to " Reactie ontvangen"

                    url_ = td_base_url + "/tas/api/incidents/number/{}".format(related_incident_number)
                    data_status = {"processingStatus" : {"id": "8228e2f3-1e1f-4563-a970-51487483e7dc"}}

                    r1= requests.patch(url_, data=json.dumps(data_status), headers=get_headers)
                    
                    if r.status_code!=200:   

                        continue            

                        # notes_dict[att_id] = "error" 

                        # tickets[ind].set_udf("Note_NWK",str(notes_dict))

                        # tickets[ind].ChangeInfoField3 = str(notes_dict)

                        # at_tickets_to_update.append(tickets[ind])

                    else:

                        #update dictionary in AT, and make reference with TD attachment id
                        # get the action id from the latest made action

                        

                        action_url = td_base_url + r.json()['action'] + "?start=0&page_size=100"

                        r_action = requests.get(action_url, headers=get_headers)

                        if r_action.status_code==200:

                            action_id123 = pd.DataFrame(r_action.json()).sort_values(by='entryDate').iloc[-1]['id'] 
                            notes_dict[att_id] = action_id123
                            tickets[ind].set_udf("Note_NWK",str(notes_dict) )

                            at_tickets_to_update.append(tickets[ind])

            # tickets[ind].set_udf("Note_NWK",str(notes_dict) )
            # tickets[ind].ChangeInfoField3 = str(notes_dict)

            # at_tickets_to_update.append(tickets[ind])
        
        if len(at_tickets_to_update) == 0:
            logging.warning('Nothing to update')
            return 'Nothing to update'
        
        else:
            
            try:

                list_id = [ticket.id for  ticket in at_tickets_to_update ]

                logging.warning('List of tickets for updating: '.format(str(list_id)))
                at.update(at_tickets_to_update).execute()
                self.open_at_tickets = self.get_all_non_compl_tickets_from_at()
                self.open_td_incidents = self.get_all_non_compl_incidents_from_td()


                return 'Tickets updates',list_id #at_tickets_to_update

            except:
                
                return 'Rel.dicts were not updated since error occ'

    def update_statuses_in_at_counterparts(self):
        at_tickets_to_update = []
        td_ticket_to_change_status = []
        
        tickets_=self.open_at_tickets[1]

        

        for ticket in tickets_:
            

            try: 

                ex_status = int(ticket.get_udf("Status_NWK"))
                # logging.warning(type(ticket.Status))
                # logging.warning(type(int(ex_status)))

            except:

                ex_status = "No"

            if (ticket.Status == 1) & ( ex_status == "No"):
            

                ticket.set_udf("Status_NWK",1)
            
                # ticket.ChangeInfoField4 = 1 
                at_tickets_to_update.append(ticket)
                            
                continue
                
            # if the status was not changed    
            if ticket.Status == ex_status:

                
                continue
                
            
            if ((ticket.Status == 26) | (ticket.Status == 8)): 

                logging.warning("it was here")
                ticket.set_udf("Status_NWK", ticket.Status)
                #ticket.ChangeInfoField4 = ticket.Status 
                at_tickets_to_update.append(ticket)
                td_ticket_to_change_status.append(ticket)

                continue
        
            else:

                ticket.set_udf("Status_NWK", ticket.Status)
                
                # ticket.ChangeInfoField4 = ticket.Status 
                at_tickets_to_update.append(ticket)


        
     
        if len(at_tickets_to_update) == 0:


            print ('No status needs to be updated in Autotask')

        else:

            try: 
                at.update(at_tickets_to_update).execute()

                print ("These ticket were update in Autotask",at_tickets_to_update)
            
            except:

                print('there was an arror in update tickets statuses in Autotask')
    



        if len(td_ticket_to_change_status) == 0: 
            return('No status needs to be updated in Topdesk')

        else:
            for ticket1 in td_ticket_to_change_status:

                incidents_updated = [] 
                related_incident_number = ticket1.get_udf("Reference_NWK") #ChangeInfoField1
                try: 
                    url_ = td_base_url + "/tas/api/incidents/number/{}".format(related_incident_number)
                    data_status = {"processingStatus" : {"id": "3a43942b-ab8e-4fcf-b57d-e29783eba4d1"}} #in In behandeling
                    r2= requests.patch(url_, data=json.dumps(data_status), headers=get_headers)

                    if r2.status_code==200:
                        incidents_updated.append(related_incident_number)
                    else:
                        continue
                except:
                    continue

            return ('Updated tickets: ', at_tickets_to_update,'Updated incidents: ',incidents_updated)
                    

    def update_statuses_in_td_counterparts_reopened(self):
    
        at_tickets_to_update=[]

        if type(self.open_td_incidents) == list:
            return  ('Nothing to update')

    
        if self.open_td_incidents.status_code !=200:

            return  ('There was an mistake')

        else:

            incidents=self.open_td_incidents.json()


        for incident in incidents:

            ex_status = incident['optionalFields1']['text1']

            if (ex_status=='Gered') & (incident['processingStatus']['id']!='c953d77d-f789-432b-8533-68039b7ec831'):

                # add that ticket to the list
                at_tickets_to_update.append(incident['externalNumber'])

                #update 'gereed' to ''
                inc_number = incident['number']

                url_ = td_base_url + "/tas/api/incidents/number/{}".format(inc_number)


                data_status = {"optionalFields1" : { "text1" : "" }} #reset that field

                #update incident status to in behandeling
                r2= requests.patch(url_, data=json.dumps(data_status), headers=get_headers)

            else:
                continue

        if len(at_tickets_to_update) != 0:

            _,tickets_for_updateting = get_list_of_at_tickets(at_tickets_to_update)


            for ind,_ in enumerate(tickets_for_updateting):

                tickets_for_updateting[ind].Status = at.picklist['Ticket']['Status']['Customer Note Added']


            try:

                at.update(tickets_for_updateting).execute()

                return ('Re-open tickets: ', at_tickets_to_update )
            except:

                return ('Error in updating re opened tickets' )

        else:

            return ('No re-opened tickets' )



    def closing_tickets(self):
        df_ticket, tickets= get_all_open_tickets()

        if len(tickets) == 0:
            return ('No tickets/ closing')

        else:

            ticket_for_closing_potential = []

            for ticket in tickets:
                try: 
                    rel_number = ticket.get_udf('Reference_NWK')
                except:

                    rel_number = 'No'

                if rel_number !="No":

                    ticket_for_closing_potential.append(ticket.TicketNumber)

            tickets_ = set(ticket_for_closing_potential) 

        # take open incidents



        incidents_for_closing_potential = []

        r= get_all_non_compl_incidents_from_td()

        if r.status_code==200:
            open_incidents = r.json()
        else:

            open_incidents=[]

        for inc in open_incidents:
            if inc['externalNumber'] != "":
                incidents_for_closing_potential.append(inc['externalNumber'])

        incidents_for_closing_potential_1=[]

        for ind, inc in enumerate(incidents_for_closing_potential):
            if incidents_for_closing_potential[ind]=='T200 200 200':

                continue

            else:

                incidents_for_closing_potential[ind]= re.sub('Uw PQR ticketnummer: ', '', incidents_for_closing_potential[ind])
                incidents_for_closing_potential[ind]= re.sub('\u200b', '', incidents_for_closing_potential[ind])

                incidents_for_closing_potential_1.append(incidents_for_closing_potential[ind])


        incidents_ = set(incidents_for_closing_potential_1)

        # now we need set difference to conclude where to close which tickets/incidents

        # closed_in_TOPDESK = tickets_ - incidents_


        to_be_closed_in_AUTOTASK = tickets_ - incidents_

        to_be_closed_in_TOPDESK = incidents_ - tickets_

        for_closing_in_AT = []

        for ticket in tickets:

            if ticket.TicketNumber in to_be_closed_in_AUTOTASK:       
                ticket.Status = at.picklist['Ticket']['Status']['Complete']

                for_closing_in_AT.append(ticket)

        if len(for_closing_in_AT)!=0:

            at.update(for_closing_in_AT).execute()



        for_closing_in_TD = []

        for inc in open_incidents:
            if inc['externalNumber'] in to_be_closed_in_TOPDESK:
                for_closing_in_TD.append(inc['number'])

        for inc_number in for_closing_in_TD:
            try: 

                url_ = td_base_url + "/tas/api/incidents/number/{}".format(inc_number) #fix the ticket for closing

                data_status = {"processingStatus" : {"id": 'c953d77d-f789-432b-8533-68039b7ec831'},"optionalFields1" : { "text1" : "Gereed" }} # in Gereed
                
                r2 = requests.patch(url_, data=json.dumps(data_status), headers=get_headers)

            except:
                pass

        return ('List of closed ticket ', for_closing_in_AT, ' List of closed incidents: ' ,for_closing_in_TD )


            