# import libraries
import requests
import json
import urllib
import pandas as pd

max_results = 50
hapikey = 'AKEYFORHUBSPOT' 
count = 50
contact_list = []
property_list = []
get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/576"


parameter_dict = {'hapikey': hapikey, 'count': count}
headers = {}

has_more = True
while has_more:
    parameters = urllib.urlencode(parameter_dict)
    get_url = get_all_contacts_url + parameters
    r = requests.get(url= get_url, headers = headers)
    response_dict = json.loads(r.text)
    has_more = response_dict['has-more']
    contact_list.extend(response_dict['contacts'])
    parameter_dict['vidOffset']= response_dict['vid-offset']
    if len(contact_list) >= max_results: 
        print('maximum number of results')
        break
print('loop finished')

list_length = len(contact_list) 

print("parsed through {} contact records".format(list_length))



# Example of pulling names emails and titles
from datetime import datetime

# list dump
last_names = []
first_names = []
emails= []
page_title = []
prop_lastmod = []
page_url=[]
content_type=[]
added_at=[]
profile_url=[]

# loop for dataframe
for x in range(len(contact_list)):
    try:
        last_names.append(contact_list[x]['properties']['lastname']['value'])
        first_names.append(contact_list[x]['properties']['firstname']['value'])
        emails.append(contact_list[x]['identity-profiles'][0]['identities'][0]['value'])
        page_title.append(contact_list[x]['form-submissions'][0]['page-title'])
        prop_lastmod.append(contact_list[x]['properties']['lastmodifieddate']['value'])
        page_url.append(contact_list[x]['form-submissions'][0]['page-url'])
        content_type.append(contact_list[x]['form-submissions'][0]['content-type'])
        added_at.append(contact_list[x]['addedAt'])
        profile_url.append(contact_list[x]['profile-url'])
    except:
        "NA"
        

#dataframe construction        
df = pd.DataFrame(data = [first_names, last_names, emails, page_title, prop_lastmod, page_url,content_type ,added_at,profile_url]).transpose()


#dataframe traspose

df_flipped = df.rename(columns ={0:'First', 1:'Last', 2:'Email',3:'page_title', 4:'prop_last_mod',5:'page_url',6:'content_type',7:'addedAT'})


# clean columns
df_flipped['page_title']=df_flipped['page_title'].str.rstrip('|things \n\t')

df_flipped
