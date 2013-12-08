#!/usr/bin/python
#check duplicate picture from web
import urllib2
import urlparse
import gevent
from gevent import monkey
import json
from cStringIO import StringIO
import imagehash
import Image

monkey.patch_all()

def checkImage(url):
#	urlTuple = urlparse.urlparse(url)
#	filename = urlTuple.path[urlTuple.path.rfind('/')+1:]
#	print urlTuple.path
#	print filename
#	f = file('images/'+filename,'wb')
#	print url
	try:
		data = StringIO(urllib2.urlopen(url).read())
		hash = imagehash.average_hash(Image.open(data))
		print hash,url
		data.close()
	except urllib2.URLError, e:
		print e
#	f.write(data)
#	f.close()

def checkImg():
	url='http://cloud.dakele.com/api/gamecenter/l1/beauty?limit=40&offset=0'
	data=urllib2.urlopen(url).read()
	jsonData = json.loads(data)['data']
	
#	for imgUrl in jsonData[0::2]:
#		checkImage(imgUrl)	
	jobs = [gevent.spawn(checkImage,imgUrl) for imgUrl in jsonData[0::2]]
	gevent.joinall(jobs)

if __name__ == '__main__':
	checkImg()
