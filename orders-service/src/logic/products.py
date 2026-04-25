from common.schemas import Product
from common.collections import products_collection

def get_products():
    products = products_collection.find().to_list(1000)
    print('#########', products)
    return products


def get_product_by_id(product_id):
    products = get_products()
    for product in products:
        if product.id == product_id:
            return product
    return None

def create_product(data: Product):
    new_product = data.momdel_dump(by_alias=True, exclude=["id"])
    result = products_collection.insert_one(new_product)
    print(result)