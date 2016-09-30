from lxml import html
import requests
from TwitterAPI import TwitterAPI
from apscheduler.schedulers.blocking import BlockingScheduler

api = TwitterAPI('y7uybSTbSXyHkve16gHaAgObI',
                 'gjSMPeCpletnARVihBl4hlYOTUMNsb5mTaU0pOr6eU89QvK0Lo',
                 '781536298506985476-nBrmnvlkOf4F6HPEHK6AWOCyyPSLAfO',
                 'KqOnzmQEfyGOhuqEft4t8XyALEp5XsEw6A40qh8W6l9DU')

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
	current = open("current.txt", 'r')
	Hillary = current.readline()[0:-1]
	Donald = current.readline()[0:-1]
	current.close

	print 'Hillary: ' + Hillary
	print 'Donald: ' + Donald

	page = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
	tree = html.fromstring(page.content)
	HillaryNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/p[2]/text()')[0]
	DonaldNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/p[2]/text()')[0]

	print 'HillaryNew: ' + HillaryNew
	print 'DonaldNew: ' + DonaldNew

	HillaryUP = "Hillary is gaining! 538's Now-Cast shows Clinton's win probability going from " + Hillary + '% to ' + HillaryNew + '%. #Clinton'
	DonaldUP = "Donald is gaining. 538's Now-Cast shows Donald's win probability going from " + Donald + '% to ' + DonaldNew + '%. #Trump'

	if float(HillaryNew) > float(Hillary):
		r = api.request('statuses/update', {'status': HillaryUP})
		print 'SUCCESS' if r.status_code == 200 else 'FAILURE'

		current = open("current.txt", 'w')
		current.write(HillaryNew + '\n' + DonaldNew + '\n')
		current.close


		Hillary = HillaryNew
	  	Donald = DonaldNew
	if float(DonaldNew) > float(Donald):
		r = api.request('statuses/update', {'status': DonaldUP})
		print 'SUCCESS' if r.status_code == 200 else 'FAILURE'

		current = open("current.txt", 'w')
		current.write(HillaryNew + '\n' + DonaldNew + '\n')
		current.close

		Hillary = HillaryNew
	  	Donald = DonaldNew

sched.start()
