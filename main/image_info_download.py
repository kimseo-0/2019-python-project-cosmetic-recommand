    # 상품 정보 html
    product_info_html = get_html_by_class(product_html,"w-sm-70 w-60 card-body-large fl-col")

    # 상품 id 추출
    p = re.compile('[0-9]+') 
    product_id = str((p.findall(product_title_quary))[0])

    # 상품 정보 저장(카테고리, 브랜드, 상품명)
    category_class = "joint-dot"
    brand_class = "card-text-secondary"
    name_class = "card-text-primary"

    # 상품 id, 상품 순위, 상품 카테고리, 상품 브랜드, 상품명, 상품 url, 상품 색상명, 상품 색상별 이미지 src
    product_info = get_product_info(product_info_html, 
                                    product_id, 
                                    product_ranking, 
                                    category_class, 
                                    brand_class, 
                                    name_class,
                                    product_url, 
                                    product_color_name_list, 
                                    product_image_src_list)