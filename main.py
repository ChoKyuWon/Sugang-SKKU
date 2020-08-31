import requests
import time
from time import sleep
from datetime import date
from urllib import parse
from datetime import datetime
import os
import argparse

TIME = 1.2

class getter():
    def __init__(self,id,pw, debug=False, netfunnel=False):
        self.id = id
        self.pw = pw
        self.url = 'https://sugang.skku.edu/'
        self.cookies = {}
        self.time = str(int(time.time()))
        self.s = requests.Session()
        self.s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                                'X-Requested-With': 'XMLHttpRequest',
                                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5,pt;q=0.4'})
        self.funnelkey=''
        self.is_netfunnel = netfunnel
        self.debug = debug
    
    def fake(self):
        return datetime.now().strftime("%a %b %d %Y %H:%M:%S").replace(" ", "%20") + "%20GMT+0900%20(%ED%95%9C%EA%B5%AD%20%ED%91%9C%EC%A4%80%EC%8B%9C)"

    def updatetime(self):
        self.time = str(int(time.time())+1000)

    def login(self):
        data={'lang':'KO', 'id':self.id, 'pwd':self.pw}
        res = self.s.post(self.url+'skku/login?attribute=loginChk&fake='+self.fake(),data=data)
        if res.json()['code'] != '200':
            print(res.json()['msg'])
            exit()
        return res.json()['token']

    def updatenetfunnel(self):
        self.updatetime()
        res = self.s.get('http://hopperinbulk.skku.edu:8000/ts.wseq?opcode=5101&nfid=0&prefix=NetFunnel.gRtype=5101;&sid=service_1&aid=act_1&js=yes&'+self.time,
                        cookies=self.cookies)
        tmp = res.text.split(';')
        for t in tmp:
            if 'result' in t:
                self.cookies['NetFunnel_ID'] = parse.quote(t.split('\'')[1])
                self.funnelkey = t.split('\'')[1].split('&')[0].split('=')[1]
                return

    def closenetfunnel(self):
        url = 'http://hopperinbulk.skku.edu:8000/ts.wseq?opcode=5004&key='+self.funnelkey+'&nfid=0&prefix=NetFunnel.gRtype=5004;&js=yes&'+self.time
        res = requests.get(url)
        if 'Success' in res.text:
            return True
        else:
            print(res.text)
            return False
    
    def getdata(self):
        self.updatetime()
        url_lec = self.url+'skku/core?attribute=lectList&token='+self.token+'&menu=0&fake='+self.fake()+'&_search=false&nd='+self.time+'&rows=2000&page=1&sidx=&sord=asc'
        res = self.s.get(url_lec, cookies=self.cookies)
        
        return res.json()

    def sugang(self, sub, name):
        data = {'params':sub}
        url = self.url+'skku/sugang?attribute=sugangMode&token='+self.token+'&mode=insert&fake='+self.fake()
        res = self.s.post(url,data=data, cookies=self.cookies)
        
        if self.debug:
            print(res.json())
        
        if res.json()['code'] =='99':
            pass
        
        elif res.json()['code'] =='118':
            #captha solver - auto!
            ticket = res.json()['msg']
            data_new = {'params':sub, 'ticket':ticket}
            res = self.s.post(url,data=data_new, cookies=self.cookies)
            
            if res.json()['code'] == '118':
                print('Auto captha solever not work!')
        
        elif res.json()['code'] =='200':
            if '대기' in res.json()['msg']:
                print(name, '대기')
            else:
                print(name, '수강신청 성공')
        else:
            pass
            # print(res.json())

    def main(self):
        subjectlist = []
        namelist = []
        res = self.s.get(self.url+'skku/login?attribute=login')
        self.token = self.login()
        if self.is_netfunnel:
            self.updatenetfunnel()
        
        rawdata = self.getdata()

        if self.debug:
            print(rawdata)
        
        for each in rawdata['rows']:
            subjectlist.append(each['haksu_no']+'@'+each['bunban']+'@0@N')
            namelist.append(each['gyogwamok_nm'])

        if self.is_netfunnel:
            if not self.closenetfunnel():
                print('Fail to close netfunnel')
                exit()
        
        for sub ,name in zip(subjectlist,namelist):
            if self.is_netfunnel:
                self.updatenetfunnel()
            self.sugang(sub, name)
            sleep(TIME)
            if self.is_netfunnel:
                if not self.closenetfunnel():
                    print('Fail to close netfunnel')
                    exit()

    def jubjub(self):
        res = self.s.get(self.url+'skku/login?attribute=login')
        self.token = self.login()
        consume_time = 0

        while True:
            if self.is_netfunnel:
                self.updatenetfunnel()
            
            rawdata = self.getdata()

            if self.is_netfunnel:
                if self.closenetfunnel() is False:
                    print('Fail to close netfunnel')
                    exit()
            
            for each in rawdata['rows']:
                if int(each['tot_dhw'].split('/')[0].strip()) < int(each['tot_dhw'].split('/')[1].strip()):
                    self.sugang(each['haksu_no']+'@'+each['bunban']+'@0@N', each['gyogwamok_nm'])
                else:
                    print(each['gyogwamok_nm'],each['tot_dhw'].split('/')[0].strip() ,'/',each['tot_dhw'].split('/')[1].strip(), consume_time, 's')
            sleep(5)
            consume_time += 5
     

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--main", help="main sugang mode", nargs='?', const=True, type=bool)
    parser.add_argument("--debug", help="debug on", nargs='?', const=True, type=bool)
    parser.add_argument("--netfunnel", help="netfunnel on", nargs='?', const=True, type=bool)
    args = parser.parse_args()

    os.system('cls')
    print('수강신청 자동화 도구... v0.3\n')


    ###################################################

    id = ''
    pw = ''

    ###################################################

    g = getter(id, pw, args.debug, args.netfunnel)
    if args.main == True:
        g.main()
    else:
        g.jubjub()

if __name__ == '__main__':
    main()
