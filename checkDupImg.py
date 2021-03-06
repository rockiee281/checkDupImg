#!/usr/bin/python
# encoding=utf-8
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
        buffer = []
        try:
                data = StringIO(urllib2.urlopen(url).read())
                hash = imagehash.average_hash(Image.open(data))
#                print hash,url
                buffer.append((str(hash),url.strip()))
                data.close()
        except urllib2.URLError, e:
            print e
        except IOError,e:
            print e
        except:
            pass

        #sort buffer ordered by phash
        sorted(buffer,key=lambda item:item[1])
        result = open('result','w',2048)
        for val in buffer:
            result.write(val[0] + ' ' + val[1] + '\n')
        result.close()

def checkImg():
        f = file('imageLists','r')
        lines = f.readlines()
        f.close()
#        for imgUrl in jsonData[0::2]:
#                checkImage(imgUrl)        
        jobs = [gevent.spawn(checkImage,imgUrl) for imgUrl in lines]
        gevent.joinall(jobs)

def checkSimilar(differ = 5000):
    f = file('result')
    outfile = file('output.html','w')
    outfile.write('<html><body>')
    delfile = file('toBeDel','w')
    lines = f.readlines()
    f.close()
    # if toBeDel.old exists, remove deleted images from result
    import os 
    if os.path.isfile('toBeDel.old'):
        deledfile = file('toBeDel.old')
        deledLines = deledfile.readlines()
        deledfile.close()
        lines = [line for line in lines if line.split(' ')[1] not in deledLines]
    lasthash = 0
    similar = []
    similar.append(lines[0].strip())
    for line in lines:
        data = line.split(' ')
        hash = int(data[0],16)
        if hash - lasthash < differ :
           similar.append(line.strip())
        else:
            if len(similar) > 1 :
                outfile.write('<div>')
                for item in similar:
                    imginfo = item.split(' ')
                    outfile.write(imginfo[0])
                    outfile.write('<img style="width:500px;" src="' + imginfo[1] + '" />')
                outfile.write('</div>\n')
                for item in similar[1:]:
                    delfile.write(item.split(' ')[1] + "\n")
                similar = []
                similar.append(line.strip())
            elif len(similar) == 1:
                similar[0] = line.strip()
        lasthash = hash
    outfile.write('</body></html>')
    outfile.close()

if __name__ == '__main__':
    import os
    import sys
    args = sys.argv[1:]
    
    differ = 5000
    if len(args) > 0:
        differ = args[0]
    #if result has been caculated, donot process again
    if not os.path.isfile('result'): 
       checkImg()
    checkSimilar(int(differ))
