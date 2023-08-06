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
from PipePyper.mytools import reversePipe

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

def test_2():
	p = reversePipe(range(200)).mp_map(get_guba_list,5).mp_map(process_page,2)
	res = p.collect()
	print(res)

if __name__=="__main__":
	test()
```