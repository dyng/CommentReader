from commentreader import *

size = {'length':10, 'width':20, 'sec_num':5}

path = '/Users/tei-you/Project/CommentReader/battleroyal.txt'

br = book(path, **size)
n = 1
for s in br.nextPage().segments:
    print "section %s" % n
    print "=" * 20
    n += 1
    for c in s.content:
        print c

