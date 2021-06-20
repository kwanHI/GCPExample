######################################
# for bucket  ----
import os
from google.cloud import storage
import json
# for noSQL Firestore Datastore
import googleapiclient.discovery
from google.cloud import datastore
import requests

from redditfeed import list_blobs, read_blob_dict
######################################

#projectid=cloud15

def create_client(project_id):
    return datastore.Client(project_id)

def add_redditItem(projectid, redditsourceid, redditsourcedtt, title, summary, link):
    client=create_client(projectid)
    key = client.key('Reddit')
    print('Entity is Reddit')
    reddit = datastore.Entity(
        key, exclude_from_indexes=['Title','Summary','Link'])

    reddit.update({
        'RedditSourceId': redditsourceid, #datetime.datetime.utcnow(),
        'RedditSourceDtt': redditsourcedtt,
        'Title': title,
        'Summary':summary,
        'Link': link
    })

    client.put(reddit)

    return reddit.key


def mark_done(client, reddit_id):
    with client.transaction():
        key = client.key('Reddit', reddit_id)
        task = client.get(key)

        if not task:
            raise ValueError(
                'Reddit {} does not exist.'.format(reddit_id))

        reddit['Title'] = 'Done'

        client.put(reddit)

        
def delete_task(client, reddit_id):
    key = client.key('Reddit', reddit_id)
    client.delete(key)  
    

def list_tasks(client):
    query = client.query(kind='Reddit')
    query.order = ['RedditSourceId']

    return list(query.fetch())    


### Loop through bucket to look for a file RedditJsonXXXX to  store data into NoSQL
vbuckname = 'dsa_mini_project_lcn1055'
fnamepattern = 'RedditJson_' 
PROJECT='cloud15'

# Listing RedditJson blob name in the bucket in order to put into NoSQL
redditjson = list_blobs(vbuckname, fnamepattern)
#client = storage.Client(project=PROJECT)
#each  bucketname
for bname in redditjson:
    # Grab data each blb and read row by row
    datadict  = read_blob_dict(vbuckname, bname)
    stop =0
    print('File No.'+ str(stop))
    for k,v in datadict.items():
        stop+=1
    # start write into  firestore-datasore ###
        # print(k)
        c1=str(k)
        
        c2=''
        c3=''
        c4=''
        c5=''
        # v="{'posteddatetime': '2021-06-19T03:07:43+00:00', 'title': 'ASUS TUF Dash 15, 144Hz FHD, RTX 3050 Ti, i7-11370H, 8GB 512GB, $949 - ASUS ROG 13.4" AMD Ryzen 9, RTX 3050 Ti, 16GB 1TB, $1499 - ASUS TUF Gaming F15, 144Hz FHD, i7-11800H, RTX 3050 Ti, 16GB 512GB, $1199 - all available for order', 'summary': '     submitted by /u/gamersecret2 to r/GamingLaptops   [link]  [comments] ', 'link': 'https://www.reddit.com/r/GamingLaptops/comments/o36rs7/asus_tuf_dash_15_144hz_fhd_rtx_3050_ti_i711370h/'}"
        cntiteminOneFile=0
        for kk,vv in v.items():
           cntiteminOneFile+=1  
           if kk=='RedditSourceId' :
               print('****'+v)
               c1=vv
           elif kk=='posteddatetime' or kk=='datetime':
               c2=vv
           elif kk=='title':
               c3=vv
           elif kk=='summary':
               c4=vv
           elif kk=='link':
               c5=vv
           else:
               print("CANNOT FIND:" + kk)
           
        print(c1+'\n'+c2+'\n'+c3+'\n'+c4+'\n'+c5) 
        add_redditItem(PROJECT,c1,c2,c3,c4,c5)
   
        #print(cntiteminOneFile)
    print('****************************\n')
    #print('\n'.join(json.dumps(item) for item in json_list))
    
    # add_redditItem(client, redditsourceid, redditsourcedtt, title, summary, link):
