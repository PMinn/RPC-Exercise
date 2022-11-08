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

def register():
	new_dict = {"username":"789"}
	response = requests.post(URI+'/register', json=new_dict)
	print(response.status_code)
	print(response.headers)
	print(response.text)

def create():
	new_dict = {"owneUsername":"789","topic":"1tit","content":"con"}
	response = requests.post(URI+'/create', json=new_dict)
	print(response.status_code)
	print(response.headers)
	print(response.text)

@eel.expose
def subject():
	response = requests.post(URI+'/subject')
	print(response.status_code)
	print(response.headers)
	print(response.text)
	return response.text

def reply():
	new_dict = {"owneUsername":"789","content":"con"}
	response = requests.post(URI+'/reply', params = {"postId":1},json=new_dict)
	print(response.status_code)
	print(response.headers)
	print(response.text)

'''
	if(sys.argv[3] == 'all'):
		# Query without parameter
		response = requests.get(URL)
		print(response.status_code)
		print(response.headers)
		print(response.text)		# response.text is a text string
	elif(sys.argv[3] == 'add'):
		# Post record
		print('Add new company')
		new_comp = input('Company name: ')
		new_city = input('City of the company: ')
		new_dict = {}
		new_dict["name"] = new_comp
		new_dict["city"] = new_city
		response = requests.post(URL, json=new_dict)
		print(response.status_code)
		print(response.headers)
		print(response.text)
	elif(sys.argv[3] == 'update'):
		print('Update a record')
		new_dict = {}
		new_dict['id'] = int(input('ID: '))
		new_dict["name"] = input('Company name: ')
		new_dict["city"] = input('City of the company: ')
		response = requests.put(URL, json=new_dict)
		print(response.status_code)
		print(response.headers)
		print(response.text)		
	elif(sys.argv[3] == 'query'):
		# Query with parameter
		city = input('City of the company: ')
		my_params = {}
		my_params["city"] = city
		response = requests.get(URL, params = my_params)
		print(response.status_code)
		print(response.headers)
		json_rec = response.json()				# response.json() is json records
		print('There are %d records' % len(json_rec)) 
		for item in json_rec:
			print('ID: %d, Company Name: %s, City: %s' % (item['id'], item['name'], item['city']))
	else:
		print("Usage: python3 7-RESTClient.py serverIP port cmd (cmd = all, add, update, query) ")
'''
eel.start('index.html', size=(1000, 1000), port=0)