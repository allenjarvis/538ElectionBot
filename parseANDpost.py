from lxml import html
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from twython import Twython
import logging

logging.basicConfig()

#sets twitter api keys... please don't steal my shit! Please!
CONSUMER_KEY = 'y7uybSTbSXyHkve16gHaAgObI'
CONSUMER_SECRET = 'gjSMPeCpletnARVihBl4hlYOTUMNsb5mTaU0pOr6eU89QvK0Lo'
ACCESS_KEY = '781536298506985476-nBrmnvlkOf4F6HPEHK6AWOCyyPSLAfO'
ACCESS_SECRET = 'KqOnzmQEfyGOhuqEft4t8XyALEp5XsEw6A40qh8W6l9DU'
twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

#test for ints
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#no idea what this shit does... methinks this function returns something super trippy
sched = BlockingScheduler()

#this shit either
@sched.scheduled_job('interval', minutes=1)
def timed_job():
	#get last update tweet, find the second '%'
	tweetcounter = 1
	idx = 0
	last = "NaN"
	while not RepresentsInt(last[idx-4:idx-2]) and not RepresentsInt(last[idx+5:idx+7]):
		user_timeline = twitter.get_user_timeline(screen_name="electionbot538", count=tweetcounter, include_retweets=False)
		for tweet in user_timeline:
			idx = 0
			last = tweet['text']
			while last[idx] != '%' and idx<len(last)-1:
				idx += 1
			idx += 1
			while last[idx] != '%' and idx<len(last)-1:
				idx += 1
		tweetcounter += 1

	#set old values based on distance from second '%'
	if last[0]=='C':
		Hillary = last[idx-4:idx]
		Donald = last[idx+5:idx+9]
	if last[0]=='D':
		Donald = last[idx-4:idx]
		Hillary = last[idx+5:idx+9]
	print 'Hillary: ' + Hillary
	print 'Donald: ' + Donald

	#get new values for Hillary and Donald from 538's site, print to log
	page = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
	tree = html.fromstring(page.content)
	HillaryNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/p[2]/text()')[0]
	DonaldNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/p[2]/text()')[0]
	print 'HillaryNew: ' + HillaryNew
	print 'DonaldNew: ' + DonaldNew

	#if values have changed post to Twitter
	#case: tied
	if DonaldNew==HillaryNew:
		AllEven = "They're tied, folks. @FiveThirtyEight #Clinton #Trump #538 #election2016"
		twitter.update_status(status=AllEven)
		print AllEven
	#case: Hillary up
	elif float(HillaryNew)>float(Hillary):
		gain = str(float(HillaryNew) - float(Hillary))
		if float(HillaryNew)>float(DonaldNew):
			leadstrails = 'leads'
		else:
			leadstrails = 'trails'
		HillaryUP = 'Clinton gained ' + gain + '%! She now ' + leadstrails + ' Donald ' + HillaryNew + '% to ' + DonaldNew + "% in the @FiveThirtyEight polls-only forecast. #Clinton #Trump #538 #election2016"
		twitter.update_status(status=HillaryUP)
		print HillaryUP
	#case: Donald up
	elif float(DonaldNew)>float(Donald):
		gain = str(float(DonaldNew) - float(Donald))
		if float(DonaldNew)>float(HillaryNew):
			leadstrails = 'leads'
		else:
			leadstrails = 'trails'
		DonaldUP = 'Donald gained ' + gain + '%. He now ' + leadstrails + ' Clinton ' + DonaldNew + '% to ' + HillaryNew + "% in the @FiveThirtyEight polls-only forecast. #Clinton #Trump #538 #election2016"
		twitter.update_status(status=DonaldUP)
		print DonaldUP
	#case: no change
	else:
		print "No Change"

#makes scheduler run???
sched.start()
