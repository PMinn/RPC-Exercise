####################################################
#  D1014636 潘子珉                                      									
####################################################
import sys
import requests
import json
import eel

eel.init('gui', allowed_extensions=['.js', '.html'])

PORT = 5050
hostname = '127.0.0.1'
URI = f'http://{hostname}:{PORT}'

isLogin = False
loginedUsername = ""

lastViewPost = None

@eel.expose
def init():
    return {"isLogin":isLogin,"loginedUsername":loginedUsername,"lastViewPost":lastViewPost}

@eel.expose
def setLastViewPost(postId):
	global lastViewPost
	lastViewPost = postId

@eel.expose
def register(username):
	global isLogin
	global loginedUsername
	response = requests.post(URI+'/register', json={"username":username})
	print(response.status_code)
	print(response.status_code == 201)
	if response.status_code == 201:
		isLogin = True
		loginedUsername = username
	return {"code":response.status_code,"text":response.text}

@eel.expose
def login(username):
	global isLogin
	global loginedUsername
	response = requests.post(URI+'/login', json={"username":username})
	print(response.status_code)
	print(response.status_code == 201)
	if response.status_code == 201:
		isLogin = True
		loginedUsername = username
	return {"code":response.status_code,"text":response.text}

@eel.expose
def create(data):
	data['owneUsername'] = loginedUsername
	response = requests.post(URI+'/create', json=data)
	print(response.status_code)
	print(response.headers)
	print(response.text)
	return {"code":response.status_code,"text":response.text}

@eel.expose
def subject():
	response = requests.post(URI+'/subject')
	print(response.status_code)
	# print(response.headers)
	print(response.text)
	return response.text

@eel.expose
def reply(postId, content):
    print(loginedUsername)
    new_dict = {"owneUsername":loginedUsername,"content":content}
    response = requests.post(URI+'/reply', params = {"postId":postId},json=new_dict)
    print(response.status_code)
    print(response.headers)
    print(response.text)
    return {"code":response.status_code,"text":response.text}

@eel.expose
def discussion(postId):
    response = requests.get(URI+'/discussion', params = {"postId":postId})
    print(response.status_code)
    print(response.headers)
    print(response.text)
    return {"code":response.status_code,"text":response.text}

@eel.expose
def delete(json):
    json['loginedUsername'] = loginedUsername
    response = requests.delete(URI+'/delete', json = json)
    print(response.status_code)
    print(response.headers)
    print(response.text)
    return {"code":response.status_code,"text":response.text}

eel.start('index.html', size=(1000, 1000), port=0)