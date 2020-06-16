#!/usr/local/bin/python3
import zeep
import re
from argparse import ArgumentParser


class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def structure(CC, vatnumber):
    country_codes = ['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','GB','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','RO','SE','SI','SK']
    countries = ['Austria','Belgium','Bulgaria','Cyprus','Czech Republic','Germany','Denmark','Estonia','Greece','Spain','Finland','France','United Kingdom','Croatia','Hungary','Ireland','Italy','Lithuania','Luxembourg','Latvia','Malta','Netherlands','Poland','Portugal','Romania','Sweden','Slovenia','Slovakia']
    countrycode = CC
    vat = vatnumber
    vat_response = checkvat(countrycode, vat)
    if not vat_response['valid']:
        print('')
        print(bcolors.FAIL + 'VAT number is invalid!' + bcolors.ENDC)
        print('')
    else:
        print('')
        print(bcolors.OKGREEN + 'VAT number is valid!' + bcolors.ENDC)
        print('')
        print(bcolors.BOLD + 'Request date: ' + bcolors.ENDC + vat_response['requestDate'].strftime('%d %b %Y'))
        print(bcolors.BOLD + 'VAT number: ' + bcolors.ENDC + vat_response['countryCode'] + ' ' + vat_response['vatNumber'])
        print(bcolors.BOLD + 'Company name: ' + bcolors.ENDC + vat_response['name'])
        print(bcolors.BOLD + 'Address: ' + bcolors.ENDC)
        print(vat_response['address'])
        print('')


def checkvat(countrycode, vat):
    wsdl = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    client = zeep.Client(wsdl=wsdl)
    return client.service.checkVat(countrycode, vat)


if __name__ == "__main__":
    parser = ArgumentParser(description="VIES VAT checking API")
    parser.add_argument('countrycode', metavar='Country Code for vat number', type=str)
    parser.add_argument('vatnumber', metavar='Numbers of the vat number', type=str)
    args = parser.parse_args()
    structure(args.countrycode, args.vatnumber)