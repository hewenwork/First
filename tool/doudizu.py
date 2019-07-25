#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Mr
# datetime:2019/7/16 14:09
# software: PyCharm
import requests,random
from lxml import etree

class Ftx_newhouse_Secondhandhouse(object):
    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    # 'Cookie': 'vY0_msid=W6InlF; pgv_pvi=306410496; '
    #           'Hm_lvt_40c6e114e4547fbe70409fa3d0e8a795=1557467513; '
    #           'Hm_lvt_63b5fb0b0c7e00e5f19960916c6ef5b8=1559209394,1561707166;'
    #           ' fcw_coclassedit=800x600; fcw_cotypesedit=800x600; '
    #           'fcw_arcinfo=480x320; PHPSESSID=dc60c66b3ec2eefe09dde50c174f1e00;'
    #           ' Hm_lvt_e0953c818f3197ba65c501b74538b609=1562998251,1563169963,1563246916,1563248802; '
    #           'Hm_lpvt_e0953c818f3197ba65c501b74538b609=1563248802; '
    #           'vY0_login_img=gjvLwsmInGeOkpcyXBeQltci3ZST48M'}

    def __init__(self):
        self.url = 'http://www.fangfangfang.com/newhouse/1.html'
        self.s = requests.session()

    def Newhouse_ftx(self):#获取单个区域url
        try:
            response = self.s.get(self.url )
        except Exception as e:
            print('errp',e)
        response.encoding = 'utf-8'
        urls = etree.HTML(response.text)
        xf_adrss = urls.xpath('//div[@class="item price"][1]/div[2]/a/text()'
                              )
        xf_url = urls.xpath('//div[@class="item price"][1]/div[2]/a/@href'
                            )
        dictx=dict(zip(xf_adrss,xf_url))
        del dictx['不限']
        del dictx['城内']
        del dictx['其他']
        listx = list(dictx.values())
        return listx

    def single_url(self):#下面功能实现了   获取单个区域页面的楼盘URL及楼盘名称
        listax = []
        for i in range(0,12):
            page = self.page_tuple()[i]
            for i,url in enumerate(page):
                resp = self.s.get(url)
                resp.encoding = 'utf-8'
                urls = etree.HTML(resp.text)
                for number in range(1,7):
                    xf_adrss = urls.xpath('//div[@class="fl new_list_l mb20"]/div["%d"]/ul[2]/li[1]/a/text()'%number)
                    if xf_adrss ==[]:
                        continue
                    xf_url = urls.xpath('//div[@class="fl new_list_l mb20"]/div["%d"]/ul[2]/li[1]/a/@href'%number)
                    lista = list(zip(xf_adrss,xf_url))
                    listax.append(lista)
                    break
        return listax

    def page_tuple(self):#所有区域页面跳转实现
        lists = tuple(self.Newhouse_ftx())
        chengbei=[]
        chengxi=[]
        chengnan=[]
        gaoxin=[]
        chengdong=[]
        qujiang=[]
        changan=[]
        chanba=[]
        jingkai=[]
        zhoubian=[]
        gaolingqu=[]
        xixian=[]
        for i in lists:
            a = str(i)
            urlx = a[:-6]
            for i in range(1, 7):
                url = urlx + '%d.html' % i
                # print(url)
                if url =='http://www.fangfangfang.com/newhouse/chengbei/%d.html'%i:
                    chengbei.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/chengxi/%d.html'%i:
                    chengxi.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/chengnan/%d.html'%i:
                    chengnan.append(url)#L
                elif url =='http://www.fangfangfang.com/newhouse/gaoxin/%d.html'%i:
                    gaoxin.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/chengdong/%d.html'%i:
                    chengdong.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/qujiang/%d.html'%i:
                    qujiang.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/changan/%d.html'%i:
                    changan.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/chanba/%d.html'%i:
                    chanba.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/jingkai/%d.html'%i:
                    jingkai.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/daxingqu/%d.html'%i:
                    zhoubian.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/gaolingqu/%d.html'%i:
                    gaolingqu.append(url)
                elif url =='http://www.fangfangfang.com/newhouse/xixian/%d.html'%i:
                    xixian.append(url)
                else:
                    print('错误')
        return  chengbei,chengxi,chengnan,gaoxin,chengdong,qujiang,changan,chanba,jingkai,zhoubian,gaolingqu,xixian

    def demo(self):
        all_page=[]
        demo1 = self.single_url()
        extent = len(demo1)
        for i in range(extent):
            listx =demo1[i]
            extent1 = len(listx)
            try:
                for i in range(extent1):
                    a = listx[i]
                    if a == None:
                        continue
                    else:
                        c = a[1]
                        all_page.append(c)
            except Exception as e:
                print()
        return all_page

if __name__ == '__main__':
    a = Ftx_newhouse_Secondhandhouse().demo()
    print(a)
