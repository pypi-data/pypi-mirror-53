# PipePyper
## usage :
```python
# -*- coding: utf-8 -*- 
""" 
Created on 2019-08-30 09:47:25.418502 

@author: 洪宇庄
"""
import re
import bs4
import requests
from PipePyper.PipePyper  import PipeSet
from PipePyper.mytools import logger


def get_guba_list(page , name =None,logger = None):
	url = 'http://guba.eastmoney.com/list,gssz_{}.html'.format(page)
	res=requests.get(url)
	logger.log('finish downLoad page : {}'.format(page))
	return url,res.text

def process_page(res,name = None,logger = None):
	el_class = 'articleh normal_post'
	url,page = res
	soup = bs4.BeautifulSoup(page,'lxml')
	res = '\n'.join( [i.text for  i in soup.find_all('div',{'class':el_class})])
	logger.log('finish process {}'.format(url))
	return res


def test():
	data = range(20)
	lg = logger('.','tmp_test')
	lg.log('1')

	p1 = PipeSet(get_guba_list,{},4)+lg
	p2 = PipeSet(process_page,{},2)+lg
	p1>>p2

	p2.run()

	data>=p1

	res = p2.collect()

	print(res)

if __name__=="__main__":
	test()
```