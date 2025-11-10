from .models import original_message
import json

class Data:
    def get_products(self, parameters = None):
        originalMessage = original_message.objects.all()
        '''if parameters: 
            if 'quantity' in parameters: 
                originalMessage = originalMessage.filter(quantity = parameters['quantity'])
            if 'title' in parameters: 
                originalMessage = originalMessage.filter(title = parameters['title'])'''
            
        return originalMessage
'''{
    "parameters": {
        "title": "Bottle",
        "quantity": 0
    }
}'''
