import os
import pandas as pd

def get_average(data):
    return round(sum(data)/len(data),2)

def get_trimmed(data, cut=2):
    data = sorted(data)[cut:-cut]
    return get_average(data)

def weighted(data, const = 1.25):
    weight = 0
    increment = 1/(len(data)-1)
    exponent = 0
    weighted_sum = 0
    for i in range(0, len(data)):
        weighted_sum+=data[i]*const**exponent
        weight+=const**exponent
        exponent+=increment
    return weighted_sum/weight

def save(data, filename, folder=""):
    if folder!="":
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
        if not os.path.exists(directory):
            os.makedirs(directory)
        folder+="\\"
    df = pd.DataFrame(data)
    df.to_excel(folder+filename+".xlsx", index=False, header=False)