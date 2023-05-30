import pandas as pd
import json
from openpyxl import load_workbook
import os
import numpy as np
from pathlib import Path


def main():

    with open('data.json', 'r') as f:
        data = json.load(f)

    d = {'XAU': 'Gold', 'XAG': 'Silver', 'XPT': 'Platinum', 'XPD': 'Palladium' }
    for k in d:
        gold_data = data[k]
        df1 = pd.DataFrame()

        for i in range(0,13):
            df = pd.DataFrame(gold_data[i]["rates"])
            df1 = pd.concat([df1, df.T.reset_index().rename(columns= {'index':'IDate'})])
            df1.columns.name = None

        df1 = df1[(df1['IDate'] >= '2011-06-01')]
        df1 = df1.fillna(method='ffill')
        df1 = df1.fillna(0)
        df1.to_excel('{}Price.xlsx'.format(d[k]) , sheet_name=d[k])

if __name__ == '__main__':
    main()