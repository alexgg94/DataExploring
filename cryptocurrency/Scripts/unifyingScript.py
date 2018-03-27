import os.path
import sys
import csv
import pandas as pd
from colorama import Fore

def join_temporal_files(file_index):
    try:
        for _file in range(0, file_index):
            if _file == 0:
                df = pd.read_csv(str(_file))
                df.to_csv("output.csv", header=["Cryptocurrency", "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap"], index=None)
            else:
                df = pd.read_csv(str(_file))
                with open('output.csv', 'a') as output_file:
                    df.to_csv(output_file, header=None, index=None)
            os.remove(str(_file))
        print(Fore.GREEN + "Joining process done! ")
    except:
        print(Fore.RED + "Error while joining files ")

def process_csv_file(fileName, file_index):
    try:
        df = pd.read_csv(fileName)
        df.insert(0,"cryptocurrency", fileName.split("/")[-1].split("_price")[0])
        df.to_csv(str(file_index), header=None, index=None)
        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print ("Usage -> python unifyingScript.py file_1.csv file_2.csv .... file_n.csv <- \n")
    
    else:
        file_index = 0
        for argument in sys.argv[1:]:
            extension = os.path.splitext(argument)[1]
            if extension == ".csv":
                print(Fore.BLACK + "Processing " + argument)
                process_csv_file(argument, file_index)
                file_index += 1

            else:
                print(Fore.YELLOW +argument + " Ignored")
        
        print(Fore.BLACK + "Joining temporal files ")
        join_temporal_files(file_index)