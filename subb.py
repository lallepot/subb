#!/usr/bin/python
import argparse, urllib2, hashlib, ssl

x = 0
result = []
template = "{0:15}|{1:50}|{2:32}"

parser = argparse.ArgumentParser()
parser.add_argument("domain", help="echo the string you use here")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-ssl", help="use https", action="store_true")
parser.add_argument("-w", help="path to word list", action="store_true")

args = parser.parse_args()

domain = args.domain

if args.ssl == True:
    protocol = "https://"
else:
    protocol = "http://"

if args.w == True:
    wordlist = args.w
else:
    wordlist = "list"

f = open(wordlist, 'r')

url = protocol+domain

def go_do():
    count = 0
    print "Checking URLs"
    print template.format("COUNT", "URL", "MD5")
    num_lines = sum(1 for line in open(wordlist))
    for line in f:
        if line.rstrip() == "":
            url = protocol + line.rstrip() + domain
        else :
            url = protocol+line.rstrip()+'.'+domain
        try:
            response = urllib2.urlopen(url).read()
            m = hashlib.md5(response)
            md5 = m.hexdigest()
        except urllib2.HTTPError as e:
            md5 = "ERROR:" + str(e.code)
        except ssl.CertificateError as e:
            url = "http://"+line.rstrip() + '.' + domain
            #print urllib2.urlopen(url).read()
            m = hashlib.md5(response)
            md5 = m.hexdigest()
        output = ("[" + str(count) + "/" + str(num_lines) + "]", url, md5)
        print template.format(*output)
        result.append(line.rstrip())
        result.append(md5)
        count = count + 1
go_do()
