import json
import os.path
import sys
import csv
import numpy as np
import pandas as pd
from colorama import Fore

def sort():
    try:
        df = pd.read_csv("output.csv", names = ["measure", "sensor", "value", "time"])
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values(by=["time"], ascending=True)
        df = pd.pivot_table(df, index=["time", "sensor"], columns=["measure"], values="value", fill_value="NaN")
        df.reset_index(inplace=True)
        df.to_csv("sorted_output.csv", index=None)
        print(Fore.GREEN + "Sorting process done! ")
        os.remove("output.csv")
    except:
        print(Fore.RED + "Error while sorting file ")

def write_to_file(line_to_append):
    with open("output.csv", 'a+') as outfile:
        outfile.write(line_to_append)

def process_json_file(fileName):
    try:
        with open(fileName) as file_content:
            for line in file_content:
                json_content = json.loads(line)
                write_to_file(str(json_content['sensor'][0]) + "," + str(json_content['sensor'][2:])+","+str(json_content['value'])+","+str(json_content['time']+"\n"))
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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print ("Usage -> python unifyingScript.py files_directory <- \n" \
        "Only .csv and .json files will be processed")
    
    else:
        for file in os.scandir(sys.argv[1]):
            extension = os.path.splitext(file.name)[1]
            if extension == ".csv":
                print(Fore.BLACK + "Processing " + file.name)
                process_csv_file(sys.argv[1]+file.name)

            elif extension == ".json":
                print(Fore.BLACK + "Processing " + file.name)
                process_json_file(sys.argv[1]+file.name)

            else:
                print(Fore.YELLOW +file.name + " Ignored")
        print(Fore.BLACK + "Sorting output by date...")
        sort()


