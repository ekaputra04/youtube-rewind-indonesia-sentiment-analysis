from pymongo import MongoClient

# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['youtube_rewind_indonesia']  # Ganti 'nama_database' dengan nama database Anda

# Mendefinisikan collections
collect_collection = db['collect_2015']
cleansing_collection = db['preprocessing_2015']
cleansing_new_collection = db['preprocessing_new_2015']

# Mengambil semua data dari collection "cleansing"
cleansing_data = cleansing_collection.find()

# Proses setiap dokumen di "cleansing" untuk menemukan data lengkap di "collect"
for cleansing_doc in cleansing_data:
    # Mencari dokumen lengkap di "collect" berdasarkan _id
    collect_doc = collect_collection.find_one({"_id": cleansing_doc["_id"]})
    
    if collect_doc:
        # Menyimpan dokumen lengkap ke collection "cleansing new"
        cleansing_new_collection.insert_one(collect_doc)

print("Proses selesai.")
