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

# 크롤링할 홈페이지 root url
base_url = "https://www.powderroom.co.kr"

# 크롤링 base_url+"/rankings/c3100"
base_html = asyncio.get_event_loop().run_until_complete(get_html_to_web(base_url+"/rankings/c3100"))
base_html = BeautifulSoup(base_html,"html.parser")

# 상품 타이틀 html list -> 각 상품 url quary list  -> 각 상품별 url list
product_title_html_list = get_html_list_by_class(base_html, "card card-landscape product-ranking-card cursor-pointer")
product_title_quary_list = list(map(lambda product_title_html : get_attr_list_by_attrKey(product_title_html,"np-href") , product_title_html_list))
    
# 모든 상품의 정보 저장
# 모든 상품을 카테고리, 상품명 별로 각 색상별 상품 이미지 다운로드
product_ranking = 0
for product_title_quary in product_title_quary_list :
    
    # 상품 순위 - ranking 순대로 크롤링 되므로
    product_ranking += 1
    
    # 크롤링 url+"/variations"
    product_url = base_url + product_title_quary + "/variations" 
    product_html = asyncio.get_event_loop().run_until_complete(get_html_to_web(product_url))
    product_html = BeautifulSoup(product_html,"html.parser")

    # 상품 정보 html
    product_info_html = get_html_by_class(product_html,"w-sm-70 w-60 card-body-large fl-col")
    
    # 상품 색상명 html list -> 상품 색상명 list
    product_color_name_list = get_html_list_by_class(product_html,"card-body-medium fl-grow p-l-3 fl-row fl-ai-center")
    product_color_name_list = list(map(lambda product_color_name :  product_color_name.text , product_color_name_list))

    # 상품 이미지 html list -> 상품 이미지 src list
    product_image_html_list =  get_html_list_by_class(product_html,"ar-content")
    product_image_src_list = list(map(lambda product_image_html :  get_attr_list_by_attrKey(product_image_html,"src") , product_image_html_list))
   
    # 상품 정보 저장(카테고리, 브랜드, 상품명)
    product_category = get_html_by_class(product_info_html,"joint-dot").text
    product_brand = get_html_by_class(product_info_html,"card-text-secondary").text
    product_name = get_html_by_class(product_info_html,"card-text-primary").text 

    p = re.compile('[0-9]+') 
    product_id = str((p.findall(product_title_quary))[0])
    product_info = set_product_info(product_id, product_ranking, product_category,product_brand,product_name,product_url,product_color_name_list,product_image_src_list)
    
    create_forlder(os.getcwd()+"/image/"+product_category)
    create_forlder(os.getcwd()+"/image/"+product_category+"/"+product_id)

    for i in range(len(product_color_name_list)) :
        download_image_by_url(product_category+"/"+product_id+"/"+product_color_name_list[i],product_image_src_list[i+1])
    
    print(product_info)
    break
    time.sleep(3)
