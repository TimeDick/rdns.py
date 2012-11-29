![Build status](https://secure.travis-ci.org/gxela/rdns.py.png?branch=master)

#rdns.py - Reverse IP Hosts Query Tool

* requires imagemagick to show captcha image

###Changes
* version 1.2 - fixed output in preparation for gui
* version 1.1 - added killall display captcha
* version 1.0 - reverse ip with display catcha

Here are a couple of bash function that will ease the process of getting ip addresses for a domain and giving to rdns.py

    #!/usr/bin/env bash
    function domainips(){
        DOMAINIPS=`dig ${1:-google.com}|grep A|awk '{if( $5 != "" ){ print $5;}}'|grep "\."|xargs`
    }
    function rdnsdomain(){
        python rdns/rdns.py `domainips ${1:-google.com};echo $DOMAINIPS;`
    }
powered by [http://whois.webhosting.info](http://whois.webhosting.info)