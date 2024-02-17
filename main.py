from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
  pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
new_contacts_list = []
new_contacts_list.append(contacts_list[0])
for record in contacts_list[1:]:
  parts = ''
  for i in record[:3]:
    parts += ' '
    parts += (''.join(i))
  parts = parts.split(' ')
  while '' in parts and len(parts) > 3:
      parts.remove('')
  record[0:3] = parts
  new_contacts_list.append(record)

contacts_list = new_contacts_list.copy()

for item in contacts_list:
  item[5] = re.sub(r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)*[\s]*(\d+)*[\)]*', r'+7(\2)\3-\4-\5 \6\7', item[5])

# Создание списка для хранения уникальных записей
unique_data = [contacts_list[0]]

# Создание словаря для хранения уникальных записей по ФИ
unique_records = {}

for record in contacts_list[1:]:
    lastname, firstname, surname, organization, position, phone, email = record
    key = (lastname, firstname)
    if key not in unique_records:
        unique_records[key] = record
    else:
        # Обновление записи, если есть недостающие данные
        existing_record = unique_records[key]
        if organization and not existing_record[3]:
            existing_record[3] = organization
        if position and not existing_record[4]:
            existing_record[4] = position
        if phone and not existing_record[5]:
            existing_record[5] = phone
        if email and not existing_record[6]:
            existing_record[6] = email

# Преобразование словаря обратно в список записей
for record in unique_records.values():
    unique_data.append(record)

#
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(unique_data)