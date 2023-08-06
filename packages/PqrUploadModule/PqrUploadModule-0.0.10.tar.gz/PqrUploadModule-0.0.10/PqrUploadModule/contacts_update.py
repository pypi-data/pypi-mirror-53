from . import authorizations
from authorizations import at,at_url,headers_at,encoded_u,encoded_u_td,td_base_url,get_headers

import atws
import time
import json
import requests


def get_autotask_contact_gem_NK():
    '''
    Returns all contacts from Autotask
    '''
    query_contacts=atws.Query('Contact')
    query_contacts.WHERE('AccountID',query_contacts.Equals,294)
    query_contacts.AND('Active',query_contacts.Equals,1)
    query_contacts.AND('EMailAddress',query_contacts.NotEqual,"")


    contacts = at.query(query_contacts).fetch_all()
    return contacts

def get_persons_from_td():
    '''
    Returns all persons from Topdesk
    '''
    
    persons = []
    i=0
    while(True):
        url_persons= td_base_url + "/tas/api/persons"
        


        url_ = url_persons+'?start={}'.format(str(i))
        try:

            r=requests.get(url_, headers=get_headers)
            if (r.status_code==206) | (r.status_code==200):
                if i==0:
                    persons=r.json()
                else:
                    persons.extend(r.json())
                i=i+10
            else:
                break
        except:
            break
    return persons

def update_contacts_in_autotask():
    
    """
    Updates /synchronizing contacts from Topdesk to Autotask
    """
    
    # get the data
    
    contacts = get_autotask_contact_gem_NK()
    
    persons_td = get_persons_from_td()
    
    count_match = 0
    new_contacts = []
    contacts_to_be_updated = []

    for ind1,person in enumerate(persons_td):

        fn1= person['firstName'].lower()
        ln1 = person['surName'].lower()

        check_pers = fn1+ln1

        for ind,contact in enumerate(contacts):
            fn= contact['FirstName'].lower()
            ln = contact['LastName'].lower()


            if (fn==fn1) & (ln==ln1):
                count_match +=1



                contacts[ind]['ExternalID'] = persons_td[ind1]['id']
                contacts_to_be_updated.append(contacts[ind])
                break


            if ind==len(contacts)-1:

                new_contact = at.new('Contact')
                new_contact.EMailAddress = 'testing@testing.co.rs'
                new_contact.AccountID = 294
                new_contact.FirstName = persons_td[ind1]['firstName']
                new_contact.LastName = persons_td[ind1]['surName']
                new_contact.MobilePhone = persons_td[ind1]['mobileNumber']
                new_contact.ExternalID = persons_td[ind1]['id']
                new_contact.Phone = persons_td[ind1]['phoneNumber']
                new_contact.Active = 1
                new_contacts.append(new_contact)

                break

    
    try:
        if (len(contacts_to_be_updated) != 0) & (len(new_contacts) != 0):
            
            
            
            
            at.update(contacts_to_be_updated).execute()
            
            for cont in new_contacts:
                cont.create()
                time.sleep(0.2)
                
            return "Contacts updated, and new contacs added"
        
        
        if len(new_contacts) != 0:
            
            for cont in new_contacts:
                cont.create()
                time.sleep(0.2)
                
            return "Only new contacts added"
        
        
        else:
            
            return "Nothing to add or update"
            

    except:
        
        return 'There was an error in updating Autotask contacts'

    
            
    