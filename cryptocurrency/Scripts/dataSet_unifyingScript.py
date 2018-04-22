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
        
def sort():
    try:
        df = pd.read_csv(pathdest+"dataset_output.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values(by=["Date"], ascending=True)
    
        df.to_csv(pathdest+"sorted_dataset_output.csv", index=None)
        print(Fore.GREEN + "Sorting process done! ")
    except:
        print(Fore.RED + "Error while sorting file ")

def join_temporal_files():
    try:
        bitcoin_dataset_df = pd.read_csv(pathtemp + "bitcoin_dataset.csv")
        ethereum_dataset_df = pd.read_csv(pathtemp + "ethereum_dataset.csv")

        joined_dataset_df = pd.merge(bitcoin_dataset_df, ethereum_dataset_df, on="Date", suffixes=('_bitcoin', '_ethereum'), how="outer")
        joined_dataset_df.to_csv(pathdest + "dataset_output.csv", index=None)

        os.remove(pathtemp + "bitcoin_dataset.csv")
        os.remove(pathtemp + "ethereum_dataset.csv")

        print(Fore.GREEN + "Joining process done! ")
    except:
        print(Fore.RED + "Error while joining files ")

def process_csv_file(fileName):
    try:
        if fileName == pathori + "bitcoin_dataset.csv":
            df = pd.read_csv(fileName)
            df = df[["Date","btc_market_price","btc_market_cap","btc_blocks_size","btc_hash_rate","btc_difficulty","btc_n_unique_addresses"]]
            df["Date"] = pd.to_datetime(df["Date"])
            df.to_csv(pathtemp + "bitcoin_dataset.csv", header=["Date", "Price", "MarketCap", "BlockSize", "HashRate", "Difficulty", "Address"], index=None)
        elif fileName == pathori + "ethereum_dataset.csv":
            df = pd.read_csv(fileName)
            df = df[["Date(UTC)","eth_etherprice","eth_marketcap","eth_blocksize","eth_hashrate","eth_difficulty","eth_address"]]
            df["Date(UTC)"] = pd.to_datetime(df["Date(UTC)"])
            df.to_csv(pathtemp + "ethereum_dataset.csv", header=["Date", "Price", "MarketCap", "BlockSize", "HashRate", "Difficulty", "Address"], index=None)
        else:
            print("There is no case for " + fileName)

        print(Fore.GREEN + fileName + " Has been processed successfully")
    except:
        print(Fore.RED + "Error while processing " + fileName)

if __name__ == '__main__':
    init()
    for file in os.listdir(pathori):
        name = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]
        datatype = name.split("_")[-1]    
        if extension == ".csv":
            if datatype == "dataset":
                print(Fore.BLACK + "Processing " + file)
                process_csv_file(pathori + file)
            else:
                print(Fore.YELLOW +file + " Ignored")
        else:
            print(Fore.YELLOW +file + " Ignored")
        
    print(Fore.BLACK + "Joining temporal files ")
    join_temporal_files()
    print(Fore.BLACK + "Sorting output by date...")
    sort()