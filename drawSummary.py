from google.cloud import datastore
import csv


# For help authenticating your client, visit
# https://cloud.google.com/docs/authentication/getting-started
client = datastore.Client()

query = client.query(kind="Reddit")
query.add_filter("RedditSourceId", ">", "20210615")
# query.order = ["Title"]
result = list(query.fetch())

with open('./output.csv','w') as f:
    writer =  csv.writer(f)
    writer.writerow(['RedditDtt','Title','Link','Summary'])
    for i in result:
        c1=i['RedditSourceDtt'] 
        c2=i['Title']
        c3=i['Summary']     
        c4=i['Link']
        data=[c1,c2,c3,c4]
        writer.writerow(data) 
