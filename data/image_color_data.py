import numpy as np
import cv2

from my_module import product as pd
from my_module import grabcut

product_id_list = pd.get_product_id_list_from_file()

for product_id in product_id_list[10:] :
    color_id_list = pd.get_color_id_list_from_file(product_id)
    pd.create_forlder('extract_image/'+product_id)

    for color_id in color_id_list :
        
         
        filename = "image/"+product_id+"/"+color_id+'.jpg'
        
        product_image = grabcut.Grabcut(filename, product_id, color_id)
        product_image.grabcut_image()
        break
    break
        