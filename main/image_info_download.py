import os
import asyncio
import re
import time
from bs4 import BeautifulSoup
import re

import image_crowling as ic

# 크롤링할 홈페이지 base url
base_url = "https://www.powderroom.co.kr"

# 크롤링 base_url+"/rankings/c3100"
base_html = asyncio.get_event_loop().run_until_complete(ic.get_html_to_web(base_url + "/rankings/c3100"))
base_html = BeautifulSoup(base_html,"html.parser")

# 상품 타이틀 html list -> 각 상품 url quary list  -> 각 상품별 url list
product_title_html_list = ic.get_html_list_by_class(base_html, "card card-landscape product-ranking-card cursor-pointer")
product_title_quary_list = list(map(lambda product_title_html : ic.get_attr_list_by_attrKey(product_title_html,"np-href") , product_title_html_list))

product_ranking = 0
for product_title_quary in product_title_quary_list :

    # 상품 정보 html
    product_url = base_url + product_title_quary
    product_info_html = asyncio.get_event_loop().run_until_complete(ic.get_html_to_web(product_url))
    product_info_html = BeautifulSoup(product_info_html,"html.parser")
    product_info_html = ic.get_html_by_class(product_info_html,"w-sm-70 w-60 card-body-large fl-col")

    # 상품 id 추출
    p = re.compile('[0-9]+') 
    product_id = str((p.findall(product_title_quary))[0])

    # 상품 정보 저장(카테고리, 브랜드, 상품명)
    category_class = "joint-dot"
    brand_class = "card-text-secondary"
    name_class = "card-text-primary"

    # 상품 id, 상품 순위, 상품 카테고리, 상품 브랜드, 상품명, 상품 url, 상품 색상명, 상품 색상별 이미지 src
    product_info = ic.get_product_info(product_info_html, 
                                    product_id, 
                                    product_ranking, 
                                    category_class, 
                                    brand_class, 
                                    name_class,
                                    product_url
                                    )