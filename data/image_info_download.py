import os
import asyncio
import re
import time
from bs4 import BeautifulSoup

from my_module import image_crowling as ic
from my_module import product as pd

# 크롤링할 홈페이지 base url
base_url = "https://www.powderroom.co.kr"

# 크롤링 base_url+"/rankings/c3100"
base_html = asyncio.get_event_loop().run_until_complete(ic.get_html_to_web(base_url + "/rankings/c3100"))
base_html = BeautifulSoup(base_html,"html.parser")

# 상품 타이틀 html list -> 각 상품 url quary list  -> 각 상품별 url list
product_title_html_list = ic.get_html_list_by_class(base_html, "card card-landscape product-ranking-card cursor-pointer")
product_title_quary_list = list(map(lambda product_title_html : ic.get_attr_list_by_attrKey(product_title_html,"np-href") , product_title_html_list))

# 상품 id 리스트
product_id_list = []

product_ranking = 0
for product_title_quary in product_title_quary_list :
     
    # 상품 순위 - ranking 순대로 크롤링 되므로
    product_ranking += 1
    print(product_ranking)

    # 상품 정보 html
    product_url = base_url + product_title_quary
    product_info_html = asyncio.get_event_loop().run_until_complete(ic.get_html_to_web(product_url))


    product_info_html = BeautifulSoup(product_info_html,"html.parser")
    #product_info_html = ic.get_html_by_class(product_info_html,"card-body fl-row b-b-card")
  
    # 상품 id 추출, id 리스트에 추가
    p = re.compile('[0-9]+') 
    product_id = str((p.findall(product_title_quary))[0])
    product_id_list.append(product_id)

    
    # 상품 정보 저장(카테고리, 브랜드, 상품명)
    category_class = "card-text-info m-b-1"
    brand_class = "card-text-secondary"
    name_class = "card-text-primary"

    product_category = ic.get_html_by_class(product_info_html,category_class).text
    product_category = product_category.strip()
    product_brand = ic.get_html_by_class(product_info_html,brand_class).text
    product_name = ic.get_html_by_class(product_info_html,name_class).text 

    # 상품 id, 상품 순위, 상품 카테고리, 상품 브랜드, 상품명, 상품 url
    product_info = pd.set_product_info( 
                                    product_id, 
                                    product_ranking, 
                                    product_category, 
                                    product_brand, 
                                    product_name,
                                    product_url
                                    )
    
    print(product_info)

    # 이미지 정보 dir 생성
    pd.create_forlder(os.getcwd()+"/image_data/"+product_id)

    # 이미지 상품별 정보 파일 저장
    pd.set_product_info_to_file(product_id, product_info)
  
# 상품 id 리스트 파일 저장    
pd.set_product_id_to_file(product_id_list)