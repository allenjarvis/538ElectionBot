from lxml import html
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from twython import Twython
import logging

logging.basicConfig()

#these API keys are deactivated...
CONSUMER_KEY = 'BWat2mRWtkRknJ6qYk0D6Hcsq'
CONSUMER_SECRET = 'V47euwkdq7H2AaAwDvSRWSNnDSkN5MpqVIsdpuiwTxmPsDu4EF'
ACCESS_KEY = '781536298506985476-0aBtzyzdYwBIFNx40dK8bR16B6pkReZ'
ACCESS_SECRET = 'VjJqVbNeBWgkwLySaBhsQlNn7gENaYl15czNmewJlURT2'
twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

#pulls tweets from timeline until it finds the last update. returns [previous gainer],[relevant segment of the tweet],[# of other tweets since last update]
def getTweetSegment(num):
	user_timeline = twitter.get_user_timeline(screen_name="electionbot538", count=num, include_retweets=False, exclude_replies=True)
	for tweet in user_timeline:
		last = tweet['text']
	if num>20:
		print 'error: could not find last update from Twitter'
		return 'error error error'
	elif last[0:14]=='Clinton gained':
		prevGainer = "Clinton"
		segment = find2Percent(last)
		return prevGainer, segment, str(num-1)
	elif last[0:13]=='Donald gained':
		prevGainer = "Donald"
		segment = find2Percent(last)
		return prevGainer, segment, str(num-1)
	else:
		return getTweetSegment(num+1)

#finds 2nd "%" in a string, returns a segment of the string near that %
def find2Percent(my_string):
	idx=0
	while my_string[idx] != '%':
		idx += 1
	idx += 1
	while my_string[idx] != '%':
		idx += 1
	hollaback = my_string[idx-4:idx+10]
	return hollaback

#scheduler setup
sched = BlockingScheduler()

#scheduler start
@sched.scheduled_job('interval', minutes=5)
def timed_job():
	#get segment of last Tweet containing percentages, assign and print
	gain, segment, tweetssince = getTweetSegment(1)
	print "---------------------------"
	print "Last: " + gain + " increased... " + segment#(should look like "##.#% to ##.#%")
	print "Tweets since last update: " + tweetssince
	if gain == "Clinton":
			Hillary = segment[0:4]
			Donald = segment[9:13]
	if gain == "Donald":
			Donald = segment[0:4]
			Hillary = segment[9:13]
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
	if Hillary != Donald and DonaldNew==HillaryNew:
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
		HillaryUP = 'Clinton gained ' + gain + '%! She now ' + leadstrails + ' Donald ' + HillaryNew + '% to ' + DonaldNew + "% in the @FiveThirtyEight polls-only forecast.\r\n#Clinton #Trump #538 #election2016"
		twitter.update_status(status=HillaryUP)
		print "POST: " + HillaryUP
	#case: Donald up
	elif float(DonaldNew)>float(Donald):
		gain = str(float(DonaldNew) - float(Donald))
		if float(DonaldNew)>float(HillaryNew):
			leadstrails = 'leads'
		else:
			leadstrails = 'trails'
		DonaldUP = 'Donald gained ' + gain + '%. He now ' + leadstrails + ' Clinton ' + DonaldNew + '% to ' + HillaryNew + "% in the @FiveThirtyEight polls-only forecast.\r\n#Clinton #Trump #538 #election2016"
		twitter.update_status(status=DonaldUP)
		print "POST: " + DonaldUP
	#case: no change
	else:
		print "No Change"

#makes scheduler run
sched.start()
