import os
import re
import codecs

def create_forlder(directory) :
    '''
    (str) ->
    create forlder 
    해당 디렉토리로 폴더를 생성한다.
    '''
    try : 
        if not os.path.exists(directory):
                os.makedirs(directory)
    except OSError :
        print('Error:Creating directory' + directory)

##################################### product info ###################################

def set_product_info(product_id, product_ranking, product_category,product_brand,product_name,product_url) :
    '''
    make dict product category, brand, name, url, color list, image source list
    return  dict
    상품 정보(id, 순위, 카테고리, 브랜드, 상품명, url) -> dict 형식으로 리턴한다.
    '''
    product_info = {
        "product_id" : product_id,
        "product_ranking" : product_ranking,
        "product_category" : product_category, 
        "product_brand" : product_brand, 
        "product_name" : product_name, 
        "product_url" : product_url, 
                }

    return product_info

def set_product_id_to_file(product_id_list) :
    '''
    (list) ->
    상품 id들을 파일에 저장한다.
    '''
    ofile = open("image_data/product_id.txt","w")
    for id in product_id_list :
        ofile.write(id+"\n")

def get_product_id_list_from_file() :
    '''
    상품 id들을 파일에서 가져와 리스트로 리턴한다.
    '''
    filename = "image_data/product_id.txt"

    ifile = open(filename,"r")

    product_id_list = []
    
    product_id_list = ifile.readlines()
    product_id_list = list(map(lambda id: id.strip(), product_id_list))

    ifile.close()

    return product_id_list

def get_color_id_list_from_file(product_id) :
    '''
    상품 id들을 파일에서 가져와 리스트로 리턴한다.
    '''
    color_id_list = get_file_list_from_folder("image/"+product_id)
    i = 0
    for color_id in color_id_list :
        start = color_id.index('.jpg')
        color_id_list[i] = color_id[:start]
        i += 1

    return color_id_list

def set_product_info_to_file(product_id,product_info) : 
    '''
    product_id, product_info
    상품 정보를 파일에 저장한다.
    '''
    filename = "image_data/"+product_id+".txt"
    ofile = open(filename,"w")
    ofile.write(product_info["product_id"]+'\n')
    ofile.write(str(product_info["product_ranking"])+'\n') # ranking -> int
    ofile.write(product_info["product_category"]+'\n')
    ofile.write(product_info["product_brand"]+'\n')
    ofile.write(product_info["product_name"]+'\n')
    ofile.write(product_info["product_url"]+'\n')
    ofile.close()

def get_product_info_from_file(product_id) :
    '''
    (str) -> (dict)
    product_id로
    파일에서 상품 정보를 dict 형식으로 리턴한다.
    '''
    filename = "image_data/"+product_id+".txt"
    
    try:
        ifile = codecs.open(filename,'r', 'utf-8')
        product_info_list = []
        product_info_list = ifile.readlines()
    except UnicodeDecodeError:
        try :
            ifile = codecs.open(filename,'r', 'cp949')
            product_info_list = []
            product_info_list = ifile.readlines()
            print("p : utf-8 안됨")
        except Exception as e :
            print("p : cp949도 안됨",e)
            
    except FileNotFoundError :
        print("p : 파일이 없어요")
    
    
    product_info_list = list(map(lambda info: info.strip(), product_info_list))

    ifile.close()

    product_info = {
        "product_id" : product_info_list[0],
        "product_ranking" : int(product_info_list[1]),
        "product_category" : product_info_list[2], 
        "product_brand" : product_info_list[3], 
        "product_name" : product_info_list[4], 
        "product_url" : product_info_list[5], 
                    }

    return product_info

def set_product_color_list_to_file(filename, product_color_name, product_image_src) :
    '''
    상품 색상명과 url을 
    상품 색상별 파일에 저장한다.
    '''
    ofile = open(filename,"w")
    ofile.write(product_color_name+'\n')
    ofile.write(product_image_src+'\n')
    ofile.close()

def add_prodcut_color_to_file(product_id,color_id,RGB) :
    '''
    상품 색상별 파일에 
    색상의 RGB 정보를 저장한다.
    '''
    color = str(RGB[0])+"\t"+str(RGB[1])+"\t"+str(RGB[2])+"\n"
    
    filename = "image_data/"+product_id+"/"+color_id+".txt"
    ofile = open(filename,"a")
    ofile.write(color)
    ofile.close()

def get_product_color_info_from_file(product_id,color_id) :
    '''
    상품 색상별 정보를 
    dict 형식으로 리턴한다.
    '''       
       
    filename = "image_data/"+product_id+"/"+color_id+".txt"
    
    try :
        ifile = codecs.open(filename,'r', 'utf-8-sig')
        color_info_list = ifile.read()
    except UnicodeDecodeError:
        ifile = codecs.open(filename,'r', 'cp949')
        color_info_list = ifile.read()
        print("c : utf-8-sig 안됨")
    except FileNotFoundError :
        print("c : 파일이 없어요")
    except Exception as e :
        print("c : cp949도 안됨",e)

    ifile.close()

    color_info = {
        "product_id" : str(product_id),
        "color_name" : color_info_list, #color_info_list[0][:indx].strip(),
        "color_src" : "", #color_info_list[0][indx+1:].strip(),
        "color_RGB" : "" #color_info_list[0].split()
                    }
    return color_info

def get_file_list_from_folder(folder) :
    path = folder
    file_list = os.listdir(path)
    return file_list