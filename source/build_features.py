# Đọc dữ liệu raw
import pandas as pd
from time import time
import random

dataFrame_raw = pd.read_csv("..\\data\\raw\\dataset.csv", encoding="ISO-8859-1", header=None)
dataFrame_raw.columns = ["label", "time", "date", "query", "username", "text"]

dataFrame = dataFrame_raw[["label", "text"]]

# Cắt nhỏ kích thước dữ liệu
start_time = time()

dataFrame_positive = dataFrame[dataFrame["label"] == 4]
dataFrame_negative = dataFrame[dataFrame["label"] == 0]

dataFrame_positive = dataFrame_positive.iloc[:100000] # :int(len(dataFrame_positive) / 40)
dataFrame_negative = dataFrame_negative.iloc[:100000] # :int(len(dataFrame_negative) / 40)

dataFrame = pd.concat([dataFrame_positive, dataFrame_negative])

print('Cắt dữ liệu: ', time() - start_time)

# [ (text, label) ] -> [ ( {token: số lần lặp}, label ) ]
from tokenize_clean_data import tokenize_clean_sentence

start_time = time()

data = []
for index, df in dataFrame.iterrows():
    try:
        if df["label"] == 4:
            data.append( (tokenize_clean_sentence(df["text"]), 1) )
        else:
            data.append( (tokenize_clean_sentence(df["text"]), 0) )
    except:
        print(index)

print('Làm sạch dữ liệu: ', time() - start_time)

# Chia thành tập train và test


start_time = time()

random.shuffle(data)

trim_index = int(len(data) * 0.8)

train_data = data[:trim_index]
test_data = data[trim_index:]

print('Chia tập: ', time() - start_time)

# Lưu lại các tập 
import pickle

start_time = time()

pickleFile = open('.\\..\\data\\processed\\before_train.pickle', 'wb')
pickle.dump(train_data, pickleFile)
pickleFile.close()

pickleFile = open('.\\..\\data\\processed\\test.pickle', 'wb')
pickle.dump(test_data, pickleFile)
pickleFile.close()

print('Lưu dữ liệu: :', time() - start_time)