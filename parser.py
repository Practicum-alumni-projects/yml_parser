import gspread

from datetime import datetime
from lxml import etree
from test_list import res

CREDENTIALS_FILE = 'service_account_token.json'
SPREADSHEET_ID = '1d8qVc3Ayt1O1eBU-ikcXrbLvCLHWawpd5WPniVajmRc'

root = etree.Element('yml_catalog',
                     date=datetime.today().strftime('%Y-%m-%d %H:%M'))


def parse_sheet():
    client = gspread.service_account(filename=CREDENTIALS_FILE)
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.get_worksheet(0)
    return worksheet.get_all_records()


# Далее длина строки игнорируется для читаемости
def create_yml():
    # res = parse_sheet()
    shop = etree.SubElement(root, 'shop')
    etree.SubElement(shop, 'name').text = res[0]['name_']
    etree.SubElement(shop, 'company').text = res[0]['company']
    etree.SubElement(shop, 'url').text = res[0]['url_']
    etree.SubElement(shop, 'email').text = res[0]['email']
    sets = etree.SubElement(shop, 'sets')
    offers = etree.SubElement(shop, 'offers')

    for i in range(len(res)):
        offer = etree.SubElement(offers, 'offer', id=res[i]['offer id'])
        etree.SubElement(offer, 'name').text = res[i]['name']
        etree.SubElement(offer, 'url').text = res[i]['url']
        etree.SubElement(offer, 'categoryId').text = str(res[i]['category Id']).split('\n')[0]
        set_id_to_sets(i, sets, res)  # Разобраться с сетами!
        etree.SubElement(offer, 'set-ids').text = str(res[i]['set id']).split('\n')[0]
        etree.SubElement(offer, 'price').text = str(res[i]['price'])
        etree.SubElement(offer, 'currencyId').text = res[i]['currency Id']
        etree.SubElement(offer, 'param', name='Цена по скидке').text = res[i]['Цена по скидке']
        etree.SubElement(offer, 'param', name='Дата окончания скидки').text = res[i]['Дата окончания скидки']
        etree.SubElement(offer, 'param', name='Цена за подписку').text = res[i]['Цена за подписку']
        etree.SubElement(offer, 'param', name='Оплата в рассрочку').text = str(res[i]['Оплата в рассрочку'])  # Доработать таблицу и переписать!
        etree.SubElement(offer, 'param', name='Ежемесячная цена').text = str(res[i]['Ежемесячная цена'])
        etree.SubElement(offer, 'param', name='Ежемесячная цена по скидке').text = str(res[i]['Ежемесячная цена по скидке'])
        etree.SubElement(offer, 'param', name='Дата окончания ежемесячной скидки').text = str(res[i]['Дата окончания ежемесячной скидки'])
        etree.SubElement(offer, 'param', name='Ближайшая дата').text = str(res[i]['Ближайшая дата'])
        etree.SubElement(offer, 'param', name='Продолжительность', unit="месяц").text = str(res[i]['Продолжительность'])  # Доработать таблицу и переписать!
        etree.SubElement(offer, 'param', name='План', unit='Введение').text = str(res[i]['План Вводный модуль'])  # Доработать таблицу и переписать!
        etree.SubElement(offer, 'param', name='План', unit='Модуль 1').text = str(res[i]['План Модуль 1'])  # Доработать таблицу и переписать!
        etree.SubElement(offer, 'param', name='Формат обучения').text = str(res[i]['Формат обучения'])
        etree.SubElement(offer, 'param', name='Есть видеоуроки').text = str(res[i]['Есть видеоуроки'])
        etree.SubElement(offer, 'param', name='Есть текстовые уроки').text = str(res[i]['Есть текстовые уроки'])
        etree.SubElement(offer, 'param', name='Есть вебинары').text = str(res[i]['Есть вебинары'])
        etree.SubElement(offer, 'param', name='Есть домашние работы').text = str(res[i]['Есть домашние работы'])
        etree.SubElement(offer, 'param', name='Есть тренажеры').text = str(res[i]['Есть тренажеры'])
        etree.SubElement(offer, 'param', name='Есть сообщество').text = str(res[i]['Есть сообщество'])
        etree.SubElement(offer, 'param', name='Сложность').text = str(res[i]['Сложность'])
        etree.SubElement(offer, 'param', name='Тип обучения').text = str(res[i]['Тип обучения'])
        etree.SubElement(offer, 'param', name='Есть бесплатная часть').text = str(res[i]['Есть бесплатная часть'])
        etree.SubElement(offer, 'param', name='С трудоустройством').text = str(res[i]['С трудоустройством'])
        etree.SubElement(offer, 'param', name='Результат обучения').text = str(res[i]['Результат обучения'])
        etree.SubElement(offer, 'param', name='Часы в неделю').text = str(res[i]['Часы в неделю'])
        # etree.SubElement(offer, 'param', name='Классы').text = str(res[i]['Классы'])  # Доработать таблицу и переписать!
        etree.SubElement(offer, 'picture').text = res[i]['picture']
        etree.SubElement(offer, 'description').text = res[i]['description']


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
