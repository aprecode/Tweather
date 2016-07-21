from flask import Flask, url_for,request
import urllib2
import json
from TwitterAPI import TwitterAPI

API_URL = "http://api.wunderground.com/api/38f0cc8295058de8/conditions/q/"

# Application is not logging in for individual twitter accounts
# Information for the sections below can be gotten from dev.twitter.com
'''
consumer_key = 
consumer_secret = 
access_token_key  = 
access_token_secret =

''' 

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

app = Flask(__name__)


def weather_condition(location):
	req = urllib2.Request(API_URL+location+".json")
	res = urllib2.urlopen(req).read()
	info = json.loads(res)
	temp = info["current_observation"]["temp_c"]
	status = info["current_observation"]["weather"]
	return {"temp": temp,"status" : status}


def weather_tweet(location):
	whe = weather_condition(location)
	temp = whe["temp"]
	status = whe["status"]
	last = location[0].upper() + location[1:] + " weather report\n" + "Temperature: " + str(temp) + "\n" + "Status: " + status
	r = api.request('statuses/update', {'status': last})
	print('SUCCESS') if r.status_code == 200 else ('FAILURE')



@app.route("/", methods=['GET','POST'])
def hello():
	if request.method == 'POST':
		loc = request.form.get('location')
		weather_tweet(loc)
		return "kk"
	return """
    	<form action='/' method='POST'>
    	<input style='width:300px;height:70px' name='location' type='text'>
    	<input type = 'submit'> 
    	</input>
    	</form>
    	"""







if __name__ == "__main__":
    app.run()



