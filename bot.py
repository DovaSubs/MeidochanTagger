from discord.ext import commands
from discord import Embed, utils
import os
from dotenv.main import load_dotenv
from googleapiclient.discovery import build
import datetime
import pytz
import isodate
import re
from urllib.request import urlopen
from urllib.parse import quote, unquote
import json
import sys
from threading import Thread
from time import sleep

def request_db(url):
  strng = ''
  fp = urlopen(url)
  mybytes = fp.read()
  strng = mybytes.decode("utf8")
  fp.close()
  return strng

def format_time_output(secs):
  date_object = datetime.datetime(2019,10,17) #Creates a "datetime" object (0h0m0s), since this function doesn't work with "time" objects
  timemark = date_object + datetime.timedelta(seconds=secs)
  if secs<60:
    formatted = timemark.strftime('%S')
  elif secs<3600:
    formatted = timemark.strftime('%-M:%S')
  else:
    formatted = timemark.strftime('%-H:%M:%S')
  return formatted
          
def convert_date(date_time_str, offset_sec):
  date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
  date_time_obj = date_time_obj + datetime.timedelta(seconds=offset_sec)
  out = date_time_obj.replace(tzinfo=pytz.utc)
  return out

def format_tags(source, tags_list, tags_out): #Formatting tags so it can be splitted into different messages (using .split('|')) since embed messages have a limit 
  for idx in tags_list: #TODO: Improve this
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
  
def main():  
  load_dotenv()
  role_admin = 'moderator'
  role_translator = 'Translator'
  id_admin = 365650515431915523
  localFormat = "%Y-%m-%d %H:%M:%S"
  tz = 'Asia/Tokyo'
  offset_sec = 20 #offset por defecto en segundos, con "20" se tiene entre 5 y 10 segundos dependiendo de la conexión al livestream 

  miu = 'miu-chat'
  lia = 'lia-chat'
  laila = 'laila-chat'
  hana = 'hana-chat'
  piyoko = 'piyoko-chat'
  hina = 'hina-chat'
  rose = 'rose-chat'
  suzu = 'suzu-chat'
  rui = 'rui-chat'
  pal = 'pal-chat'
  luna = 'luna-chat'
  STREAMS = {miu:0, lia:1, laila:2, hana:3, piyoko:4, hina:5, rose:6, suzu:7, rui:8, pal:9, luna:10}
  Names = ['miu', 'lia', 'laila', 'hana', 'piyoko', 'hina', 'rose', 'suzu', 'rui', 'pal', 'luna']

  TL_prefix = ['[Esp]', '[ES]', '(ES)','(ESP)', 'ESP:']
  processThread = ['', '', '', '', '', '', '', '', '', '', '']

  streams_ids = ['', '', '', '', '', '', '', '', '', '', '']
  isFinished = [True, True, True, True, True, True, True, True, True, True, True]
  
  total_time_paused = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  time_paused = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  isPaused = [False, False, False, False, False, False, False, False, False, False, False]
  start_time_utc = ['', '', '', '', '', '', '', '', '', '', '']
  TAGS_LIST = [[], [], [], [], [], [], [], [], [], [], []]
  
  #Repl.it webserver url in .env file (it's possible to use plain text) 
  main_url = os.getenv('main_url')
  #Google Cloud Platform: Application's Api key in .env file
  api_key = os.getenv('api_key')
  youtube = build("youtube", "v3", developerKey=api_key)  

  def save_tags(video_id, tags):
    tags_string = json.dumps(tags, separators=(',', ' '))
    tags_string = quote(tags_string)
    video_id = video_id.replace(" ", "%20")
    success = False
    retry_time = 15
    while not success: #Simple try/except, can be improved
      try:
        url = main_url + f"/save_tags?video_id={video_id}&tags={tags_string}"
        request_db(url)
        success = True
      except Exception as e:
        wait = retry_time
        print ("Re-trying...")
        print(e)
        sys.stdout.flush()
        sleep(wait)
        
  def save_id(index, video_id):
    video_id = video_id.replace(" ", "%20")
    success = False
    retry_time = 15
    while not success: 
      try:
        request_db(main_url + f"/save_id?video_id={video_id}&index={index}")
        success = True
      except Exception as e:
        wait = retry_time
        print ("Re-trying...")
        print(e)
        sys.stdout.flush()
        sleep(wait)

  def save_state(index, state):
    success = False
    retry_time = 15
    while not success: 
      try:
        request_db(main_url + f"/save_state?state={state}&index={index}")
        success = True
      except Exception as e:
        wait = retry_time
        print ("Re-trying...")
        print(e)
        sys.stdout.flush()
        sleep(wait)
        
# Loads ids from database
  def load_ids():
    success = False
    retry_time = 15
    while not success: 
      try:
        ids = request_db(main_url + f"/load_ids")
        success = True
      except Exception as e:
        print ("Re-trying...")
        print(e)
        sys.stdout.flush()
        sleep(retry_time)
    ids = unquote(ids)
    ids = json.loads(ids)
    ids[1] = [False if x == "False" else True for x in ids[1]]
    return ids[0], ids[1]

  def load_tags(video_id):
    video_id = video_id.replace(" ", "%20")
    success = False
    retry_time = 15
    while not success: 
      try:
        tags = request_db(main_url + f"/load_tags?video_id={video_id}")
        success = True
      except Exception as e:
        print ("Re-trying...")
        print(e)
        sys.stdout.flush()
        sleep(retry_time)
    
    tags = unquote(tags)
    if tags:
      tags = json.loads(tags)
    else:
      tags = []
    return tags
      
  streams_ids, isFinished = load_ids()
  print(streams_ids)
  print(isFinished)
# Checks if stream is not Finished and loads its tags
  if False in isFinished:
    for idx in range(len(isFinished)):
      if not isFinished[idx]:
        TAGS_LIST[idx] = load_tags(streams_ids[idx])
        request = youtube.videos().list(part="liveStreamingDetails", id=streams_ids[idx].split()[0])
        response = request.execute()
        try: #Check if privated and pass (set isFinished to True)
          date_time_str =response['items'][0]['liveStreamingDetails']['actualStartTime']
          start_time_utc[idx] = convert_date(date_time_str, offset_sec)
        except:
          process = Thread(target=save_state, args=[idx, True])
          process.start()
        
  
        
  client = commands.Bot(command_prefix='!')
  client.remove_command('help')
  @client.event
  async def on_ready():
    print(f'{client.user.name} has connected.')

###################### TRANSLATIONS PICK UP 
  def check_translation(video_id, channel):
    request = youtube.videos().list(part="liveStreamingDetails", id=video_id)
    response = request.execute()
    chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
    msg_list = []
    Stream_idx = STREAMS[channel.name]
    while not isFinished[Stream_idx]:
      print(channel.name)
      request_chat = youtube.liveChatMessages().list(liveChatId=chat_id, part="snippet")
      response_chat = request_chat.execute()
      for idx in range(len(response_chat['items'])):
        chat = response_chat['items'][idx]['snippet']['displayMessage']
        author_id = response_chat['items'][idx]['snippet']['authorChannelId']
        isTL = True in (chat.lower().startswith(pref.lower()) for pref in TL_prefix)
        if isTL:
          msg_id = response_chat['items'][idx]['id']
          if msg_id not in msg_list:
            msg_list.append(msg_id)
            #request_author = youtube.channels().list(id=author_id,part='snippet')
            #response_author = request_author.execute()
            #author = response_author['items'][0]['snippet']['title']
            client.dispatch('send_msg', channel, f'||{author_id}|| {chat}')
      sleep(3)

  @client.event
  async def on_send_msg(channel, msg):
    await channel.send('\N{Speech Balloon}' + msg)
    
################################## EDIT TAG
  @client.event
  async def on_message_edit(before, after):
    if '!t ' in before.content[:3]:
      if before.channel.name in STREAMS:
        source = TAGS_LIST[STREAMS[before.channel.name]] #TODO: Extraer de la DB?
        try:
          new_msg = after.content.split('!t ')[1]
          new_msg = new_msg.split("!adjust ")[0]
          if new_msg[-1:] == '\n' :
            new_msg = new_msg[:-1]
          ids = []
          msg_id = before.id
          for idx in source:
            ids.append(idx[3])
          if msg_id in ids: #Solo opera sobre tags anteriores
            msg_idx = ids.index(msg_id)
            msg_tag = source[msg_idx]
            msg_tag[1] = new_msg
            source[msg_idx] = msg_tag
            TAGS_LIST[STREAMS[before.channel.name]] = source
        except Exception as e:
          print('Error al editar la tag')
          print(e)
    
################################## REACTIONS
  @client.event
  async def on_raw_reaction_add(payload):
    reaction = payload.emoji
    channel = client.get_channel(payload.channel_id)
    user = client.get_user(payload.user_id)
    message = await channel.fetch_message(payload.message_id)
    if not user:
        user = await client.fetch_user(payload.user_id)
    if user.id == id_admin and message.author == client.user and str(reaction) =='❌': #Admin del bot elimina mensajes del mismo reaccionando con '❌':
      await message.delete()
    if user == client.user:
      return
    if channel.name in STREAMS:
      try:
        Stream_idx = STREAMS[channel.name]
        if streams_ids[Stream_idx]:
          id_data = TAGS_LIST[Stream_idx]
          ids = []
          msg_id = message.id
          for idx in id_data:
            ids.append(idx[3])
          if msg_id in ids: #Solo opera sobre tags anteriores
            msg_idx = ids.index(msg_id)
            if str(reaction) =='❌': 
              if user.id==message.author.id:
                del TAGS_LIST[Stream_idx][msg_idx]
                await message.delete()
              elif utils.get(user.roles, name=role_admin) or utils.get(user.roles, name=role_translator) or user.id == id_admin: #Roles y personas autorizadas:
                del TAGS_LIST[Stream_idx][msg_idx]
                await message.delete()
            if str(reaction) == '⭐': #Para hacer upvote a la tag
              msg_cont = TAGS_LIST[Stream_idx][msg_idx]
              msg_cont[2] = utils.get(message.reactions, emoji='⭐').count
              TAGS_LIST[Stream_idx][msg_idx] = msg_cont 
      except Exception as e:
        print(f'This is an exception: {e}')
        
######################################  COMANDS  ###############################################

  @client.command()
  async def hello(message):
    if message.author.id == id_admin:
      await message.channel.send('Hello Master!')
    else:
      await message.channel.send(f'Hi {message.author.mention}')

#################################### Force TL Pick up (In case of bot reset)
  @client.command()
  async def start_TL(message):
    if message.channel.name not in STREAMS:
      return
    Stream_idx = (STREAMS[message.channel.name])
    processThread[Stream_idx] = Thread(target=check_translation, args=[streams_ids[Stream_idx].split()[0], message.channel])
    processThread[Stream_idx].start()
    
#################################### SET STREAM
  @client.command()
  async def stream(message):
    if message.channel.name not in STREAMS:
      return
    Stream_idx = (STREAMS[message.channel.name])
    isPaused[Stream_idx] = False
    time_paused[Stream_idx] = 0
    total_time_paused[Stream_idx] = 0
    cmd = message.message.content.split()
    if len(cmd)!=2:
      await message.channel.send('Error en el URL del stream. Utilice: !stream «URL»')
      return
    link = cmd[1][-11::]
    source = link+f' {Names[Stream_idx]}'
    #if streams_ids[Stream_idx] == source:
    #  await message.channel.send(f"Este stream ya se encuentra configurado.")
    #  return
    request = youtube.videos().list(part="liveStreamingDetails", id=source.split()[0])
    response = request.execute()
    try:
      date_time_str =response['items'][0]['liveStreamingDetails']['actualStartTime']
      start_time_utc[Stream_idx] = convert_date(date_time_str, offset_sec)
      streams_ids[Stream_idx] = source
      isFinished[Stream_idx] = False
      process = Thread(target=save_id, args=[Stream_idx, streams_ids[Stream_idx]])
      process.start()
      TAGS_LIST[Stream_idx] = []
      #Start Threads for Translations
      processThread[Stream_idx] = Thread(target=check_translation, args=[link, message.channel])
      processThread[Stream_idx].start()
      await message.channel.send(f"Stream configurado correctamente")
    except IndexError:
      await message.channel.send("Error en el enlace.\nUtilice enlaces con el formato:\nhttps://www.youtube.com/watch?v=C7e1EJdtoCM\no\nhttps://youtu.be/C7e1EJdtoCM")
      await message.message.add_reaction('❌')
    except KeyError:
      await message.channel.send("Stream no activo, inténtelo más tarde.")
      await message.message.add_reaction('❌')
    
##################################### NEW TAG
  @client.command()
  async def t(message):
    if message.channel.name not in STREAMS:
      return
    msg = message.message
    Stream_idx = (STREAMS[message.channel.name])
    new_tag = msg.content.split('!t ')[1]
    if '|' in new_tag:
      await message.channel.send(f"No se permite el uso del símbolo: |")
      return
    #Para evitar tagear "adjust" por error (al inicio)
    #Y también aceptar un "!adjust" en el mismo mensaje después del tag 
    found = re.findall(r"((?:adjust )[-+]?[0-9])", new_tag, flags=re.IGNORECASE)
    hasAdjust = 0
    if found:
      if new_tag[0:7] == "adjust ":
        await message.channel.send(f"{msg.author.mention} Es !adjust, campeón")
        return
      else:
        try:
          hasAdjust = int(new_tag.split("!adjust ")[1])
          new_tag = new_tag.split("!adjust ")[0]
          if new_tag[-1:] == '\n' :
            new_tag = new_tag[:-1]
          await message.message.add_reaction('\N{Thumbs Up Sign}')
        except Exception as e:
          print(e)
          await message.channel.send("Error adjustando el tiempo. Tag no aceptada.")
          return
    if not isFinished[Stream_idx]:
      time_now = datetime.datetime.utcnow()
      time_now_utc = time_now.replace(tzinfo=pytz.utc)
      if not start_time_utc[Stream_idx]:
        start_time_utc[Stream_idx] = convert_date(start_time_utc[Stream_idx], offset_sec)
      if time_paused[Stream_idx]:
        secs = str(round((time_paused[Stream_idx] - start_time_utc[Stream_idx] - datetime.timedelta(seconds=total_time_paused[Stream_idx]) + datetime.timedelta(seconds=hasAdjust)).total_seconds()))
      else:
        secs = str(round((time_now_utc - start_time_utc[Stream_idx] - datetime.timedelta(seconds=total_time_paused[Stream_idx])+ datetime.timedelta(seconds=hasAdjust)).total_seconds()))
      TAGS_LIST[Stream_idx].append([secs, new_tag, 1, msg.id, msg.author.id]) #time, tag, upvotes, messageID, author
      process = Thread(target=save_tags, args=[streams_ids[Stream_idx], TAGS_LIST[Stream_idx]])
      process.start()
      await msg.add_reaction('⭐')
      await msg.add_reaction('❌')
    else:
      await message.channel.send("El stream anterior ha finalizado. Configure un nuevo stream con: !stream (URL del stream)")

##################################### PAUSE/RESUME TIME
  @client.command()
  async def movistar(message):
    if message.channel.name not in STREAMS:
      return
    Stream_idx = STREAMS[message.channel.name]
    if isPaused[Stream_idx]:
      total_time_paused[Stream_idx] = round((datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - time_paused[Stream_idx]).total_seconds()) + total_time_paused[Stream_idx]
      time_paused[Stream_idx] = 0
      await message.message.add_reaction('\N{Thumbs Up Sign}')
      await message.channel.send(f"Stream reanudado.")
    else:
      isPaused[Stream_idx] = True
      time_paused[Stream_idx] = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
      await message.message.add_reaction('\N{Thumbs Up Sign}')
      await message.channel.send(f"Stream pausado. Para reanudar vuelva a utilizar el comando: !movistar")
    
##################################### ADJUST TAG
  @client.command()
  async def adjust(message):
    if message.channel.name not in STREAMS:
      return
    Stream_idx = (STREAMS[message.channel.name])
    try:
      new_time = int(message.message.content.split()[1])
      author_data = TAGS_LIST[Stream_idx]
      authors = []
      msg_author = message.author.id
      for idx in author_data:
        authors.append(idx[4])
      if msg_author in authors: 
        authors.reverse()
        msg_idx = len(authors) - authors.index(msg_author) -1
        msg_cont = TAGS_LIST[Stream_idx][msg_idx]
        msg_cont[0] = str(int(msg_cont[0]) + new_time)
        TAGS_LIST[Stream_idx][msg_idx] = msg_cont 
        await message.message.add_reaction('\N{Thumbs Up Sign}')
    except Exception as e:
      print(e)
      await message.channel.send("Error ajustando el tiempo.")
      await message.message.add_reaction('❌')
      
##################################### OFFSET TAGS
  @client.command()
  async def offset(message): #Roles y personas permitidas:
    if message.channel.name not in STREAMS or not (utils.get(message.author.roles, name=role_admin) or utils.get(message.author.roles, name=role_translator) or message.author.id == id_admin):
      await message.channel.send("No tiene permisos.")
      await message.message.add_reaction('❌')
      return
    Stream_idx = (STREAMS[message.channel.name])
    try:
      if streams_ids[Stream_idx]:
        start_off = int(message.message.content.split()[1])
        num_off = int(message.message.content.split()[2])
        data = TAGS_LIST[Stream_idx]
        for idx in range(len(data)):
          if int(data[idx][0]) > start_off:
            data[idx][0] = str(int(data[idx][0]) + num_off)
            TAGS_LIST[Stream_idx][idx] = data[idx]
        if isFinished[Stream_idx]:
          process = Thread(target=save_tags, args=[streams_ids[Stream_idx], TAGS_LIST[Stream_idx]])
          process.start()
        await message.message.add_reaction('\N{Thumbs Up Sign}')
    except Exception as e:
      print(e)
      await message.channel.send("Error ajustando el tiempo.")
      await message.message.add_reaction('❌')
      
##################################### LIST TAG
  @client.command()
  async def tags(message):
    if message.channel.name in STREAMS:
      Stream_idx = STREAMS[message.channel.name]
    stream_source = ''
    tags_emb = ''
    isLocal = True
    cmd = message.message.content.split()
    if len(cmd)>1: #URL
      video_url = cmd[1][-11::]
      #Busqueda DataBase
      try: #Comprueba el url
        request = youtube.videos().list(part="liveStreamingDetails", id=video_url)
        response = request.execute()
        date_time_str =response['items'][0]['liveStreamingDetails']['actualStartTime']
        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
        start_time_utc_print = date_time_obj.replace(tzinfo=pytz.utc)
      except IndexError:
        #print('Error en el link.')
        await message.channel.send("Error en el enlace.\nUtilice enlaces con el formato:\nhttps://www.youtube.com/watch?v=C7e1EJdtoCM\no\nhttps://youtu.be/C7e1EJdtoCM")
        await message.message.add_reaction('❌')
        return
      except KeyError:
        #print('Stream no activo')
        await message.channel.send("El stream no existe.")
        await message.message.add_reaction('❌')
        return
      tags_emb = request_db(main_url + f"/tags?video_id={video_url}")
      if tags_emb:
        name = tags_emb.split("[")[0]
        tags_emb = tags_emb[len(name):]
        stream_source = video_url + " " + name
        isLocal = False
        num_tags = len(tags_emb.splitlines())
        Stream_idx = Names.index(name)
      else:
        await message.channel.send('No se encontraron tags en la base de datos')
        return
    else:
      stream_source = streams_ids[Stream_idx]
      request = youtube.videos().list(part="liveStreamingDetails", id=stream_source.split()[0])
      response = request.execute()
      date_time_str =response['items'][0]['liveStreamingDetails']['actualStartTime']
      date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%SZ")
      start_time_utc_print = date_time_obj.replace(tzinfo=pytz.utc)
      Stream_idx = Names.index(stream_source.split()[1])
      if not isFinished[Stream_idx]:
        #Revisa si el stream terminó:
        request = youtube.videos().list(part="contentDetails", id=stream_source.split()[0])
        response = request.execute()
        date_time_str = response['items'][0]['contentDetails']['duration']
        duration = isodate.parse_duration(date_time_str)
        secs = duration.total_seconds()
        if secs != 0 and not isFinished[Stream_idx]:
          process = Thread(target=save_state, args=[Stream_idx, True])
          process.start()
          isFinished[Stream_idx] = True
      tags_emb = format_tags(stream_source.split()[0], TAGS_LIST[Stream_idx], tags_emb)          
      num_tags = len(TAGS_LIST[Stream_idx])
    msg_len = len(tags_emb.split('|')) #Splitting message
    embed = Embed()
    start_time_jst = start_time_utc_print.astimezone(pytz.timezone(tz))
    start_data = start_time_jst.strftime("%H:%M:%S (JST) %a %d/%m/%Y")
    for idx in range(msg_len):
      if idx==0:
        if msg_len==1:
          embed.title = f'Tags de {Names[Stream_idx].capitalize()}'
        else:
          embed.title = f'Tags de {Names[Stream_idx].capitalize()} (1/{msg_len})'
        embed.description = f'https://www.youtube.com/watch?v={stream_source.split()[0]}\nHora de inicio: {start_data}\nTags: {num_tags}\n' + tags_emb.split('|')[idx]
        await message.channel.send(embed=embed)
      else:
        embed.title = f'Tags de {Names[Stream_idx].capitalize()}({idx+1}/{msg_len})'
        embed.description = tags_emb.split('|')[idx]
        await message.channel.send(embed=embed)          

##################################### STREAM TIME
  @client.command()
  async def time(message):
    if message.channel.name not in STREAMS:
      return
    Stream_idx = (STREAMS[message.channel.name])
    if streams_ids[Stream_idx]:
      request = youtube.videos().list(
        part="contentDetails",
        id=streams_ids[Stream_idx].split()[0])
      response = request.execute()
      date_time_str = response['items'][0]['contentDetails']['duration']
      duration = isodate.parse_duration(date_time_str)
      secs = duration.total_seconds()       
      if secs == 0:
        time_now = datetime.datetime.utcnow()
        time_now_utc = time_now.replace(tzinfo=pytz.utc)
        start_time_utc_print = start_time_utc[Stream_idx] - datetime.timedelta(seconds=offset_sec) #Actual start time (no offset)
        secs = round((time_now_utc - start_time_utc_print - datetime.timedelta(seconds=total_time_paused[Stream_idx])).total_seconds())
      elif not isFinished[Stream_idx]:
        process = Thread(target=save_state, args=[Stream_idx, True])
        process.start()
        isFinished[Stream_idx] = True
      aux2 = format_time_output(secs)
      if isFinished[Stream_idx] == True:
        await message.channel.send(f"El stream de {Names[Stream_idx].capitalize()} ha finalizado con una duración de {aux2}")
      else:
        await message.channel.send(f"{Names[Stream_idx].capitalize()} lleva {aux2} de stream")
    else:
      await message.channel.send("Stream no configurado")

##################################### FIND  
      ##Mejoras: TODO: (Regex) Buscar citas de tags como: !t "Quote" /!t Misora: Quote /!t M: "Quote"
  def find_func(mats_emb, text, tags, stream_id): # (Lista de encuentros, Texto a buscar, Tags para buscar, ID video)
    for idx in tags:
      if text.lower() in idx[1].lower():
        secs = int(idx[0])
        aux2 = format_time_output(secs)
        timestamp = 'https://www.youtube.com/watch?v='+stream_id+'&t='+str(secs)
        mats_emb = mats_emb + f"[{aux2}]({timestamp}) " + idx[1] + '\n'
    return mats_emb
    
  @client.command()
  async def find(message):
    cmd = message.message.content.split()
    if message.channel.name not in STREAMS and len(cmd)<3: #Can be used outside Streams channels only with optional argument: len(cmd)==3
      return
    if len(cmd)==1:
      await message.channel.send('Falta el texto de búsqueda.')
      await message.message.add_reaction('❌')
      return
    arg = cmd[1]
    if (arg[0] == '-') and (arg[1:].lower() in Names): #Optional argument used
      if len(cmd)>2:
        Stream_idx = Names.index(arg[1:].lower())
        text = message.message.content.split(arg+' ')[1]
      else:
        await message.channel.send('Falta el texto de búsqueda dentro de los tags de "{arg}".')
        await message.message.add_reaction('❌')
    else:
      Stream_idx = (STREAMS[message.channel.name])
      text = message.message.content.split("!find ")[1]
    mats_emb = ''
    mats_emb = find_func(mats_emb, text, TAGS_LIST[Stream_idx], streams_ids[Stream_idx].split()[0])
    embed = Embed()
    embed.title = f'Resultados de la búsqueda de "{text}":'
    embed.description = mats_emb
    #TODO: Function to split embed message when its length exceeds the maximum allowed
    await message.channel.send(embed=embed)
      
##################################### FIND ALL
  @client.command()
  async def findall(message):
    cmd = message.message.content.split()
    name = message.channel.name
    if name not in STREAMS and len(cmd)<3:
        return
    if len(cmd)==1:
        await message.channel.send('Falta el texto de búsqueda.')
        await message.message.add_reaction('❌')
        return
    arg = cmd[1]
    if (arg[0] == '-') and (arg[1:].lower() in Names): #Optional argument used
      if len(cmd)>2:
        Stream_idx = Names.index(arg[1:].lower())
        text = message.message.content.split(arg+' ')[1]
      else:
        await message.channel.send('Falta el texto de búsqueda dentro de los tags de "{arg}".')
        await message.message.add_reaction('❌')
        return
    else:
      Stream_idx = STREAMS[name]
      text = message.message.content.split('!findall ')[1]
    text = quote(text)
    try:
      mats_emb = request_db(main_url + f"/findall?text={text}&name={Stream_idx}") 
    except:
      await message.channel.send('Base de datos inactiva. Vuelva a intentarlo en unos minutos.')
      return
    embed = Embed()
    text = unquote(text)
    embed.title = f'Resultados de la búsqueda de "{text}":'
    embed.description = mats_emb
    #TODO: Function to split embed message when its length exceeds the maximum allowed
    await message.channel.send(embed=embed)

##################################### RANK
  @client.command()
  async def rank(message):
    #if not (utils.get(message.author.roles, name=role_admin) or utils.get(message.author.roles, name=role_translator) or message.author.id == id_admin):
    #  await message.channel.send("No tiene permisos.")
    #  await message.message.add_reaction('❌')
    #  return
    try:
      sorted_rank = request_db(main_url + "/rank")
    except:
      await message.channel.send('Base de datos inactiva. Vuelva a intentarlo en unos minutos.')
      return
    sorted_rank = json.loads(sorted_rank)
    guild = client.get_guild(message.guild.id)
    i = 1
    strng = ''
    for key, value in sorted_rank.items():
      user_name = (await client.fetch_user(key)).name
      try:
        nick_name = (await guild.fetch_member(key)).nick
        if nick_name is not None:
          user_name = nick_name 
      except:
        pass          
      strng += f'#{i} {user_name}: {value} tags\n'
      i +=1
      if i > 10:
        break
    embed = Embed()
    embed.title = f'Ranking de Taggers'
    embed.description = strng
    await message.channel.send(embed=embed)
    
##################################### HELP
  @client.command()
  async def help(message):
    embed = Embed()
    text_channel = client.get_channel(876979402284609546) #stream-tags channel ID
    mats_emb = f"• MeidochanTagger recopila etiquetas con el comando: `!t`\n• Al final del stream, las etiquetas con timestamps se pueden ver en el canal {text_channel.mention}\n• [Manual del bot](https://github.com/DovaSubs/MeidochanTagger#readme) "
    #embed.title = 'Help'
    embed.description = mats_emb
    await message.channel.send(embed=embed)

  #Bot TOKEN in .env file (it's possible to use plain text) 
  client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
  main()
