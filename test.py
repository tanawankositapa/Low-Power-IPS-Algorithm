import csv
import pandas as pd
raw_df = pd.DataFrame()

# แบ่งข้อมูลออกเป็น block เพราะต้องการจะตรวขสอบว่าข้อมูลแต่ละชุดที่ได้มามี beacon ตัวไหนที่หายไป
with open('Dataset/dataset-fingerprint.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:

        row = [''.join(row)]
        raw_df = raw_df.append(row)


# ตั้งชื่อให้ column 0
raw_df.columns = ['Raw']
checklist = []
checklist2 = []
checklist3 = []
checklist4 = []
for row in raw_df.itertuples():
    mac = row.Raw.split(" ")
    # print(mac[11])
    # print(len(mac))
    if len(mac) == 1:
        checklist.append(mac[0])
        checklist2.append(mac[0])
        checklist3.append(mac[0])
        checklist4.append(mac[0])

    if len(mac) > 1:
        # note: mac[1] = mac address
        # note: mac[4] = RSSI
        # note: mac[10] = PosX
        # note: mac[11] = PosY
        checklist.append(mac[1])
        checklist2.append(mac[4])
        print(mac[11])
        # checklist3.append(mac[10])
        # checklist4.append(mac[11])
        # print(checklist4)


# print(checklist)
raw_df.insert(loc=0, column='Beacon', value=checklist)
raw_df.insert(loc=1, column='RSSI', value=checklist2)
# raw_df.insert(loc=2, column='PosX', value=checklist3)
# raw_df.insert(loc=3, column='PosY', value=checklist4)
raw_df.drop(columns='Raw', inplace=True)
print(raw_df.head(20))
