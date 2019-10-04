from instagram_private_api import Client as PrivateClient

from tinydb import TinyDB, Query
import urllib.request
import datetime
import time
import os

db = TinyDB('db.json')
Story = Query()

username = input('username: ')
password = input('password: ')
web_api = PrivateClient(authenticate=True, auto_patch=True, username=username, password=password)

def create_path(path):
  if not os.path.isdir(path):
    os.makedirs(path)

while True:
  try:
    stories = web_api.reels_tray()
    for origin_stories in stories.get('tray',[]):
      tmp_stories = origin_stories.get('items',[])
      for story in tmp_stories[::-1]:
        if len(db.search(Story.id == story['pk'])) == 0:
          path = datetime.datetime.fromtimestamp(float(story['created_time'])).strftime('%D').replace('/','-')+'/'+origin_stories['user']['username']
          create_path(path)
          path += '/'+str(story['pk'])
          if 'video_versions' in story:
            urllib.request.urlretrieve(story['video_versions'][0]['url'], path+'.mp4')
          else:
            urllib.request.urlretrieve(story['images']['standard_resolution']['url'], path+'.jpg')
          db.insert({'id':story['pk']})
          f = open(path+".txt","w+")
          f.write(str(story))
          f.close()
        else:
          break
    time.sleep(120)
    
  except Exception as e:
    print(e)
  
