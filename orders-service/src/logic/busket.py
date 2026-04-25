from common.schemas import BusketItem, Busket

buskets: dict[int, Busket] = {}

def insert_to_busket(user_id, product_id, quantity):
    if user_id not in buskets:
        buskets[user_id] = Busket(items=[])
    for item in buskets[user_id].items:
        if item.product_id == product_id:
            item.quantity += quantity
            return buskets[user_id]
    

    buskets[user_id].items.append(
        BusketItem(
            product_id=product_id,
            quantity=quantity
        )
    ) 
    return buskets[user_id]

