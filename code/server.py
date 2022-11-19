####################################################
#  D1014636 潘子珉                                      									
####################################################
from flask import Flask, json, request, jsonify
import time
import threading

PORT = 5050
POST_FILE = 'posts.json'
USER_FILE = 'users.json'
USERS = []
POSTS = []

API = Flask(__name__)
lock = threading.Lock()

def find_next_topic_id():
    if len(POSTS) == 0:
        return 0
    return max(post["id"] for post in POSTS) + 1

def find_next_reply_id(postId):
    for post in POSTS:
        if post['id'] == postId:
            if len(post['reply']) == 0:
                return 0
            return max(reply["id"] for reply in post['reply']) + 1

def isUsernameAlreadyExist(username):
    lock.acquire()
    for user in USERS:
        if user['username'] == username:
            lock.release()
            return (True, user)
    lock.release()
    return (False, None)

def find_topic_by_id(postId):
    for post in POSTS:
        if post['id'] == postId:
            return post
    return None

def find_reply_by_id(post, replyId):
    for reply in post['reply']:
        if reply['id'] == replyId:
            return reply
    return None

@API.route("/register", methods=['POST'])
def register():
    if request.is_json:
        newUser = request.get_json()
        if newUser['username'] == None:
            return {"error": "username not found"}, 400
        if isUsernameAlreadyExist(newUser['username'])[0]:
            return {"error": "username already exists"}, 400
        lock.acquire()
        USERS.append(newUser)
        with open(USER_FILE, 'w') as wfp:
            json.dump(USERS, wfp)
        lock.release()
        return newUser, 201
    else:
    	return {"error": "Request must be JSON"}, 415

@API.route("/login", methods=['POST'])
def login():
    if request.is_json:
        newUser = request.get_json()
        if newUser['username'] == None:
            return {"error": "username not found"}, 400
        state = isUsernameAlreadyExist(newUser['username'])
        if not state[0]:
            return {"error": "username not exists"}, 400
        return state[1], 201
    else:
    	return {"error": "Request must be JSON"}, 415

@API.route("/create", methods=['POST'])
def create():
    if request.is_json:
        newPost = request.get_json()
        if newPost['owneUsername'] == None or newPost['topic'] == None or newPost['content'] == None:
            return {"error": "paramas not found"}, 400
        lock.acquire()
        newPost["id"] = find_next_topic_id()
        lock.release()
        newPost["reply"] = []
        newPost["time"] = time.time()
        lock.acquire()
        POSTS.append(newPost)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
        lock.release()
        return newPost, 201
    else:
    	return {"error": "Request must be JSON"}, 415


@API.route("/subject", methods=['GET','POST'])
def subject():
    topics = []
    lock.acquire()
    for post in POSTS:
        topics.append({
            'topic':post['topic'],
            'id':post['id'],
            'numOfReply':len(post['reply'])
        })
    lock.release()
    return jsonify(topics)


@API.route("/reply", methods=['POST'])
def reply():
    postId = request.args.get('postId')
    if postId == None:
        return {"error": "paramas postId not found"}, 400
    postId = int(postId)
    post = None
    lock.acquire()
    for p in POSTS:
        if p['id'] == postId:
            post = p
    lock.release()
    if post == None:
        return {"error": "postId is unavailable"}, 404
    if request.is_json:
        newReply = request.get_json()
        if newReply['owneUsername'] == None or newReply['content'] == None:
            return {"error": "paramas not found"}, 400
        newReply["time"] = time.time()
        lock.acquire()
        newReply["id"] = find_next_reply_id(postId)
        post['reply'].append(newReply)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
        lock.release()
        return newReply, 201
    else:
    	return {"error": "Request must be JSON"}, 415

@API.route("/discussion", methods=['GET','POST'])
def discussion():
    postId = request.args.get('postId')
    if postId == None:
        return {"error": "paramas postId not found"}, 400
    postId = int(postId)
    lock.acquire()
    for p in POSTS:
        if p['id'] == postId:
            lock.release()
            return jsonify(p)
    lock.release()
    return {"error": "postId is unavailable"}, 404

@API.route("/delete", methods=['DELETE','POST'])
def delete():
    body = request.get_json()
    if body['type'] == None or body['postId'] == None or body['loginedUsername'] == None:
        return {"error": "paramas not found"}, 400
    if body['type'] == 'post':
        lock.acquire()
        post = find_topic_by_id(int(body['postId']))
        if post['owneUsername'] != body['loginedUsername']:
            lock.release()
            return {"error": "you can't delete not yours post"}, 400
        POSTS.remove(post)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
        lock.release()
        return {} ,200
    elif body['type'] == 'reply':
        lock.acquire()
        post = find_topic_by_id(int(body['postId']))
        reply = find_reply_by_id(post, int(body['replyId']))
        if reply['owneUsername'] != body['loginedUsername']:
            lock.release()
            return {"error": "you can't delete not yours reply"}, 400
        post['reply'].remove(reply)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
        lock.release()
        return {} ,200
    return {"error": "type must be reply or post"}, 400

with open(USER_FILE, encoding='utf-8') as fp:
	USERS = json.load(fp)

with open(POST_FILE, encoding='utf-8') as fp:
	POSTS = json.load(fp)
	
API.run(host='127.0.0.1', port=PORT, debug=True, threaded=True)