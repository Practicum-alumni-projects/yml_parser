import gspread

from datetime import datetime
from lxml import etree
from test_list import res

CREDENTIALS_FILE = 'service_account_token.json'
SPREADSHEET_ID = '1d8qVc3Ayt1O1eBU-ikcXrbLvCLHWawpd5WPniVajmRc'

root = etree.Element('yml_catalog',
                     date=datetime.today().strftime('%Y-%m-%d %H:%M'))

tags = ('name', 'url', 'category Id', 'price', 'currency Id')
params = ('Цена по скидке', 'Дата окончания скидки', 'Цена за подписку',
          'Ежемесячная цена', 'Ежемесячная цена по скидке',
          'Дата окончания ежемесячной скидки', 'Ближайшая дата',
          'Формат обучения', 'Есть видеоуроки', 'Есть текстовые уроки',
          'Есть вебинары', 'Есть домашние работы', 'Есть тренажеры',
          'Есть сообщество', 'Сложность', 'Тип обучения',
          'Есть бесплатная часть', 'С трудоустройством', 'Результат обучения',
          'Часы в неделю', 'Классы')


def parse_sheet():
    client = gspread.service_account(filename=CREDENTIALS_FILE)
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.get_worksheet(0)
    return worksheet.get_all_records()


def create_yml():
    # res = parse_sheet()
    shop = etree.SubElement(root, 'shop')
    etree.SubElement(shop, 'name').text = res[0]['name_']
    etree.SubElement(shop, 'company').text = res[0]['company']
    etree.SubElement(shop, 'url').text = res[0]['url_']
    etree.SubElement(shop, 'email').text = res[0]['email']
    etree.SubElement(shop, 'picture').text = res[0]['picture']
    etree.SubElement(shop, 'description').text = res[0]['description']
    sets = etree.SubElement(shop, 'sets')
    offers = etree.SubElement(shop, 'offers')

    for i in range(len(res)):
        offer = etree.SubElement(offers, 'offer', id=res[i]['offer id'])
        set_id_to_sets(i, sets, res)
        for key, value in res[i].items():
            if key in tags:
                key = key.replace('_', '').split()
                etree.SubElement(offer, ''.join(key)).text = str(value)
            elif key == 'set id':
                etree.SubElement(
                    offer, 'set-ids'
                ).text = str(res[i]['set id']).split('\n')[0]
            elif key == 'Оплата в рассрочку':
                etree.SubElement(
                    offer, 'param', name='Оплата в рассрочку'
                ).text = str(res[i]['Оплата в рассрочку'])
            elif key == 'Продолжительность':
                etree.SubElement(
                    offer, 'param', name='Продолжительность', unit="месяц"
                ).text = str(res[i]['Продолжительность'])
            elif key == 'План Вводный модуль':
                etree.SubElement(
                    offer, 'param', name='План', unit='Введение'
                ).text = str(res[i]['План Вводный модуль'])
            elif key == 'План Модуль 1':
                etree.SubElement(
                    offer, 'param', name='План', unit='Модуль 1'
                ).text = str(res[i]['План Модуль 1'])
            elif key == 'Классы':
                pass
            elif key in params:
                etree.SubElement(offer, 'param', name=key).text = str(value)


def set_id_to_sets(i, sets, res):
    set_list = str(res[i]['set id']).replace('\n\n', ',').split(',')
    long = len(set_list) // 2
    for j in range(long):
        one_set = etree.SubElement(sets, 'set', id=set_list[j])
        etree.SubElement(one_set, 'name').text = set_list[j + long]
        etree.SubElement(one_set, 'url').text = str(res[i]['url'])


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
