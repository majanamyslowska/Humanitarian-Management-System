# from install_libraries import *
import pycountry


def country_dict():
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
    return countries
    
#country_dictionary = country_dict("Spain")
#print (country_dictionary)

def get_country_code(input_country):
    countries = country_dict()
    return countries.get(input_country)

#country_code = get_country_code("Spain")




