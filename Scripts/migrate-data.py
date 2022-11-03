import csv
import requests

url_target = 'http://127.0.0.1:5000/transaction'
auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Njc1OTk4MjgsImlhdCI6MTY2NzUxMzQyOCwic3ViIjoxfQ.eDzhxS_i1HWKRfFgfZwECAvS3i8J3Y2R2z40u5bwG9E'


def upload_row(csv_row):
    cost = csv_row[0].replace('$', '').replace('.', '')
    c = int(cost)
    tax = int(c / 1.0625)

    payload = {'location': csv_row[2],
               'cost': cost,
               'tax': tax,
               'purchase_time': csv_row[1]}

    res = requests.post(url=url_target,
                        headers={'Authorization': auth},
                        data=payload)

    print("Response: ", res.status_code)


with open('mig.csv', 'r') as file:
    reader = csv.reader(file)
    header = False
    for row in reader:
        if not header:
            header = True
            continue
        upload_row(row)
