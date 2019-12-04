import os
import asyncio
import re
import time
import urllib.request
from bs4 import BeautifulSoup

from module import image_crowling as ic
from module import product as pd

# 크롤링할 홈페이지 base url
base_url = "https://www.powderroom.co.kr"

# 크롤링 base_url+"/rankings/c3100" -> 립스틱
base_html = asyncio.get_event_loop().run_until_complete(ic.get_html_to_web(base_url + "/rankings/c3100"))
base_html = BeautifulSoup(base_html,"html.parser")

# 상품 타이틀 html list -> 각 상품 url quary list  -> 각 상품별 url list
product_title_html_list = ic.get_html_list_by_class(base_html, "card card-landscape product-ranking-card cursor-pointer")
product_title_quary_list = list(map(lambda product_title_html : ic.get_attr_list_by_attrKey(product_title_html,"np-href") , product_title_html_list))
    
# 모든 상품의 정보 저장
# 모든 상품을 카테고리, 상품명 별로 각 색상별 상품 이미지 다운로드
product_ranking = 0
for product_title_quary in product_title_quary_list :
    
    # 상품 순위 - ranking 순대로 크롤링 되므로
    product_ranking += 1
    print(product_ranking)

    # 크롤링 url+"/variations"
    product_url = base_url + product_title_quary + "/variations" 
    product_html = asyncio.get_event_loop().run_until_complete(ic.get_html_to_web(product_url))
    product_html = BeautifulSoup(product_html,"html.parser")
    
    # 상품 색상명 html list -> 상품 색상명 list
    product_color_name_list = ic.get_html_list_by_class(product_html,"card-body-medium fl-grow p-l-3 fl-row fl-ai-center")
    product_color_name_list = list(map(lambda product_color_name :  product_color_name.text , product_color_name_list))

    # 상품 이미지 html list -> 상품 이미지 src list
    product_image_html_list =  ic.get_html_list_by_class(product_html,"ar-content")
    product_image_src_list = list(map(lambda product_image_html :  ic.get_attr_list_by_attrKey(product_image_html,"src") , product_image_html_list))
    
    print(product_color_name_list)

    # 상품 id 추출
    p = re.compile('[0-9]+') 
    product_id = str((p.findall(product_title_quary))[0])
    
    # 이미지 dir 생성
    #pd.create_forlder(os.getcwd()+"/image/"+product_id)

    for i in range(len(product_color_name_list)) :

        # 이미지 다운로드
        #ic.download_image_by_url(product_id+"/"+str(i),product_image_src_list[i+1])

        # 이미지 상품의 각 색상별 정보 저장
        pd.set_product_color_list_to_file("image_data/"+product_id+"/"+str(i)+".txt",
                                        product_color_name_list[i],
                                        product_image_src_list[i+1])