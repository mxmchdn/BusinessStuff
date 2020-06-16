from suds.client import Client
#from urllib import getproxies


VIES_URL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

client = Client(VIES_URL)

response = client.service.checkVat(countryCode='BE', vatNumber='0893134428')

print(response)
