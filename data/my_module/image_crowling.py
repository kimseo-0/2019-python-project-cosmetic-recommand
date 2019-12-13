import asyncio
import urllib.request
from pyppeteer import launch
from bs4 import BeautifulSoup

async def get_html_to_web(url) :
    '''
    get html from url
    해당 url 페이지의 html을 모두 크롤링해 리턴한다. 
    '''
    browser = await launch() # pyppetteer로 웹 페이지 launch 
    page = await browser.newPage()
    await page.goto(url)
    html = await page.content()
    await browser.close()

    return html

def get_html_list_by_class(base_html,tag_class) :
    '''
    find class from base_html
    return html
    html에서 해당 태그의 클래스와 
    일치하는 부분의 html 리스트 리턴
    '''
    html_list = base_html.find_all(class_ = tag_class)

    return html_list

def get_html_by_class(base_html,tag_class) :
    '''
    find class from base_html
    return html
    html에서 해당 태그의 클래스와 
    일치하는 첫 번째 부분의 html 리턴
    '''
    html = base_html.find(class_ = tag_class)

    return html

def get_attr_list_by_attrKey(base_html,attr) :
    '''
    attr of base_html
    return  attr
    html에서 해당 태그의 속성의 내용 리턴
    '''

    return base_html[attr]

def download_image_by_url(image_name,url) :
    '''
    download image by url
    dir :  "./image/" + str(image_name) + ".jpg"
    '''
    
    fullname = "./image/" + str(image_name) + ".jpg"
    urllib.request.urlretrieve(url,fullname)