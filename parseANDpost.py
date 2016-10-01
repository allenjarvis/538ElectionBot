from lxml import html
import requests
from TwitterAPI import TwitterAPI
from apscheduler.schedulers.blocking import BlockingScheduler

#sets twitter api keys... please don't steal my shit! Please!
api = TwitterAPI('y7uybSTbSXyHkve16gHaAgObI',
                 'gjSMPeCpletnARVihBl4hlYOTUMNsb5mTaU0pOr6eU89QvK0Lo',
                 '781536298506985476-nBrmnvlkOf4F6HPEHK6AWOCyyPSLAfO',
                 'KqOnzmQEfyGOhuqEft4t8XyALEp5XsEw6A40qh8W6l9DU')

#no idea what this shit does... methinks this function returns something super trippy
sched = BlockingScheduler()

#this shit either
@sched.scheduled_job('interval', minutes=1)
def timed_job():
	#get old values for Hillary and Donald from current.txt, print to log
	current = open("current.txt", 'r')
	Hillary = current.readline()[0:-1]
	Donald = current.readline()[0:-1]
	current.close
	print 'Hillary: ' + Hillary
	print 'Donald: ' + Donald

	#get new values for Hillary and Donald from 538's site, print to log
	page = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
	tree = html.fromstring(page.content)
	HillaryNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/p[2]/text()')[0]
	DonaldNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/p[2]/text()')[0]
	print 'HillaryNew: ' + HillaryNew
	print 'DonaldNew: ' + DonaldNew

	#set current values to 538's values if current values are "00.1"
	#(this means that application was redeployed since last time script was run)
	if Hillary == "00.1" and Donald == "00.1":
		print "values reset"
		current = open("current.txt", 'w')
		current.write(HillaryNew + '\n' + DonaldNew + '\n')
		current.close
	#if values have changed post to Twitter
	else:
		if float(HillaryNew) > float(Hillary):
			#post
			HillaryUP = 'Hillary is gaining! Likelihood of a Clinton win went from ' + Hillary + '% to ' + HillaryNew + '%. #Clinton'
			r = api.request('statuses/update', {'status': HillaryUP})
			print 'SUCCESS' if r.status_code == 200 else 'FAILURE'
			#set current values
			current = open("current.txt", 'w')
			current.write(HillaryNew + '\n' + DonaldNew + '\n')
			current.close
		if float(DonaldNew) > float(Donald):
			#post
			DonaldUP = 'Donald is gaining. Likelihood of a Donald win went from ' + Donald + '% to ' + DonaldNew + '%. #Trump'
			r = api.request('statuses/update', {'status': DonaldUP})
			print 'SUCCESS' if r.status_code == 200 else 'FAILURE'
			#set current values
			current = open("current.txt", 'w')
			current.write(HillaryNew + '\n' + DonaldNew + '\n')
			current.close
		else:
			print "No Change"

#makes scheduler run???
sched.start()
