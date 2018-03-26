import json
import os.path
import sys
import csv
import pandas as pd
from colorama import Fore

def sort():
    try:
        df = pd.read_csv("output.csv", names = ["sensor", "value", "time"])
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values(by=["time"], ascending=True)
        df.to_csv("sorted_output.csv", header=["sensor", "value", "time"], index=None)
        print(Fore.GREEN + "Sorting process done! ")
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
                write_to_file(str(json_content['sensor'])+","+str(json_content['value'])+","+str(json_content['time']+"\n"))
        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)
    
def process_csv_file(fileName):
    try:
        with open(fileName) as file_content:
            #Skip headers
            next(file_content)
            for line in file_content:
                write_to_file(line)
        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print ("Usage -> python unifyingScript.py file_1 file_2 .... file_n <- \n" \
        "Only .csv and .json files will be processed")
    
    else:
        for argument in sys.argv[1:]:
            extension = os.path.splitext(argument)[1]
            if extension == ".csv":
                print(Fore.BLACK + "Processing " + argument)
                process_csv_file(argument)

            elif extension == ".json":
                print(Fore.BLACK + "Processing " + argument)
                process_json_file(argument)

            else:
                print(Fore.YELLOW +argument + " Ignored")
        print(Fore.BLACK + "Sorting output by date...")
        sort()


