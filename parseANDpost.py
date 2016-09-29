from lxml import html
import requests
from twitter.api import Twitter

twitter = Twitter('electionbot538','Th1s1smy9assw0rd')
current = open("current.txt")
Hillary = int(current.readline()[0,3])
Donald = int(current.readline()[0,3])
print Hillary
print Donald

page = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
tree = html.fromstring(page.content)
HillaryNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/p[2]/text()')
DonaldNew = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/p[2]/text()')
#check that these are numbers instead of strings?

print HillaryNew
print DonaldNew

HillaryUP = 'Hillary is UP! Liklihood of a Clinton win went from ' + Hillary + ' to ' + HillaryNew
DonaldUP = 'Donald is UP. Liklihood of a Donald win went from ' + Donald + ' to ' + DonaldNew

if HillaryNew >= Hillary:
  twitter.statuses.update(status=HillaryUP)
  Hillary = HillaryNew
  Donald = DonaldNew
if DonaldNew >= Donald:
  twitter.statuses.update(status=DonaldUP)
  Hillary = HillaryNew
  Donald = DonaldNew

current.close
