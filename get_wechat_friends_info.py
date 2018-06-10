# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 19:02:06 2018

@author: Leo
"""

import itchat
import json
import requests
import codecs

sex_dict = {'0':'这些人都不写性别的', '1':'帅气的小伙子们', '2':'漂亮的小姐姐们'}

#下载微信好友头像图片
def download_images(friend_list):
    image_dir = "D:/Leo/Projects/wechatfriendsanalysis/images/"
    #num = 1
    for friend in friend_list:
        image_name = friend['NickName']+'.jpg'
        #num+=1
        img = itchat.get_head_img(userName=friend['UserName'])
        with open(image_dir+image_name, 'wb') as file:
            file.write(img)

#保存微信好友信息            
def save_data(friend_list):
    out_file_name = "D:/Leo/Projects/wechatfriendsanalysis/data/friends.json"
    with codecs.open(out_file_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(friend_list, ensure_ascii=False))

#通过图灵api实现消息自动回复
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {'key' : '1107d5601866433dba9599fac1bc0083',
        'info': msg,
        'userid': u'Leo\'s rebot'}
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

#获取微信文本信息
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I get it:'+msg['Text']
    reply = get_response(msg['Text'])
    return reply or defaultReply

if __name__ == '__main__':
    itchat.auto_login()
    friends = itchat.get_friends(update=True)[0:]
    friends_list = []
    for friend in friends:
        item = {}
        item['NickName'] = friend['NickName']
        item['HeadImgUrl'] = friend['HeadImgUrl']
        item['Sex'] = sex_dict[str(friend['Sex'])]
        item['Province'] = friend['Province']
        item['Signature'] = friend['Signature']
        item['UserName'] = friend['UserName']
        item['City'] = friend['City']+'市'
        friends_list.append(item)
    save_data(friends_list)
    download_images(friends_list)
    user = itchat.search_friends(name=u'ATM')

#这是我自己的微信小号，用来测试信息发送功能，日后也许会做成一个自动聊天机器人
    itchat.send(u'运行完成啦~~!', user[0]['UserName'])
    itchat.run()