#!/bin/python3
import argparse
import subprocess
import os
import requests
import sys

argp = argparse.ArgumentParser(usage = "dom.py -d domain.com -s\nor\ndom.py -og example.txt -s\nif you want to save other \ndomains with response status code \nthen use -s or by defualt it will not save \nthe response code")
argp.add_argument("-d", "--domain",default=0)
argp.add_argument("-og","--organize",default=0)
argp.add_argument("-s","--status",action='store_true')
parser = argp.parse_args()
domain = parser.domain
fname = parser.organize
header={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30'}
timeout = 5


def assetfinder():
    try:
        print("[+] using assetfinder")
        lis1 = os.popen('assetfinder -subs-only %s'%domain).read()
        print("[+] assetfinder Fetching Done")
        fsubs = lis1.split('\n')
        return fsubs
    except:
        print('[-] Error Occured While Fetching With Assetfinder')
def amass():
    try:
        print("[+] using amass")
        lis2 = os.popen('amass enum -d %s'%domain).read()
        print("[+] Amass Fetching Done")
        fsubs = []
        fsubs = lis2.split('\n')
        return fsubs
    except:
        print('[-] Error Occured While Fetching With Assetfinder')
def sublister():
    print("[+] using sublist3r")
    try:
        s = subprocess.Popen(['sublist3r','-d',domain,'-o','./tmp.txt'],stdout = subprocess.PIPE)
        s.communicate()
        print("[+] Sublist3r Fetching Done")
        with open('./tmp.txt','r') as s:
            su = s.readlines()
        tmp = ''.join(su)
        tmp = tmp.replace('<BR>','\n')
        ru = tmp.split('\n')
        os.system('rm ./tmp.txt')
        return ru
    except:
        print('[-] Error Occured While Fetching With Assetfinder')

def return_code(subs):
    with open('live_domains.txt','w') as live:
        live.close()
    with open('other_domains.txt','w') as other:
        other.close()
    for line in subs:
        url = "http://{}".format(line)
        try:
            req = requests.get(url, timeout=timeout,headers=header)
            if req.status_code == 200:
                code = " HTTP 200 OK"
                print("[+] Domain is online! ({}) {}".format(url, code))
                with open('live_domains.txt','a') as live:
                    live.write("{}\n".format(url))
            else:
                code = "HTTP {}".format(req.status_code)
                print("[-] Domain did not return 200 OK! ({}) {}".format(url, code))
                with open('other_domains.txt','a') as other:
                    other.write("{}".format(url) + ("{}\n".format(code) if parser.status else '\n'))
        except KeyboardInterrupt:
            exit()
        except requests.exceptions.Timeout:
            print("[-] Domain timed out! ({})".format(url))
            with open('other_domains.txt','a') as other:
                other.write("{}".format(url) + (("  Timeout\n") if parser.status else '\n'))
        except requests.exceptions.ConnectionError:
            print("[-] Domain may not exist! ({})".format(url))
            with open('other_domains.txt','a') as other:
                other.write("{}".format(url) + (("  ConnectionError\n") if parser.status else '\n'))

if __name__=='__main__':
    if(domain != 0):
        asset_subs = assetfinder()
        print(asset_subs)
        print("This might Take Some Time\nPlease Wait")
        amass_subs = amass()
        print(amass_subs)
        sublister_subs = sublister()
        print(sublister_subs)
        input('lol : ')
        subdomains = asset_subs + sublister_subs + amass_subs
        subdomains.remove('')
        print("[+] removing Duplicates")
        f = dict.fromkeys(subdomains)
        f_subdomains = list(f)
        try:
            return_code(f_subdomains)
        except:
            print("Something Went Wrong Please Check the all_dom.txt\nAnd Try Again \nwith -og option to continue the process")
            with open('all_dom.txt','w') as s:
                s.close()
            for line in f_subdomains:
                with open('all_dom.txt','a') as s:
                    s.write(line + '\n')
    else:
        if(fname!=0):
            doms = []
            with open(fname,'r') as l:
                d = l.readlines()
            for el in d:
                doms.append(el.strip())
            return_code(doms)