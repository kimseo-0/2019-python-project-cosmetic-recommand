import urllib.request
from bs4 import BeautifulSoup

def get_html_from_url(url) :
    '''
    get html from URL
    '''
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    html = res.read()
    res.close()

    return html

def get_html_list_by_class(base_html, tag_class) :
    '''
    find class from base_html
    get html
    '''
    html_list = base_html.find_all(class_ = tag_class)
    return html_list

def get_url_from_tag_href(base_html, tag_href) :
    url = base_html.p['tag_href']
    return url
    
def download_image_by_url(image_name,url) :
    fullname = str(image_name) + ".jpg"
    urllib.request.urlretrieve(url,fullname)


base_url = "https://www.powderroom.co.kr"
rankings_url = "https://www.powderroom.co.kr/rankings"
rankings_html = get_html_from_url(rankings_url)

category_class = "col-6 col-sm-4 p-a-2 cursor-pointer rnav-sub-label-active"
category_tag_href = "np-href"
category_quary_list = get_url_from_tag_href(get_html_list_by_class(rankings_html,category_class),category_tag_href)
category_url_list = list(map(lambda category_quary : base_url + category_quary , category_quary_list))
category_html_list = list(map(lambda category_url : get_html_from_url(category_url), category_url_list))

products_class = ".card card-landscape product-ranking-card cursor-pointer"
products_tag_href = "np-href"
products_quary_list = list(map(lambda category_html : get_url_from_tag_href(get_html_list_by_class(category_html, products_class),category_html_list)))
products_url_list = list(map(lambda product_quary : base_url + product_quary + "/variations" , products_quary_list))
products_html_list = list(map(lambda product_url : get_html_from_url(product_url), products_url_list))

print(products_html_list)


""" import os
import asyncio
from pyppeteer import launch
import urllib.request
from bs4 import BeautifulSoup

async def get_html_from_url(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    html = await page.content()
    await browser.close()
    return html

def get_html_list_by_class(base_html,tag_class) :
    '''
    find class from base_html
    get html
    '''
    class_list = base_html.find_all(class_ = tag_class)
    return class_list

def get_attr_list_by_attrKey(base_html,attr) :
    '''
    find class from base_html
    get html
    '''
    return base_html[attr]
    

def download_image_by_url(image_name,url) :
    fullname = "./image/" + str(image_name) + ".jpg"
    urllib.request.urlretrieve(url,fullname)

def createForlder(directory) :
      try : 
        if not os.path.exists(directory):
              os.makedirs(directory)
      except OSError :
        print('Error:Creating directory' + directory)

base_html = asyncio.get_event_loop().run_until_complete(get_html_from_url("https://www.powderroom.co.kr/products/56459872/variations"))

base_html = BeautifulSoup(base_html,"html.parser")
product_info_html = get_html_list_by_class(base_html,"w-sm-70 w-60 card-body-large fl-col")[0]
product_color_name_list = get_html_list_by_class(base_html,"card-body-medium fl-grow p-l-3 fl-row fl-ai-center")


# 상품 정보 저장(카테고리, 브랜드, 상품명)

product_category = get_html_list_by_class(product_info_html,"joint-dot")[0].text
product_brand = get_html_list_by_class(product_info_html,"card-text-secondary")[0].text
product_name = get_html_list_by_class(product_info_html,"card-text-primary")[0].text 
product_info = {product_category : product_category , product_brand : product_brand, product_name : product_name}


# 상품명 리스트
image_name_list = [product_name]
for name in product_color_name_list :
      image_name_list.append(name.text) 

# 상품 이미지 소스 리스트
product_image_html_list =  get_html_list_by_class(base_html,"ar-content")

product_image_src_list = []
for image_html in product_image_html_list :
      image_src = get_attr_list_by_attrKey(image_html,"src")
      product_image_src_list.append(image_src)

createForlder(os.getcwd()+"/image/"+product_category)
createForlder(os.getcwd()+"/image/"+product_category+"/"+product_name)

for i in range(len(product_image_src_list)) :
      download_image_by_url(product_category+"/"+product_name+"/"+image_name_list[i],product_image_src_list[i]) 
 """

