from .models import unit_message
import json

class Data:
    def get_products(self, parameters = None):
        unitMessage = unit_message.objects.all()
        '''if parameters: 
            if 'quantity' in parameters: 
                unitMessage = unitMessage.filter(quantity = parameters['quantity'])
            if 'title' in parameters: 
                unitMessage = unitMessage.filter(title = parameters['title'])'''
            
        return unitMessage
'''{
    "parameters": {
        "title": "Bottle",
        "quantity": 0
    }
}'''
