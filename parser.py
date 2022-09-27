import gspread
import json

from datetime import datetime
from lxml import etree

# from test_list import res

CREDENTIALS_FILE = 'service_account_token.json'

root = etree.Element('yml_catalog',
                     date=datetime.today().strftime('%Y-%m-%d %H:%M'))

tags = ('name', 'url', 'category Id', 'price', 'currency Id',
        'picture', 'description')
params = ('Ссылка на контент курса', 'Ежемесячная цена', 'Ближайшая дата', 'Формат обучения',
          'Есть видеоуроки', 'Есть текстовые уроки',
          'Есть вебинары', 'Есть домашние работы', 'Есть тренажеры',
          'Есть сообщество', 'Сложность', 'Тип обучения',
          'Есть бесплатная часть', 'С трудоустройством', 'Результат обучения',
          'Часы в неделю')


def settings():
    with open('settings_test.txt', 'r') as sf:
        return json.loads(sf.read())


config = settings()
url = config['url']
work_sh = int(config['worksheet']) - 1


def parse_sheet():
    client = gspread.service_account(filename=CREDENTIALS_FILE)
    sheet = client.open_by_url(url)
    worksheet = sheet.get_worksheet(work_sh)
    return worksheet.get_all_records()


def create_yml():
    res = parse_sheet()
    shop = etree.SubElement(root, 'shop')
    etree.SubElement(shop, 'name').text = res[0]['company']
    etree.SubElement(shop, 'url').text = res[0]['url_']
    etree.SubElement(shop, 'email').text = res[0]['email']
    etree.SubElement(shop, 'picture').text = res[0]['picture_']
    etree.SubElement(shop, 'description').text = res[0]['description_']
    offers = etree.SubElement(shop, 'offers')

    for i in range(len(res)):
        offer = etree.SubElement(offers, 'offer', id=res[i]['offer id'])
        for key, value in res[i].items():
            if key == '':
                continue
            if key in tags and value:
                key = key.split()
                etree.SubElement(offer, ''.join(key)).text = str(value)
            elif key == 'Продолжительность':
                unit_selection(key, value, offer)
            elif key.split()[0] == 'План' and value:
                plan(key, value, offer)
            elif key == 'Ссылка на контент курса' and value:
                handle_urls_list(key, value, offer)
            elif key in params and value:
                etree.SubElement(offer, 'param', name=key).text = str(value)


def unit_selection(key, value, offer):
    unit = 'месяц'
    value = str(value).split(';')
    if len(value) > 1:
        unit = value[1]
    etree.SubElement(offer, 'param', name=key, unit=unit).text = value[0]


def plan(key, value, offer):
    key = key.split()
    value = replace_all(str(value)).split('\n\n')

    attributes = value[0].split(';')
    title = attributes[0]
    hours = attributes[1] if len(attributes) > 1 else 'None'
    order = key[2] if key[2] != 'модуль' else '0'
    content = value[1] if len(value) > 1 else 'Описание отсутствует'

    etree.SubElement(offer,
                     'param',
                     name=key[0],
                     title=title,
                     hours=str(hours),
                     order=str(order)).text = str(content).replace('\n', '')


def handle_urls_list(key, value, offer):
    url_protocol = 'https://'
    url_practicum_domain = 'practicum.yandex.ru'
    urls_splitter = ','
    urls_list = value.split(urls_splitter)
    for record in urls_list:
        record = record.strip()
        if (record.startswith(url_protocol)) and url_practicum_domain in record:
            etree.SubElement(offer, 'param', name=key).text = record


# Тут небольшой костыль для корректной обработки перевода строки в таблице.
def replace_all(text):
    substring = ('\r\n', '\n\r', '\n\r\n', '\r\n\r', '\n\r\n\r', '\r\n\r\n')
    for i in substring:
        text = text.replace(i, '\n\n')
    return text


def create_education_file():
    create_yml()
    result = etree.tostring(root,
                            encoding='utf-8',
                            pretty_print=True,
                            xml_declaration=True).decode()
    with open('education.yml', "w", encoding='utf-8') as file:
        file.write(result)


if __name__ == '__main__':
    create_education_file()
