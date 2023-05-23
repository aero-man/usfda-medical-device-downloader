'''
Flatten openFDA JSON into a dictionary.

This avoids making a column for every little thing, since some keys have 100s
of values that flatten into 100s of columns. Multi-valued keys will get a main
column plus an `additional` column for all other values. For example, a heart
pump may have dozens of nested "products" for every screw, wire, and tube that
it contains.
'''


import settings


class OpenFdaJsonCleaner():
    @staticmethod
    def clean(device_json):
        keys = settings.CSV_COLUMNS
        clean_dict = {key: None for key in keys}
        
        # Proprietary names
        try:
            prop_names = OpenFdaJsonCleaner.clean_multi_value_item(device_json['proprietary_name'])
            clean_dict['proprietary_name'] = prop_names['main']
            clean_dict['proprietary_names_additional'] = prop_names['additional']
        except Exception as e:
            print('ERROR while parsing JSON: ', e)

        # Establishment types
        try:
            estab_types = OpenFdaJsonCleaner.clean_multi_value_item(device_json['establishment_type'])
            clean_dict['establishment_type'] = estab_types['main']
            clean_dict['establishment_types_additional'] = estab_types['additional']
        except Exception as e:
            print('ERROR while parsing JSON: ', e)

        # Registration
        try:
            clean_dict['registration_number'] = device_json['registration']['registration_number']
            clean_dict['registration_fei_number'] = device_json['registration']['fei_number']
            clean_dict['registration_status_code'] = device_json['registration']['status_code']
            clean_dict['registration_initial_importer_flag'] = device_json['registration']['initial_importer_flag']
            clean_dict['registration_expiry_date_year'] = device_json['registration']['reg_expiry_date_year']
            clean_dict['registration_name'] = device_json['registration']['name']
            clean_dict['registration_address_line_1'] = device_json['registration']['address_line_1']
            clean_dict['registration_address_line_2'] = device_json['registration']['address_line_2']
            clean_dict['registration_city'] = device_json['registration']['city']
            clean_dict['registration_state_code'] = device_json['registration']['state_code']
            clean_dict['registration_iso_country_code'] = device_json['registration']['iso_country_code']
            clean_dict['registration_zip_code'] = device_json['registration']['zip_code']
            clean_dict['registration_postal_code'] = device_json['registration']['postal_code']
            clean_dict['registration_city'] = device_json['registration']['city']
        except Exception as e:
            print('ERROR while parsing JSON: ', e)

        # Registration US agent (ignoring the 15 rows of registration agent address, etc.)
        try:
            clean_dict['registration_us_agent_name'] = device_json['registration']['us_agent']['name']
            clean_dict['registration_us_agent_business_name'] = device_json['registration']['us_agent']['business_name']
        except Exception as e:
            print('ERROR while parsing JSON: ', e)

        # Misc. details
        try:
            clean_dict['pma_number'] = device_json['pma_number']
            clean_dict['k_number'] = device_json['k_number']
            products = OpenFdaJsonCleaner.clean_multi_value_item(device_json['products'])
            clean_dict['products_product_code'] = products['main']['product_code']
            clean_dict['products_created_date'] = products['main']['created_date']
            clean_dict['products_owner_operator_number'] = products['main']['owner_operator_number']
            clean_dict['products_exempt'] = products['main']['exempt']
            clean_dict['products_openfda_device_name'] = products['main']['openfda']['device_name']
            clean_dict['products_openfda_medical_specialty_description'] = products['main']['openfda']['medical_specialty_description']
            clean_dict['products_openfda_regulation_number'] = products['main']['openfda']['regulation_number']
            clean_dict['products_openfda_device_class'] = products['main']['openfda']['device_class']
            clean_dict['products_additional'] = products['additional']
        except Exception as e:
            print('ERROR while parsing JSON: ', e)

        return clean_dict


    @staticmethod
    def clean_multi_value_item(raw_json):
        try:
            cleaned_data = {
                'main': raw_json[0],
                'additional': raw_json[1:].replace('[', '').replace(']', '')
            }
        except Exception as e:
            print('ERROR: values not found for multi-value item.', e)
            cleaned_data = {
                'main': None,
                'additional': None
            }
        return cleaned_data


        

