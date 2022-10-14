import csv
import json

csv_file_path_1 = r'category.csv'
json_file_path_1 = r'category.json'

csv_file_path_2 = r'ad.csv'
json_file_path_2 = r'ad.json'

csv_file_path_3 = r'location.csv'
json_file_path_3 = r'location.json'

csv_file_path_4 = r'user.csv'
json_file_path_4 = r'user.json'


def csv_to_json(csv_file_path, json_file_path, model):
    data = []
    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            to_add = {'model': model, 'pk': int(row['Id']) if 'Id' in row else int(row['id'])}
            if 'Id' in row:
                del row['Id']
            else:
                del row['id']
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price'] = int(row['price'])

            if 'category_id' in row:
                row['category_id'] = int(row['category_id'])
            if 'location_id' in row:
                row['location_id'] = [int(row['location_id'])]
            if 'author_id' in row:
                row['author_id'] = int(row['author_id'])
            if 'lat' in row:
                row['lat'] = float(row['lat'])
            if 'lng' in row:
                row['lng'] = float(row['lng'])
            if 'age' in row:
                row['age'] = int(row['age'])
            to_add['fields'] = row

            data.append(to_add)

    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        json_s = json.dumps(data, ensure_ascii=False, indent=4)
        jsonf.write(json_s)


csv_to_json(csv_file_path_1, json_file_path_1, 'ads.category')
csv_to_json(csv_file_path_2, json_file_path_2, 'ads.ad')
csv_to_json(csv_file_path_3, json_file_path_3, 'users.location')
csv_to_json(csv_file_path_4, json_file_path_4, 'users.user')
