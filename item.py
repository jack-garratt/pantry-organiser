

class Item():
    def __init__(self,name,quantity):
        self._name = name
        self._quantity = quantity
    
    def get_name(self):
        return self._name
    
    def get_quantity(self):
        return self._quantity
    
    def increment_quantity(self):
        from db_utils import increment_item
        increment_item(self)
        self._quantity +=1

    def decrement_quantity(self):
        from db_utils import decrement_item,delete_item
        decrement_item(self)
        self._quantity -=1
        if self._quantity == -1:
            delete_item(self)