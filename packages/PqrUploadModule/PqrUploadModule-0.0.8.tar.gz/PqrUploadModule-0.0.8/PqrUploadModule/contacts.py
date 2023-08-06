
from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws



def get_contact_extID_for_id(id_):
    query_contact = atws.Query('Contact')
    query_contact.WHERE('id',query_contact.Equals,id_)
    contact = at.query(query_contact).fetch_one()
    
    if contact==None:
        return 0
    else:
        # query_contact.fetch_one()
        return contact['ExternalID']


def get_contact_id_for_extID(extID_):
    query_contact = atws.Query('Contact')
    query_contact.WHERE('ExternalID',query_contact.Equals,extID_)

    contact = at.query(query_contact).fetch_one() 
    if contact == None:
        return 0
    
    else:
        # query_contact.fetch_one()
        return contact['id']


