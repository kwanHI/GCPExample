## Include whichever API are appropriate for your cloud provider
import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment

from datetime import datetime
import json

# for bucket
import os
from google.cloud import storage

# for noSQL Firestore Datastore
import googleapiclient.discovery
from google.cloud import datastore
import requests


##Write ReadReddit To Retriev Dictionary DataSET

# Functions from: https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# Define URL of the RSS Feed I want
def readRedditDict():
    a_reddit_rss_url = 'http://www.reddit.com/new/.rss?sort=new'

    feed = feedparser.parse( a_reddit_rss_url )
    results = {}
    seq =0
    if (feed['bozo'] == 1):
        print("Error Reading/Parsing Feed XML Data")    
    else:
        for item in feed[ "items" ]:
            dttm = item[ "date" ] #"2021-06-17T18:50:49+00:00_2"
            seq +=1
            seqdttm = dttm[:4]+dttm[5:7]+dttm[8:10]+dttm[11:13]+dttm[14:16]+dttm[17:19]+"_"+str(seq)
            results[seqdttm]= \
                    {
                    "posteddatetime":item[ "date" ] ,
                    "title":item[ "title" ],
                    "summary":text_from_html(item[ "summary" ]),
                    "link":item[ "link" ]
                    }

    return results     

############################################
##Write ReadReddit To Retriev Dictionary DataSET

PROJECT='cloud15'

#vbuckname = 'dsa_mini_project_lcn1055'
#filename = 'RedditJson_'+datetime.now().strftime("%Y%m%d%H%M")  #length=19



def list_blobs(bucket_name, blobnamepattern):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()
    retblobs = []
    for blob in blobs:
        if blobnamepattern == '':
            print(blob.name)
            retblobs.append(blob.name)
        else:
            if blobnamepattern in blob.name:
                retblobs.append(blob.name)
    return retblobs    
        

def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix.
    This can be used to list all blobs in a "folder", e.g. "public/".
    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:
        /a/1.txt
        /a/b/2.txt
    If you just specify prefix = '/a', you'll get back:
        /a/1.txt
        /a/b/2.txt
    However, if you specify prefix='/a' and delimiter='/', you'll get back:
        /a/1.txt
    """
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    print('Blobs:')
    for blob in blobs:
        print(blob.name)

    if delimiter:
        print('Prefixes:')
        for prefix in blobs.prefixes:
            print(prefix)
            


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def upload_as_blob(bucket_name, source_data, destination_blob_name, content_type='text/plain'):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    """blob.upload_from_filename(source_file_name)"""
    blob.upload_from_string(source_data, content_type=content_type)
    
    print('Data uploaded to {}.'.format(destination_blob_name))


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))



def read_blob_dict(bucket_name, source_blob_name):
    """Read a blob from the bucket into Text"""
    
    storage_client = storage.Client(project=PROJECT)
    bucket = storage_client.get_bucket(bucket_name)

    # download as string
    json_data = bucket.get_blob(source_blob_name).download_as_string()
    json_dict = json.loads(json_data.decode('utf-8'))   

    return json_dict
    """
    #blob = bucket.get_blob(source_blob_name)
    with open(json_data) as f:
        data = json.load(json_data)
       itSourceId'] = data['RedditSourceId']
    """
## Write your additional Code Segments here, 
##  because your VM will get deleted


vbuckname = 'dsa_mini_project_lcn1055'
filename = 'RedditJson_' + datetime.now().strftime("%Y%m%d%H%M")  #length=19
list_blobs(vbuckname,'')
print('Before load ---------')
# upload_as_blob(vbuckname, json.dumps(readRedditDict(), indent = 4), filename)
list_blobs(vbuckname,'')
print('After load ---------')





