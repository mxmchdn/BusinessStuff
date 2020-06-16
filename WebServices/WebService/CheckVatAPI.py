#!/usr/local/bin/python3
import zeep, re, csv, time, os
from argparse import ArgumentParser
from pathlib import Path


def extract(file):
    with open(file, "r") as f:
        List = []
        read = csv.DictReader(f, delimiter=';', quotechar='|')
        for row in read:
            vat = row['VAT']
            List.append(vat)
    return List


def validity(CC, vatnumber):
    country_codes = ['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','GB','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','RO','SE','SI','SK']
    countrycode = CC
    vat = vatnumber
    if CC in country_codes:
        return checkvat(countrycode, vat)
    else:
        return({'valid': 'Country code not in the database'})




def checkvat(countrycode, vat):
    wsdl = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    try:
        client = zeep.Client(wsdl=wsdl)
        return client.service.checkVat(countrycode, vat)
    except:
        return {'valid': 'Server Down'}


if __name__ == "__main__":
    parser = ArgumentParser(description="VIES VAT checking API")
    parser.add_argument('file', metavar='file with VAT number')
    args = parser.parse_args()
    
    file = Path(args.file).absolute()
    VAT_extraction = extract(file)

    out_path = 'media/tables_outputs/Output_' + args.file.split('/')[2]

    with open(out_path, "w", newline='') as csvfile:
        fields = ['Name', 'TVA_Number', 'TVA_Name', 'TVA_Address', 'TVA_CP_Country', 'Exist', 'Request_Date']
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=';')
        writer.writeheader()

        for VAT in VAT_extraction:
            dictionary = validity(VAT[:2], VAT[2:])
            if dictionary['valid'] == 'Country code not in the database':
                writer.writerow({'Name': '', 'TVA_Number': VAT, 'TVA_Name': '---', 'TVA_Address': '---', 'TVA_CP_Country': '---', 'Exist': dictionary['valid'], 'Request_Date': time.strftime('%d %b %Y', time.gmtime())})
            elif dictionary['valid'] == 'Server Down':
                writer.writerow({'Name': '', 'TVA_Number': VAT, 'TVA_Name': '---', 'TVA_Address': '---', 'TVA_CP_Country': '---', 'Exist': dictionary['valid'], 'Request_Date': time.strftime('%d %b %Y', time.gmtime())})
            else:
                if dictionary['valid']:
                    vatName = dictionary['name']
                    if len(dictionary['address']) > 3:
                        Adresses = dictionary['address'].split('\n')
                        address = Adresses[0]
                        cp = Adresses[1]
                    else:
                        address = dictionary['address']
                        cp = address
                    date = dictionary['requestDate'].strftime('%d %b %Y')
                    writer.writerow({'Name': '', 'TVA_Number': VAT, 'TVA_Name': vatName, 'TVA_Address': address, 'TVA_CP_Country': cp, 'Exist': True, 'Request_Date': date})
                else:
                    date = dictionary['requestDate'].strftime('%d %b %Y')
                    writer.writerow({'Name': '', 'TVA_Number': VAT, 'TVA_Name': '---', 'TVA_Address': '---', 'TVA_CP_Country': '---', 'Exist': False, 'Request_Date': date})
            time.sleep(2)
    print(out_path)