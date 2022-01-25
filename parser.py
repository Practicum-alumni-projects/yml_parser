import gspread

from datetime import datetime
from lxml import etree
from test_list import res

CREDENTIALS_FILE = 'service_account_token.json'
SPREADSHEET_ID = '1d8qVc3Ayt1O1eBU-ikcXrbLvCLHWawpd5WPniVajmRc'

root = etree.Element('yml_catalog',
                     date=datetime.today().strftime('%Y-%m-%d %H:%M'))

tags = ('name', 'url', 'parentId', 'category Id', 'price', 'currency Id',
        'picture', 'description')
params = ('Ежемесячная цена', 'Ближайшая дата', 'Формат обучения',
          'Есть видеоуроки', 'Есть текстовые уроки',
          'Есть вебинары', 'Есть домашние работы', 'Есть тренажеры',
          'Есть сообщество', 'Сложность', 'Тип обучения',
          'Есть бесплатная часть', 'С трудоустройством', 'Результат обучения',
          'Часы в неделю')


def parse_sheet():
    client = gspread.service_account(filename=CREDENTIALS_FILE)
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.get_worksheet(1)
    return worksheet.get_all_records()


def create_yml():
    # res = parse_sheet()
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
            if key in tags and value:
                key = key.split()
                etree.SubElement(offer, ''.join(key)).text = str(value)
            elif key == 'Продолжительность':
                unit_selection(key, value, offer)
            # elif key.split()[0] == 'План':
            #     plan()
            elif key in params and value:
                etree.SubElement(offer, 'param', name=key).text = str(value)


def unit_selection(key, value, offer):
    unit = 'месяц'
    value = str(value).split(',')
    if len(value) > 1:
        unit = value[1]
    etree.SubElement(offer, 'param', name=key, unit=unit).text = value[0]


def plan():
    pass


def create_education_file():
    create_yml()
    result = etree.tostring(root,
                            encoding='utf-8',
                            pretty_print=True,
                            xml_declaration=True).decode()
    with open('education.yml', "w") as file:
        file.write(result)


if __name__ == '__main__':
    create_education_file()
