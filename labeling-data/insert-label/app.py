from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

# Nama database dan collection
db_name = 'youtube_rewind_indonesia'
collection_name = 'labeling_2016' # Ganti dengan nama collection yang ingin dilabel

# Memuat value dari file .env
load_dotenv()

mongodb_url = os.getenv('URL_SANDY')
local_url = os.getenv('URL_LOCAL')

# Membuat koneksi ke MongoDB
client = MongoClient(local_url)

db = client[db_name]
collection = db[collection_name]

# Mengambil data dari MongoDB ke dalam dataframe
data = list(collection.find())
df = pd.DataFrame(data)

# Fungsi untuk meminta input pengguna
def label_komentar():
    while True:
        try:
            label = int(input("(1=positif, 2=netral, 3=negatif, 0=berhenti): "))
            if label == 1:
                return 'positif'
            elif label == 2:
                return 'netral'
            elif label == 3:
                return 'negatif'
            elif label == 0:
                return 'berhenti'
            else:
                print("Input tidak valid. Masukkan angka 1, 2, 3, atau 0.")
        except ValueError:
            print("Input tidak valid. Masukkan angka 1, 2, 3, atau 0.")

# Menambahkan label berdasarkan input pengguna hanya untuk data yang belum memiliki label
for i, row in df.iterrows():
    if 'label' not in row or pd.isnull(row['label']):
        print(f"\nKomentar: {row['textOriginal']}")
        label = label_komentar()
        if label == 'berhenti':
            break
        df.at[i, 'label'] = label
        collection.update_one({'_id': row['_id']}, {'$set': {'label': label}})
        labeled_count = collection.count_documents({'label': {'$exists': True}})
        print(f"{labeled_count} : Label '{label}' tersimpan untuk komentar: {row['textOriginal']}")

print("Program berhenti. Data yang sudah dilabeli tersimpan dalam MongoDB.")
