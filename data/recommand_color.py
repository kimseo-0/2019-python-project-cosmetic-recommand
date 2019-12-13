from my_module import product as pd
from my_module import product_info as pi

product_id_list = pd.get_product_id_list_from_file()

inventory = pi.Inventory()
prodcutinfo_list = inventory.get_productinfo_list()
