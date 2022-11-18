####################################################
#  D1014636 潘子珉                                      									
####################################################
from flask import Flask, json, request, jsonify

PORT = 5050
POST_FILE = 'posts.json'
USER_FILE = 'users.json'
USERS = []
POSTS = []

API = Flask(__name__)

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
    for user in USERS:
        if user['username'] == username:
            return (True, user)
    return (False, None)

def find_topic_by_id(postId):
    for post in POSTS:
        if post['id'] == postId:
            return post
    return None

@API.route("/register", methods=['POST'])
def register():
    if request.is_json:
        newUser = request.get_json()
        if newUser['username'] == None:
            return {"error": "username not found"}, 400
        if isUsernameAlreadyExist(newUser['username'])[0]:
            return {"error": "username already exists"}, 400
        USERS.append(newUser)
        with open(USER_FILE, 'w') as wfp:
            json.dump(USERS, wfp)
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
        newPost["id"] = find_next_topic_id()
        newPost["reply"] = []
        POSTS.append(newPost)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
        return newPost, 201
    else:
    	return {"error": "Request must be JSON"}, 415


@API.route("/subject", methods=['GET','POST'])
def subject():
    topics = []
    for post in POSTS:
        topics.append({
            'topic':post['topic'],
            'id':post['id'],
            'numOfReply':len(post['reply'])
        })
    return jsonify(topics)


@API.route("/reply", methods=['POST'])
def reply():
    postId = request.args.get('postId')
    if postId == None:
        return {"error": "paramas postId not found"}, 400
    postId = int(postId)
    post = None
    for p in POSTS:
        if p['id'] == postId:
            post = p
    if post == None:
        return {"error": "postId is unavailable"}, 404
    if request.is_json:
        newReply = request.get_json()
        if newReply['owneUsername'] == None or newReply['content'] == None:
            return {"error": "paramas not found"}, 400
        newReply["id"] = find_next_reply_id(postId)
        post['reply'].append(newReply)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
        return newReply, 201
    else:
    	return {"error": "Request must be JSON"}, 415

@API.route("/discussion", methods=['GET','POST'])
def discussion():
    postId = request.args.get('postId')
    if postId == None:
        return {"error": "paramas postId not found"}, 400
    postId = int(postId)
    for p in POSTS:
        if p['id'] == postId:
            return jsonify(p)
    return {"error": "postId is unavailable"}, 404

@API.route("/delete", methods=['DELETE','POST'])
def delete():
    body = request.get_json()
    if body['type'] == None or body['postId'] == None:
        return {"error": "paramas not found"}, 400
    if body['type'] == 'post':
        post = find_topic_by_id(int(body['postId']))
        if len(post['reply']) > 0:
            return {"error": "post has reply"}, 400
        POSTS.remove(post)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
    elif body['type'] == 'reply':
        post = find_topic_by_id(int(body['postId']))
        POSTS.remove(post)
        with open(POST_FILE, 'w') as wfp:
            json.dump(POSTS, wfp)
'''
    paramUsername = request.args.get('username')
    print(paramUsername)
    newUser = {'username':paramUsername}
    if(paramUsername == None):
        return {"error": "username not found"}, 400
    with open(USER_FILE) as fp:
        USERS = json.load(fp)
    for user in USERS:
        if user['username'] == paramUsername:
            return {"error": "username already exists"}, 400
    USERS.append(newUser)
    with open(COMP_FILE, 'w') as wfp:
        json.dump(COMPANIES, wfp)
    return newUser, 201

@API.get("/register")
def register():
	param = request.args.get('city')
	print(param)
	if(param == None):				# no parameters
		return jsonify(COMPANIES)
	else:
		RET_COMP = []
		for i in range(len(COMPANIES)):
			if(COMPANIES[i]['city'] == param):
				RET_COMP.append(COMPANIES[i])
		return jsonify(RET_COMP)
# end of get_companies()

@API.post("/companies")
def add_companies():
    if request.is_json:
        new = request.get_json()
        new["id"] = find_next_id()
        COMPANIES.append(new)
        with open(COMP_FILE, 'w') as wfp:
        	json.dump(COMPANIES, wfp)
        return new, 201
    else:
    	return {"error": "Request must be JSON"}, 415
# end of add_companies()

@API.put("/companies")
def update_companies():
    if request.is_json:
        new = request.get_json()
        new_id = int(new["id"]) -1			# index begin from 0
        if(new_id >= len(COMPANIES)):
        	return {"error": "ID out of  range"}, 400
        COMPANIES[new_id] = new
        with open(COMP_FILE, 'w') as wfp:
        	json.dump(COMPANIES, wfp)
        return new, 201
    else:
    	return {"error": "Request must be JSON"}, 415
# end of update_companies()
'''


with open(USER_FILE, encoding='utf-8') as fp:
	USERS = json.load(fp)

with open(POST_FILE, encoding='utf-8') as fp:
	POSTS = json.load(fp)
	
API.run(host='127.0.0.1', port=PORT, debug=True)