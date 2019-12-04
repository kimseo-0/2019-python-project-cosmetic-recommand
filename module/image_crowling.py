import asyncio
import urllib.request
from pyppeteer import launch
from bs4 import BeautifulSoup

async def get_html_to_web(url) :
    '''
    get html from url
    '''
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    html = await page.content()
    await browser.close()

    return html

def get_html_list_by_class(base_html,tag_class) :
    '''
    find class from base_html
    return html
    '''
    html_list = base_html.find_all(class_ = tag_class)

    return html_list

def get_html_by_class(base_html,tag_class) :
    '''
    find class from base_html
    return html list
    '''
    html_list = base_html.find(class_ = tag_class)


    return html_list

def get_attr_list_by_attrKey(base_html,attr) :
    '''
    find class from base_html
    return  html list
    '''

    return base_html[attr]

def download_image_by_url(image_name,url) :
    '''
    download image by url
    dir :  "./image/" + str(image_name) + ".jpg"
    '''
    fullname = "./image/" + str(image_name) + ".jpg"
    urllib.request.urlretrieve(url,fullname)