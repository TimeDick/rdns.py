#!/usr/bin/env python
#requires imagemagick for display command
# version 1.0 - reverse ip with display catcha
# version 1.1 - added killall display captcha
# version 1.2 - fixed output in preparation for gui

#dig google.com|awk '{if( $5 != "" ){ print $5;}}'|grep "\."|xargs
from urllib2 import Request, urlopen
from urllib import urlencode
import sys,os,subprocess
from sgmllib import SGMLParser


class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)
#    def start_input(self,attrs):
#        keys=[v for k,v in attrs if k == 'name']
#        values=[v for k,v in attrs if k == 'value']
#        print dict(zip(keys,values))
class wwhi_rip(object):
    def __init__(self,ip):
        self.html=[] #holds all read pages for scraping
        self.cid="" #captcha id
        self.cvalue="" #captcha value inside image
        self.ip=ip #ip used in reverse lookup
        self.image_app="display" #app used to diplay captcha
        self.url="http://whois.webhosting.info/"+self.ip
        self.hosts_count=0 #hosts count
        self.hosts_per_page=50 #hosts per page as per self.url
        self.pages_count=0 #pages count
        self.hosts={} #host to ip map

    def _sendreq(self,req):
        u = None
        try:
            _u = urlopen(req)
            u = _u.read()
        except IOError,e:
            if hasattr(e,'reason'):
                print e.reason
                return None
            elif hasattr(e,'code'):
                print e.code
                return None
        else:
            _u.close()
        return u
    def _q_page(self,page):
        return self._sendreq(self.url+"?pi=%s&ob=SLD&oo=ASC"%(page))

    def _postcaptcha(self):
        values = {"enck":self.cid,"srch_value":self.ip,"code":self.cvalue,"subSecurity":"Submit"}
        data = urlencode(values)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = Request(self.url,data,headers)
        return self._sendreq(req)
    def _showcaptcha(self):
        #print "Please complete displayed CAPTCHA to continue."
        subprocess.Popen(self.image_app+" http://charting.webhosting.info/scripts/sec.php?ec="+self.cid,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.cvalue=raw_input("CAPTCHA: ")
        if self.cvalue!="":
            return self._postcaptcha()
        else:
            return None

    def _iscaptcha(self,html):
        if html.find("http://charting.webhosting.info/scripts/sec.php?ec=")>0:
            self.cid=html.split("http://charting.webhosting.info/scripts/sec.php?ec=")[1].split("'></td>")[0]
            cap=self._showcaptcha()
            if cap != None:
                print "Terminating Image"
                os.system("killall "+self.image_app)
                return cap
            else:
                print "Try Again!",sys.exit()
        else:
            return html

    def _gethostscount(self,html):
        if html.find("IP hosts") >=0:
            self.hosts_count = int(html.split("IP hosts <b>")[1].split("</b>")[0])
            self.pages_count=self.hosts_count/self.hosts_per_page
            if self.hosts_count%self.hosts_per_page>0:
                self.pages_count+=1

    def display_hosts(self, show_output = False, show_index = True):
        self.html.append(self._iscaptcha(self._q_page(1))) #get the first page

        self._gethostscount(self.html[0])

        if show_output:
            print "IP: %s"%self.ip

        self._parsehosts()

        if show_index:
            c=1 #used to display number next to output of host

        if show_output:
            print "Hosts:",self.hosts_count

        for i in self.hosts.keys():
            if show_index and show_output:
                print str(c)+": "+i
                c+=1
            else:
                if show_output:
                    print i

        if show_output:
            print ""

        return list([self.ip, self.hosts_count, self.hosts])

    def _parsehosts(self):
        parser = URLLister()
        if self.pages_count>1:
            for i in range(2,self.pages_count+1):
                self.html.append(self._iscaptcha(self._q_page(i)))
        for i in range(self.pages_count):
            parser.feed(self.html[i])

        parser.close()

        for i in range(len(parser.urls)):
            try:
                #print str(i)+":",parser.urls[i].split("http://whois.webhosting.info/")[1][:-1]
                self.hosts[parser.urls[i].split("http://whois.webhosting.info/")[1][:-1]]=self.ip
            except:
                pass

        if self.hosts.has_key(''):
            del self.hosts['']

    def __call__(self, *args, **kwargs):
        return self.display_hosts(*args,**kwargs)
        
if __name__ == "__main__":
    print "http://whois.webhosting.info - Reverse IP Hosts Query Tool"
    if len(sys.argv) <= 1:
        print """ \nUsage: rdns.py <space-separated-list-of-ip-addresses>\n """
    else:
        print ""
        for i in range(1,len(sys.argv)):
            ip=sys.argv[i]
            wwhi_rip(ip)(True, True)

