import os.path
import sys
import csv
import pandas as pd
from colorama import Fore

pathori = "../data/raw/"
pathtemp = "../data/interim/"
pathdest = "../data/processed/"

def init():  
    for file in os.listdir(pathtemp):
        os.remove(pathtemp + file)
    
    for file in os.listdir(pathdest):
        os.remove(pathdest + file)
        
def join_temporal_files(file_index):
    try:
        for _file in os.listdir(pathtemp):
            print (_file)
            if not os.path.isfile(pathdest + "output.csv"):
                df = pd.read_csv(pathtemp + _file)
                df.to_csv(pathdest + "output.csv", header=["Cryptocurrency", "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap"], index=None)
            else:
                df = pd.read_csv(pathtemp + _file)
                with open(pathdest + 'output.csv', 'a') as output_file:
                    df.to_csv(output_file, header=None, index=None)
        print(Fore.GREEN + "Joining process done! ")
    except:
        print(Fore.RED + "Error while joining files ")

def process_csv_file(fileName, file_index):
    try:
        df = pd.read_csv(fileName)
        df.insert(0,"cryptocurrency", fileName.split("/")[-1].split("_price")[0])
        df.to_csv(pathtemp + str(file_index) + ".csv", header=None, index=None)
        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)

if __name__ == '__main__':
    init()
    file_index = 0
    for file in os.listdir(pathori):
        name = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]
        datatype = name.split("_")[-1]    
        if extension == ".csv":
            if datatype == "price":
                print(Fore.BLACK + "Processing " + file)
                process_csv_file(pathori + file, file_index)
                file_index += 1
            else:
                print(Fore.YELLOW +file + " Ignored")
        else:
            print(Fore.YELLOW +file + " Ignored")
        
    print(Fore.BLACK + "Joining temporal files ")
    join_temporal_files(file_index)