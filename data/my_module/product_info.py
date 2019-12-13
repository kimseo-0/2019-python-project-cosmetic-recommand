import numpy as np

from my_module import product as pd

class Inventory :
    def __init__(self) :
        product_id_list = pd.get_product_id_list_from_file()
        self.product_id_list = product_id_list

        product_list = []
        for product_id in product_id_list :
            product = ProductInfo(product_id)
            product_list.append(product)
        self.product_list = product_list
        print(self.product_list[0])

    def get_productinfo_list(self) :
        return self.product_list

class ProductInfo :
    def __init__(self,product_id) :
        self.product_id = product_id
        
        product_info = pd.get_product_info_from_file(product_id)
        self.product_info = product_info
      
        color_id_list = pd.get_color_id_list_from_file(product_id)
        self.color_id_list = color_id_list
        
        product_color_list = []
        for color_id in color_id_list :
            product_color = ColorInfo(product_id,color_id)
            product_color_list.append(product_color)         
        self.product_color_list = product_color_list

    def __str__(self) :
        return self.product_info["product_name"]

class ColorInfo() :
    def __init__(self,product_id,color_id) :
        self.product_id = product_id
        self.color_id = color_id

        color_info = pd.get_product_color_info_from_file(product_id, color_id)
        self.color_info = color_info

    def __str__(self) :
        return self.color_id
 
    def compare_color(self, other) :
        color_A = self.color_info.RGB
        color_B = other.color_info.RGB

        a = np.array(color_A)
        b = np.array(color_B)
        distance = (sum((a-b)**2))**(1/2)
        return distance < 1
