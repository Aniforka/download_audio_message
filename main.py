from requests import get
import os
from glob import glob

#-----------------------------------------

def getHistory(offset, peer_id, access_token):
    messages_getHistory = 'https://api.vk.com/method/messages.getHistory'
    count = 200
    rev = 1
    v = '5.124'
    params_message_getHistory = {
        'offset':offset,
        'count':count,
        'peer_id':peer_id,
        'rev':rev,
        'v':v,
        'access_token':access_token
    }
    res = get(url=messages_getHistory, params=params_message_getHistory).json

    return res

def get_name(id, access_token):
    user_get = 'https://api.vk.com/method/users.get'
    v = '5.124'
    params_get = {
        'user_ids':id,
        'fields':'first_name, last_name',
        'v':v,
        'access_token':access_token
    }
    res = get(url=user_get, params=params_get).json
    first_name = res()['response'][0]['first_name']
    last_name = res()['response'][0]['last_name']
    name = first_name + ' ' + last_name

    return name

def download(url, name):
    os.chdir(os.path.join(path, 'c' + str(peer_id - 2000000000)))
    try:
        os.mkdir(name)
    except:
        os.chdir(os.path.join(os.getcwd(),name))
        number = len(glob(os.path.join(os.getcwd(),'*.mp3')))
        number = str(number+1)
        with open(number+'.mp3', 'wb') as f:
            f.write(get(url).content)
    else:
        os.chdir(os.path.join(os.getcwd(),name))
        with open('1.mp3', 'wb') as f:
            f.write(get(url).content)

#-----------------------------------------
chatid = '' #айди чата/диалога
peer_id = 2000000000 + int(chatid)
access_token = '' #токен от страницы вк
path = os.path.abspath(__file__) #путь к папке с кодом

try:
    os.mkdir(os.path.join(path, 'c' + str(peer_id - 2000000000)))
except:
    pass
k = 0
offset = 0
res = getHistory(offset, peer_id, access_token)
count = int(res()['response']['count'])
print('Всего сообщений в чате', count)


with open(os.path.join(path, 'c' + str(peer_id - 2000000000), 'info.txt'), 'a') as f_out:
    f_out.write('ID чата: ' + str(peer_id - 2000000000) + '\nСообщений в чате: ' + str(count) + '\n')


while(offset < count):
    res = getHistory(offset, peer_id, access_token)
    messages = res()['response']['items']
    for message in messages:
        attachments = message['attachments']
        for attachment in attachments:
            if(attachment['type'] == 'audio_message'):
                url = attachment['audio_message']['link_mp3']
                id = attachment['audio_message']['owner_id']
                name = get_name(id, access_token)
                download(url, name)
                k += 1
                print('Голосовое номер', k)

    offset += 200

print('Из', count, 'сообщений голосовыми оказались', k)

with open(os.path.join(path, 'c' + str(peer_id - 2000000000), 'info.txt'), 'a') as f_out:
    f_out.write('Голосовыми оказались ' + str(k))
