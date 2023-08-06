from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws
import atws.monkeypatch.attributes
import pandas as pd
import requests
import ast
import json


from . import tickets
from . import notes
from . import actions

from tickets import get_non_compl_tickets,get_list_of_at_tickets
from notes import get_ticket_notes_at,make_note_in_at,get_notes_for_list_of_note_ids
from actions import get_all_actions_from_td



def update_notes_rel_dict():

    df_,tickets=get_non_compl_tickets()

    list_at_ids =[ticket.id for ticket in tickets]

    df_notes,notes = get_ticket_notes_at(list_at_ids)

    list_of_ticket_ids = list(df_notes.TicketID.unique())



    tickets_to_update=[]

    for ticket in tickets:
        
        if ticket.id in list_of_ticket_ids:
            notes_ids = list(df_notes[df_notes.TicketID==ticket.id].id)
        else:
            continue
        #now, we need to check if there is a dictionary in ChangeInfoField3. If there is not, we need to create one.
        # dictionary will have note_ids as keys, and '' as values. 

        #if there is, we need to check if all attachment_ids are in its keys. 

        # If all attachment_ids are in keys, we do continue. If not, we need to add them to the dictionary 

        if ticket.ChangeInfoField3 =='':
            #if this field is empty, we need to create dictionary
            notes_dict = {}
            for id_ in notes_ids:
                notes_dict[id_] = ''
            ticket.ChangeInfoField3 = str(notes_dict)
            tickets_to_update.append(ticket)
        else:
            #First extract existing dictionary, with its keys and values
            notes_dict = ast.literal_eval(ticket.ChangeInfoField3)
            #make a set of its keys:
            already_existing_keys = set(notes_dict.keys())
            set_of_new_keys = set(notes_dict)
            #keys to add to dictionary:
            keys_to_add = list(set_of_new_keys -already_existing_keys)
            
            if len(keys_to_add) == 0:
                continue
                
            for id_ in keys_to_add:
                notes_dict[id_] = ''
            #Now we make string representation of  attachm_dict, and save it to the   ChangeInfoField2

            ticket.ChangeInfoField3 = str(notes_dict)
            tickets_to_update.append(ticket)

            

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

    actions,at_tickets = get_all_actions_from_td()

    df_tickets,at_tickets1 = get_list_of_at_tickets(at_tickets)
    
    tickets_to_update = []

    for ind,ticket in enumerate(at_tickets1):

        try:
            rel_dict = ast.literal_eval(ticket.ChangeInfoField3)

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

                    act1 = list(actions[0].values())[0]

                    #now we need to create this action as Autotask note

                    descr = act1['memoText']

                    ticket_id=ticket.id


                    try:
                        note=make_note_in_at(descr=descr,ticket_id=ticket_id)
                        note_id = note.id
                    except:

                        continue




                    # Now, when we have at_attachment id, we need to update rel_dict

                    rel_dict[note_id] = td_action_id

                    at_tickets1[ind]['ChangeInfoField3'] = str(rel_dict)
                    
                    tickets_to_update.append(at_tickets1[ind])
                    
    if len(tickets_to_update)==0:
        return 'Nothing to update'
                    
    try:
        
        at.update(tickets_to_update).execute()
        return 'All dicts were update succesfully'
    except:
        return 'There was an error in updateing dict'


def make_at_notes_counterparts():


    df_,tickets =get_non_compl_tickets()

    #now we extract list of ids of interested_tickets.we need this list to get all attachments
    tickets_ids_for_notes_check = list(df_.id)

    df_notes,notes = get_ticket_notes_at(tickets_ids_for_notes_check)


    # df_attach , at_attachments = get_all_attachments_for_list_of_ids(tickets_ids_for_attachment_check)
    list_of_ticket_ids = list(df_notes.TicketID.unique())
    
    at_tickets_to_update = []


    for ind,ticket in enumerate(tickets):
        #Find related incident number in TD

        related_incident_number= ticket.ChangeInfoField1

        if ticket.ChangeInfoField3 == '':
            continue 
        else:    
            notes_dict = ast.literal_eval(ticket.ChangeInfoField3)

 
        non_rel_notes_ids = []
        for k, v in notes_dict.items():
            if (v=='') | (v[:3]=='err'):
                non_rel_notes_ids.append(k)

        for att_id in non_rel_notes_ids:

            df_non_rel_notes,non_rel_notes= get_notes_for_list_of_note_ids([att_id])
                    
            for note in non_rel_notes:

                #now we need to create notes counterparts in Topdesk 

                memo_text=note.Description


                url_ = td_base_url + "/tas/api/incidents/number/{}".format(related_incident_number)

                data_ = {"action": memo_text}

                r = requests.patch(url_, data=json.dumps(data_), headers=get_headers)
                
                if r.status_code!=200:

                    notes_dict[att_id] = "error" 

                    tickets[ind].ChangeInfoField3 = str(notes_dict)

                    at_tickets_to_update.append(tickets[ind])


                else:

                    #update dictionary in AT, and make reference with TD attachment id

                    notes_dict[att_id] = r.json()["id"]

                    tickets[ind].ChangeInfoField3 = str(notes_dict)

                    at_tickets_to_update.append(tickets[ind])
        
    if len(at_tickets_to_update) == 0:
        return 'Nothing to update'
    
    else:
        
        try:
            at.update(at_tickets_to_update).execute()

            return at_tickets_to_update

        except:
            
            return 'Rel.dicts were not updated since error occ'
    
    
    
    
    


