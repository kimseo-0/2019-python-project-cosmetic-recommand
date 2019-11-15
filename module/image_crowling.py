import os
import asyncio
import re
import time
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

def set_product_info(product_id, product_ranking, product_category,product_brand,product_name,product_url,product_color_name_list,product_image_src_list) :
    '''
    make dict product category, brand, name, url, color list, image source list
    return  dict
    '''
    product_info = {
        "product_id" : product_id,
        "product_ranking" : product_ranking,
        "product_category" : product_category, 
        "product_brand" : product_brand, 
        "product_name" : product_name, 
        "product_url" : product_url, 
        "product_color" : product_color_name_list,
        "product_image_src" : product_image_src_list
                    }

    return product_info

def get_product_info(product_info_html, 
                    product_id, 
                    product_ranking, 
                    category_class, 
                    brand_class, 
                    name_class,
                    product_url, 
                    product_color_name_list, 
                    product_image_src_list) :
                    
    product_category = get_html_by_class(product_info_html,category_class).text
    product_brand = get_html_by_class(product_info_html,brand_class).text
    product_name = get_html_by_class(product_info_html,name_class).text 

    product_info = set_product_info(product_id, 
                                    product_ranking, 
                                    product_category,
                                    product_brand,
                                    product_name,
                                    product_url,
                                    product_color_name_list,
                                    product_image_src_list)

    return product_info

def download_image_by_url(image_name,url) :
    '''
    download image by url
    dir :  "./image/" + str(image_name) + ".jpg"
    '''
    fullname = "./image/" + str(image_name) + ".jpg"
    urllib.request.urlretrieve(url,fullname)

def create_forlder(directory) :
    '''
    create forlder
    '''
    try : 
        if not os.path.exists(directory):
                os.makedirs(directory)
    except OSError :
        print('Error:Creating directory' + directory)