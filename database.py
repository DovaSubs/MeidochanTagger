#Intented to work on Repl.it using web server (flask) 
from replit import db
import datetime
import flask
import requests
import json
from urllib.parse import unquote, quote

app = flask.Flask(__name__)
sess = requests.Session()

Names = ['miu', 'lia', 'laila', 'hana', 'piyoko', 'hina', 'rose', 'suzu', 'rui', 'pal', 'luna']

@app.route('/')
def home():
    return "Hello. I am alive!"

@app.route("/load_tags")
def load_tags():
  stream_source = flask.request.args['video_id']
  stream_source = stream_source.replace("%20", " ")
  out = ''
  if stream_source in db.keys():
    if type(db[stream_source][0]) == str: #Because I fucked up the first item of every key in the previous database 
      x = db[stream_source][1:]
    else: #New database format
      x = db[stream_source]
    out = [list(idx) for idx in x]
    out = json.dumps(out, separators=(',', ' '))
    out = quote(out)
  return out

@app.route("/load_ids")
def load_ids():
  x = db['streams_ids'][1:]
  y = db['isFinished'][1:]
  out = [x]+[y]
  out = json.dumps(out, separators=(',', ' '))
  out = quote(out)
  return out

@app.route("/save_tags")
def save_tags():
  video_id = flask.request.args['video_id']
  tags = flask.request.args['tags']
  tags = unquote(tags)
  tags = json.loads(tags)
  db[video_id] = tags
  return "Done!"

@app.route("/save_id")
def save_id():
  video_id = flask.request.args['video_id']
  video_id = video_id.replace("%20", " ")
  index = int(flask.request.args['index'])
  x = db['streams_ids'][1:]
  x[index] = video_id
  db['streams_ids'][1:] = x
  isFinished = db['isFinished'][1:] 
  isFinished[index] = 'False'
  db['isFinished'][1:] = isFinished
  print(x)
  print(isFinished)
  return "Done!"

@app.route("/save_state")
def save_state():
  index = int(flask.request.args['index'])
  state = flask.request.args['state']
  isFinished = db['isFinished'][1:] 
  isFinished[index] = state
  db['isFinished'][1:] = isFinished
  print(isFinished)
  return "Done!"

@app.route("/findall")
def findall():
  text = flask.request.args['text']
  text = unquote(text)
  Stream_idx = int(flask.request.args['name'])
  keys_list = []
  for key in db.keys():
    if Names[Stream_idx] in key:
      keys_list.append(key) 
  mats_emb = ''
  for key_stream in keys_list:
    y = db[key_stream]
    mats_emb = find_function(mats_emb, text, y[1:], key_stream.split()[0])
  return mats_emb

def find_function(mats, text, tags, stream_id):
  for idx in tags:
    if text.lower() in idx[1].lower():
      secs = int(idx[0])
      aux2 = format_time_output(secs)
      timestamp = 'https://www.youtube.com/watch?v='+stream_id+'&t='+str(secs)
      mats = mats + f"[{aux2}]({timestamp}) " + idx[1] + '\n'
  return mats

@app.route("/tags")
def tags():
  stream_source = flask.request.args['video_id']
  for n in Names:
    lb = stream_source+' '+n
    if lb in db.keys():
      stream_source = lb
      tags_emb = n
      if type(db[stream_source][0]) == str: #Because I fucked up the first item of every key in the previous database 
         x = db[stream_source][1:]
      else: #New database format
        x = db[stream_source]
      tags_emb = format_tags(stream_source.split()[0], x, tags_emb)
      return tags_emb

def format_time_output(secs):
  date_object = datetime.datetime(2019,10,17) #Creates a "datetime" object (0h0m0s), since this is not possible with "time" objects
  timemark = date_object + datetime.timedelta(seconds=secs)
  if secs<60:
    formatted = timemark.strftime('%S')
  elif secs<3600:
    formatted = timemark.strftime('%-M:%S')
  else:
    formatted = timemark.strftime('%-H:%M:%S')
  return formatted

def format_tags(source, tags_list, tags_out):
  for idx in tags_list:
    secs = int(idx[0])
    aux2 = format_time_output(secs)      
    timestamp = 'https://www.youtube.com/watch?v='+source+'&t='+str(secs)
    if len(tags_out + f"[{aux2}]({timestamp}) " + idx[1] + ' (' + str(idx[2]-1) +') ' + '\n')>=(2500*len(tags_out.split('|'))):
      tags_out = tags_out + '|'
    if idx[2]>1:
      tags_out = tags_out + f"[{aux2}]({timestamp}) " + idx[1] + ' (' + str(idx[2]-1) +') ' + '\n'
    else:
      tags_out = tags_out + f"[{aux2}]({timestamp}) " + idx[1] + '\n'
  return tags_out

@app.route("/rank")
def rank():
  users_list = []  
  for key in db.keys():
    if len(key.split())>1: #If key is stream ID
      y = db[key]
      for idx in y:
        users_list.append(idx[4])
  users_rank = {i:users_list.count(i) for i in users_list}
  sorted_rank = dict(sorted(users_rank.items(), key=lambda item: item[1], reverse=True))
  sorted_rank = json.dumps(sorted_rank)
  return sorted_rank

app.run(host='0.0.0.0',port=8080)
