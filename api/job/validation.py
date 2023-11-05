from rest_framework.response import Response
from api import messages
def validate_rdata(data):
    if type(data['quote_no'])!=str:
        return 2018
        # errors['quote_no'] = 'quote_no must be a string'
    if type(data['logo_same_for_all'])!=bool:
        return 2019
        # errors['logo_same_for_all'] = 'logo_same_for_all must be a True or False'
    if type(data['logo_name'])!=str:
        return 2020
        # errors['logo_same_for_all'] = 'logo_same_for_all must be a string'
    if type(data['send_art_to_customer'])!=bool:
        return 2018
        # errors['send_art_to_customer'] = 'send_art_to_customer must be a True or False'
    if type(data['proof_request_type'])!=str:
        return 2021
        # errors['proof_request_type'] = 'proof_request_type must be a string'
        
    if type(data['customer_no'])!=str:
        return 2023
        # errors['customer_no'] = 'customer_no must be a string'
    if type(data['customer_name'])!=str:
        return 2023
        # errors['customer_name'] = 'customer_name must be a string'
    if type(data['segment_no'])!=str:
        return 2024
        # errors['segment_no'] = 'segment_no must be a string'
    if type(data['note'])!=str:
        return 2025
        # errors['note'] = 'note must be a string'
    if type(data['status'])!=str:
        return 2026
        # errors['status'] = 'status must be a string'
    for i in data['item']:
        if type (i['item']) != str:
            return 2027
            # errors['item'] = 'item must be a string'
        if type(i['product_color'])!=str:
            return 2028
            # errors['product_color'] = 'product_color must be a string'
        if type(i['imprint_color'])!=str:
            return 2029
            # errors['imprint_color'] = 'imprint_color must be a string'
        if type (i['imprint_location'])!= str:
            return 2030
            # errors['imprint_location'] = 'imprint_location must be a string'
        if type (i['imprint_method'])!= str:
            return 2031
            # errors['imprint_method'] = 'imprint_method must be a string'
        if type (i['imprint_instructions'])!= str:
            return 2032
            # errors['imprint_instructions'] = 'imprint_instructions must be a string'
    
        
    return ""    
    