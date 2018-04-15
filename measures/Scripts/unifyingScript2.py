import json
import os.path
import sys
import csv
import numpy as np
import pandas as pd
from colorama import Fore

pathori = "../data/raw/"
pathtemp = "../data/interim/"
pathdest = "../data/processed/"

def init():  
    if (os.path.isfile(pathtemp + "output.csv")):
        os.remove(pathtemp + "output.csv")
    if (os.path.isfile(pathdest + "sorted_output.csv")):
        os.remove(pathdest + "sorted_output.csv")

def sort():
    try:
        df = pd.read_csv(pathtemp+"output.csv", names = ["measure", "sensor", "value", "time"])
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values(by=["time"], ascending=True)
        df = pd.pivot_table(df, index=["time", "sensor"], columns=["measure"], values="value", fill_value="NaN")
        df.reset_index(inplace=True)
        df.to_csv(pathdest+"sorted_output.csv", index=None)
        print(Fore.GREEN + "Sorting process done! ")
    except:
        print(Fore.RED + "Error while sorting file ")

def write_to_file(line_to_append):
    with open(pathtemp + "output.csv", 'a+') as outfile:
        outfile.write(line_to_append)

def process_json_file(fileName):
    try:
        with open(fileName) as file_content:
            for line in file_content:
                json_content = json.loads(line)
                write_to_file(str(json_content['sensor'][0]) + "," + str(json_content['sensor']                                                                        [2:])+","+str(json_content['value'])+","+str(json_content['time']+"\n"))
 
        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)
    
def process_csv_file(fileName):
    try:
        with open(fileName) as file_content:
            #Skip headers
            next(file_content)
            for line in file_content:
                write_to_file(line[0] + "," + line[2:])
              
        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)

init()
for file in os.listdir(pathori):
    print (file)
    extension = os.path.splitext(file)[1]
    if extension == ".csv":
        print(Fore.BLACK + "Processing " + file)
        process_csv_file(pathori+file)
    elif extension == ".json":
        print(Fore.BLACK + "Processing " + file)
        process_json_file(pathori+file)
    else:
        print(Fore.YELLOW +file + " Ignored")
print(Fore.BLACK + "Sorting output by date...")
sort()


