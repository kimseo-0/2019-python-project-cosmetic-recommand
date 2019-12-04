import numpy as np
import cv2

from module import product as pd
from module import grabcut

product_id_list = pd.get_product_id_list_from_file();

for product_id in product_id_list :
    color_id_list = pd.get_file_list_from_folder("image/"+product_id)
    
    for color_id in color_id_list :
        filename = "image/"+product_id+"/"+color_id
        
        product_image = grabcut.Grabcut(filename, product_id, color_id)
        product_image.grabcut_image()