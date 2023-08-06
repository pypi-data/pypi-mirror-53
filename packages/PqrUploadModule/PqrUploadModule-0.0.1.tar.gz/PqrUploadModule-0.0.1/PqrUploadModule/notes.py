# Here is the list of modules we need to import
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws
import atws.monkeypatch.attributes
import pandas as pd
import requests


def get_notes_for_list_of_note_ids(id_=[]):
    query_notes=atws.Query('TicketNote')
    
    
    query_notes.open_bracket('AND')


    if len(id_)==1:
        query_notes.WHERE('id',query_notes.Equals,id_[0])
        # query_notes.AND('NoteType',query_notes.Equals,3) #at.picklist['TicketNote']['NoteType']['Task Notes']
    else:
        query_notes.WHERE('id',query_notes.Equals,id_[0])
        # query_notes.AND('NoteType',query_notes.Equals,3) #at.picklist['TicketNote']['NoteType']['Task Notes']

        for element in id_[1:]:
            query_notes.OR('id',query_notes.Equals,element)

    query_notes.close_bracket()

    query_notes.open_bracket('AND')
    
    query_notes.AND('NoteType',query_notes.NotEqual,13)
    query_notes.AND('Publish',query_notes.Equals,1)
    
    query_notes.close_bracket()



    notes = at.query(query_notes).fetch_all()
    
    df = pd.DataFrame([dict(note) for note in notes])

    return df,notes


# def get_ticket_notes_at(id_=[0]):

#     """
#     Returns all notes, belonging to the tickets from the given list. 
    
#     Parameters:
    
#     id_ [list]: list of Autotask ticket ids
#     at [Autotask connect object] : Autotask atws.connect object
    
#     Returns:
    
#     Tuple: (Python DataFrame, list of notes) 
#     """

#     query_notes=atws.Query('TicketNote')
#     query_notes.AND('NoteType',query_notes.Equals,3)
    
#     if len(id_)==1:
#         query_notes.WHERE('TicketID',query_notes.Equals,id_[0])
#     else:
#         query_notes.WHERE('TicketID',query_notes.Equals,id_[0])
#         for element in id_[1:]:
#             query_notes.OR('TicketID',query_notes.Equals,element)
#     notes = at.query(query_notes).fetch_all()
#     df = pd.DataFrame([dict(note) for note in notes])

#     return df,notes

def get_ticket_notes_at(id_=[0]):

    """
    Returns all notes, belonging to the tickets from the given list. 
    
    Parameters:
    
    id_ [list]: list of Autotask ticket ids
    at [Autotask connect object] : Autotask atws.connect object
    
    Returns:
    
    Tuple: (Python DataFrame, list of notes) 
    """

    query_notes=atws.Query('TicketNote')
    #     query_notes.WHERE('NoteType',query_notes.Equals,3)
    #     query.open_bracket('AND')

    query_notes.open_bracket('AND')
    
    if len(id_)==1:
        query_notes.WHERE('TicketID',query_notes.Equals,id_[0])
    else:
        query_notes.WHERE('TicketID',query_notes.Equals,id_[0])
        for element in id_[1:]:
            query_notes.OR('TicketID',query_notes.Equals,element)
            
    query_notes.close_bracket()
      
    query_notes.open_bracket('AND')
    
    query_notes.AND('NoteType',query_notes.NotEqual,13)
    query_notes.AND('Publish',query_notes.Equals,1)
    
    query_notes.close_bracket()
    
    notes = at.query(query_notes).fetch_all()
    df = pd.DataFrame([dict(note) for note in notes])

    return df,notes

def make_note_in_at(title='Title',descr='Long description 3200 chars',note_type=6,ticket_id=0):
    note = at.new('TicketNote')
    note.Title = title
    note.Description = descr
    note.NoteType = 3
    note.TicketID= ticket_id
    note.Publish = 1
    
    note.create()
    
    return note
    

