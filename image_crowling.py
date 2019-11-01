import urllib.request
from bs4 import BeautifulSoup

def get_html_from_url(url) :
    '''
    get html from URL
    '''
    req = urllib.request.Request(base_url)
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

def get_url_from_tag(base_html, tag_href) :
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
category_quary_list = get_url_from_tag(get_html_list_by_class(rankings_html,category_class),category_tag_href)
category_url_list = list(map(lambda category_quary : base_url + category_quary , category_quary_list))
category_html_list = list(map(lambda category_url : get_html_from_url(category_url), category_url_list))

products_class = ".card card-landscape product-ranking-card cursor-pointer"
products_tag_href = "np-href"
products_quary_list = list(map(lambda category_html : get_url_from_tag(get_html_list_by_class(category_html, products_class),category_html_list)))
products_url_list = list(map(lambda product_quary : base_url + product_quary + "/variations" , products_quary_list))
products_html_list = list(map(lambda product_url : get_html_from_url(product_url), products_url_list))


#produts_url_list.map(elem, (elem) + ((tag[np-href])))



