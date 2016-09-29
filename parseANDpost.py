from lxml import html
import requests

page = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
tree = html.fromstring(page.content)

Hillary = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[1]/div[2]/p[2]/text()')
Donald = tree.xpath('//*[@id="cardsets"]/div[1]/div/div[4]/div[1]/div/div[1]/div[2]/div[1]/p[2]/text()')

print Hillary
print Donald

