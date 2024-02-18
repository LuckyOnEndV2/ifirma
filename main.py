import json
import time
from datetime import datetime
import requests
import pipedrive_service

pipeservice = pipedrive_service

def sign_raw(data, key):
    import hmac
    from binascii import unhexlify
    from hashlib import sha1

    api_key = key if isinstance(key, bytes) else unhexlify(key)
    bin_data = data.encode(encoding="utf-8", errors="strict")

    return hmac.new(api_key, bin_data, sha1).hexdigest()

def get_invoice_by_id(id):
    username = "nikodem.pawlowski@me.com"
    api_token = "49311F4D221B0E63"
    url = f"https://www.ifirma.pl/iapi/faktury.json"

    sign_data = f"{url}{username}faktura"

    hashWiadomosci = sign_raw(sign_data, api_token)
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json; charset=UTF-8',
        'Authentication': f"IAPIS user={username}, hmac-sha1={hashWiadomosci}"
    }

    print("get invoice by id reuqest send")
    response = requests.get(f"{url}?dataOd={datetime.now().strftime('2024-02-12')}", headers=headers)
    print("get invoice by id reuqest success")
    data = response.json()
    for invoice in data['response']['Wynik']:
        if invoice['FakturaId'] == id:
            print("get invoice by id , invoice found")
            return invoice['PelnyNumer'], invoice['Brutto']

    return None, None


def send_mail_country(email, invoice_number):
    email_url = "https://www.ifirma.pl/iapi/rachunekkraj/send"
    username = "MICHAL@SPAUTOMOTIVE.PL"
    api_token = "0FB0456A7BD7B3A4"

    url = f"{email_url}/{invoice_number}.json?wyslijEfaktura=true"

    data = {
        "Tekst": " ",
        "SkrzynkaEmail": "app@spautomotive.pl",
        "SzablonEmail": "Rachunek prowizja",
        "SkrzynkaEmailOdbiorcy": email
    }

    json_content = json.dumps(data, ensure_ascii=False)

    base_url = url.split("?")[0]
    sign_data = f"{base_url}{username}rachunek{json_content or ''}"

    hashWiadomosci = sign_raw(sign_data, api_token)

    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json; charset=UTF-8',
        'Authentication': f"IAPIS user={username}, hmac-sha1={hashWiadomosci}"
    }

    print(f"send email {invoice_number}")
    response = requests.post(url, data=json_content.encode('utf-8'), headers=headers)
    data_response = response.json()
    print(f"send email success {invoice_number}")


def send_mail(email, invoice_number, invoice_nr, price, freightInsure, freight, broker, last_price):
    template = """
    Dzień dobry,

    W załączniku znajduje się faktura {numer_faktury} za fracht morski na kwotę {kwota} USD.

    Faktura zawiera:
    Usługa brokera: {usluga_brokera}
    Odbiór z aukcji i fracht morski do Rotterdamu: {odbior_frachtu}
    Ubezpieczenie cargo: {ubezpieczenie_cargo}
    Opłata za późną płatność i parking na aukcji: {oplata}

    Płatność jest w USD i jest realizowana na nasze polskie konto walutowe w banku PKO BP.

    Bank: PKO BP
    Numer konta IBAN: PL57 1020 4900 0000 8902 3092 5632
    SWIFT: BPKOPLPW

    
    """

    email_url = "https://www.ifirma.pl/iapi/fakturawaluta/send"
    username = "nikodem.pawlowski@me.com"
    api_token = "49311F4D221B0E63"

    url = f"{email_url}/{invoice_number}.json?wyslijEfaktura=true"

    email_content = template.format(
        numer_faktury=f'{invoice_nr}',
        kwota=f'{price}',
        usluga_brokera=f'{broker}USD',
        odbior_frachtu=f'{freight}USD',
        ubezpieczenie_cargo=f'{freightInsure}USD',
        oplata=f'{last_price}USD'
    )

    data = {
        "Tekst": email_content,
        "SkrzynkaEmail": "app@spautomotive.pl",
        "SzablonEmail": "Pusty",
        "SkrzynkaEmailOdbiorcy": email
    }

    json_content = json.dumps(data, ensure_ascii=False)

    base_url = url.split("?")[0]
    sign_data = f"{base_url}{username}faktura{json_content or ''}"

    hashWiadomosci = sign_raw(sign_data, api_token)

    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json; charset=UTF-8',
        'Authentication': f"IAPIS user={username}, hmac-sha1={hashWiadomosci}"
    }

    print(f"send email {invoice_number} {invoice_nr}")
    requests.post(url, data=json_content.encode('utf-8'), headers=headers)
    print(f"send email success {invoice_number} {invoice_nr}")

def create_country_invoice(data):
    try:
        username = "MICHAL@SPAUTOMOTIVE.PL"
        api_token = "0FB0456A7BD7B3A4"
        url = "https://www.ifirma.pl/iapi/rachunekkraj.json"

        json_content = json.dumps(data, ensure_ascii=False)
        sign_data = f"{url}{username}rachunek{json_content or ''}"

        hashWiadomosci = sign_raw(sign_data, api_token)

        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json; charset=UTF-8',
            'Authentication': f"IAPIS user={username}, hmac-sha1={hashWiadomosci}"
        }

        print("create invoce post")
        response = requests.post(url, data=json_content.encode('utf-8'), headers=headers)
        print("create invoce send")
        data_response = response.json()
        result = data_response['response']
        if result["Kod"] == 0:
            identyficator = result["Identyfikator"]
            print(f"create invoce identyfikator {identyficator}")
            return 0, (int)(identyficator)
        else:
            print(f"create invoce error")
            return 500, 0
    except Exception as e:
        return 500, 0

def create_invoice(data):
    try:
        username = "nikodem.pawlowski@me.com"
        api_token = "49311F4D221B0E63"
        url = "https://www.ifirma.pl/iapi/fakturawaluta.json"

        json_content = json.dumps(data, ensure_ascii=False)
        sign_data = f"{url}{username}faktura{json_content or ''}"

        hashWiadomosci = sign_raw(sign_data, api_token)

        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json; charset=UTF-8',
            'Authentication': f"IAPIS user={username}, hmac-sha1={hashWiadomosci}"
        }

        print("create invoce post")
        response = requests.post(url, data=json_content.encode('utf-8'), headers=headers)
        print("create invoce send")
        data_response = response.json()
        result = data_response['response']
        if result["Kod"] == 0:
            identyficator = result["Identyfikator"]
            print(f"create invoce identyfikator {identyficator}")
            return 0, (int)(identyficator)
        else:
            print(f"create invoce error")
            return 500, 0
    except Exception as e:
        return 500, 0

def create_new_invoice(products):
    for product in products:
        nip = ""
        if product['e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_subpremise'] == None:
            nip = ""
        else:
            nip = product['e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_subpremise']
        ulica = ""
        if product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_route"] == None and product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_street_number"] == None:
            if product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91"] != None:
                ulica = product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91"].split(",")[0]
        else:
            ulica = f'{product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_route"]} {product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_street_number"]}'

        if product['6b12c94620ef88cea439f652fc648e4b5036ef2f'] == "46":
            invoice_model = {
                "Zaplacono": 0,
                "NumerKontaBankowego": "40102052420000240204694057",
                "DataWystawienia": datetime.now().strftime("%Y-%m-%d"),
                "MiejsceWystawienia": "WROCŁAW",
                "DataSprzedazy": datetime.now().strftime("%Y-%m-%d"),
                "FormatDatySprzedazy": "DZN",
                "SposobZaplaty": "PRZ",
                "WpisDoKpir": "NIE",
                "Numer": None,
                "Pozycje": [
                    {
                        "Ilosc": 1,
                        "CenaJednostkowa": product['cd515a5b699d2f76e1d2df06068c5ada9c28df5e'],
                        "NazwaPelna": f"Prowizja za organizacje importu pojazdu z USA: {product['title']}",
                        "Jednostka": "szt.",
                    }
                ],
                "Kontrahent": {
                    "Nazwa": product['8edef253a2dab4c978cca356b4ca689b8d089634'],
                    "Ulica": ulica,
                    "KodPocztowy": product['e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_postal_code'],
                    "Kraj": product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_country"],
                    "Miejscowosc": product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_locality"],
                    "Email": product["person_id"]["email"][0]["value"]
                }
            }
            status, new_invoice = create_country_invoice(invoice_model)
            if status == 0:
                send_mail_country(product["person_id"]["email"][0]["value"], new_invoice)
                pipedrive_service.mark_as_sent_country(product["id"])

        if product['5f784ebfd4428d6e26e2af34d67b268f6b22ca0f'] == "45":
            invoice_model = {
                "TypSprzedazy": "KRAJOWA",
                "ZaplaconoNaDokumencie": 0,
                "Zaplacono": 0,
                "LiczOd": "BRT",
                "NumerKontaBankowego": "PL57102049000000890230925632",
                "DataWystawienia": datetime.now().strftime("%Y-%m-%d"),
                "MiejsceWystawienia": "POZNAŃ",
                "DataSprzedazy": datetime.now().strftime("%Y-%m-%d"),
                "FormatDatySprzedazy": "DZN",
                "SposobZaplaty": "PRZ",
                "Jezyk": "en",
                "Waluta": "USD",
                "KursWalutyWidoczny": False,
                "KursWalutyZDniaPoprzedzajacegoDzienWystawieniaFaktury": currency,
                "RodzajPodpisuOdbiorcy": "BPO",
                "WidocznyNumerGios": False,
                "WidocznyNumerBdo": False,
                "Numer": None,
                "Pozycje": [
                    {
                        "StawkaVat": 0.00,
                        "Ilosc": 1,
                        "CenaJednostkowa": product['463274f945608f73a35db47670b946186f723386'],
                        "NazwaPelna": f"Fracht morski - Rotterdam: {product['title']}",
                        "Jednostka": "szt",
                        "TypStawkiVat": "PRC"
                    }
                ],
                "Kontrahent": {
                    "Nazwa": product['8edef253a2dab4c978cca356b4ca689b8d089634'],
                    "NIP": nip,
                    "Ulica": ulica,
                    "KodPocztowy": product['e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_postal_code'],
                    "Kraj": product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_country"],
                    "Miejscowosc": product["e134f8360b17a18963ca6ea8cfaa7e0b156b7f91_locality"],
                }
            }
            print("create invoice")
            status, new_invoice = create_invoice(invoice_model)
            if status == 0:
                invoice_nr, price = get_invoice_by_id(new_invoice)
                send_mail(product["person_id"]["email"][0]["value"], new_invoice, invoice_nr, price, product['10cb2dd06a7a60d9d9e19bd3819a6569ffb208c1'], product['5073621992b2b327ea4ca4733833c97af8aadc4e'],product['199cc63d9c8efe4d49249d9a7e97318015d8cb10'], product['4f14897cef15702d7cf7583bea70e89bafa36646'])
                pipedrive_service.mark_as_sent(product["id"])

while True:
    try:
        #time.sleep(20)
        product_to_create_invoice = pipeservice.get_data()

        if len(product_to_create_invoice) > 0:
            print("get currency started")
            response = requests.get("https://open.er-api.com/v6/latest/USD")
            response.raise_for_status()
            responseObject = response.json()
            currency = responseObject['rates']['PLN']
            print("get currency finished")
            create_new_invoice(product_to_create_invoice)
    except Exception as ex:
        print(ex.args)
        time.sleep(10)
        continue
