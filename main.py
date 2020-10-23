import vk_api
import time
import telebot
import io
import requests

bot_token=''
vk_community_id=-
vk_token=''
telegram_id_channel='@'


vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()

post_count_before = vk.wall.get(owner_id=vk_community_id).get("count")

def send_message_to_channel(post_text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
    data = {'chat_id' : telegram_id_channel, "text" : post_text}
    r= requests.post(url,data=data)
    return r

def send_photo_to_channel(img_url,post_text=""):
    url = "https://api.telegram.org/bot{}/sendPhoto".format(bot_token)
    remote_image = requests.get(img_url)
    photo = io.BytesIO(remote_image.content)
    photo.name = 'img.png'
    files = {'photo': photo}
    data = {'chat_id' : telegram_id_channel, "caption" : post_text}
    r= requests.post(url, files=files, data=data)
    return r

def get_post_count(vk_community_id):
    global post_count
    post_count=vk.wall.get(owner_id=vk_community_id).get("count")


while True:
    post_text=""
    get_post_count(vk_community_id=vk_community_id)
    if post_count_before < post_count:
        if vk.wall.get(owner_id=vk_community_id).get("items")[1].get("attachments")!=None:
            last_post = vk.wall.get(owner_id=vk_community_id).get("items")[0].get("is_pinned")
            
            if last_post == 1:
                img_url=(vk.wall.get(owner_id=vk_community_id).get("items")[1].get("attachments")[0].get("photo").get("sizes")[-1].get("url"))
                post_text=(vk.wall.get(owner_id=vk_community_id).get("items")[1].get("text"))
                
            elif last_post==None:
                img_url=(vk.wall.get(owner_id=vk_community_id).get("items")[0].get("attachments")[0].get("photo").get("sizes")[-1].get("url"))
                post_text=(vk.wall.get(owner_id=vk_community_id).get("items")[0].get("text"))
            send_photo_to_channel(img_url=img_url,post_text=post_text)
    

        elif vk.wall.get(owner_id=vk_community_id).get("items")[1].get("attachments")==None:
            last_post = vk.wall.get(owner_id=vk_community_id).get("items")[0].get("is_pinned")
            
            if last_post == 1:
                post_text=(vk.wall.get(owner_id=vk_community_id).get("items")[1].get("text"))
                
            elif last_post==None:
                post_text=(vk.wall.get(owner_id=vk_community_id).get("items")[0].get("text"))
            send_message_to_channel(post_text=post_text)
        
        post_count_before+=1
    time.sleep(180)
