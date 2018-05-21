import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randrange

def extract_all_company_information_from_source(soup):
    companies = []

    for company_data in soup.find_all("article"):
        try:
            company_name = company_data.find("span", itemprop="name").get_text()
        except: company_name = ""

        try:
            street = company_data.find("span", itemprop="streetAddress").get_text().replace("\xa0", " ")
        except: street = ""

        try:
            city = company_data.find("span", itemprop="addressLocality").get_text()
        except: city = ""

        try:
            postal_code = company_data.find("span", itemprop="postalCode").get_text()
        except: postal_code = ""

        try:
            phone_number = company_data.find("span", class_="nummer").get_text()
        except: phone_number = ""

        try:
            email = company_data.find(class_="link email_native_app")['href']
            email = email.replace('mailto:','').replace('?subject=Anfrage%20über%20Gelbe%20Seiten','')
        except: email = ""

        try:
            website = company_data.find(class_="website hidden-xs").find("a", class_="link")['href']
        except: website = ""

        companies.append([company_name,street,city,postal_code,phone_number,email,website])

    return companies

company_leads = []
page = 10
loop = True

while loop:
    random_sleep = randrange(40, 90)
    print("Next iteration page " + str(page) + ". Sleep for " + str(random_sleep) + " seconds")
    sleep(random_sleep)

    try:
        response = requests.get('https://www.gelbeseiten.de/gebaeudereinigung/s' + str(page) +'/relevanz/details-e-mail-kontakt')
        html_source = response.text
    except:
        sleep(300)
        response = requests.get('https://www.gelbeseiten.de/gebaeudereinigung/s' + str(page) +'/relevanz/details-e-mail-kontakt')
        html_source = response.text


    soup = BeautifulSoup(html_source, 'html.parser')
    company_leads.extend(extract_all_company_information_from_source(soup))

    with open('.\SourceCodes\\' + str(page) + '.txt', "w") as text_file:
        text_file.write(html_source)

    with open('.\leads.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for row in company_leads:
            writer.writerow(row)

    page += 1

    if not html_source.__contains__("<span>Weiter</span>"):
        loop = False