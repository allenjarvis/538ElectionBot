from lxml import html
import requests
from TwitterAPI import TwitterAPI
from apscheduler.schedulers.blocking import BlockingScheduler

api = TwitterAPI('y7uybSTbSXyHkve16gHaAgObI',
                 'gjSMPeCpletnARVihBl4hlYOTUMNsb5mTaU0pOr6eU89QvK0Lo',
                 '781536298506985476-nBrmnvlkOf4F6HPEHK6AWOCyyPSLAfO',
                 'KqOnzmQEfyGOhuqEft4t8XyALEp5XsEw6A40qh8W6l9DU')

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
	current = open("current.txt", 'r')
	Hillary = current.readline()[0:-1]
	Donald = current.readline()[0:-1]
	current.close

	print Hillary
	print Donald

	page = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
	tree = html.fromstring(page.content)
	HillaryNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/p[2]/text()')[0]
	DonaldNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/p[2]/text()')[0]

	print HillaryNew
	print DonaldNew

	HillaryUP = 'Hillary is UP! Likelihood of a Clinton win went from ' + Hillary + ' to ' + HillaryNew
	DonaldUP = 'Donald is UP. Likelihood of a Donald win went from ' + Donald + ' to ' + DonaldNew

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
