from flask import Flask, render_template, request
import requests
import pandas as pd
import numpy as np
import json
import geopy
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe


 
def cleaning(b,g,lo):
    
    data_comb = [b,g]
    data_df = pd.concat(data_comb)
    a= data_df.reset_index(drop=True)
    
    
    # Removing any duplicate results
    for i in a.index:
        print(i)
        for k in range(i+1,len(a)):
            print(i,k)
            try:
                if a.loc[i,'url'] == a.loc[k,'url']:
                    print(k)
                    a=a.drop(k)
            except:
                print('key missing')
    a=a.reset_index(drop=True)


    ## Removing results that dont have any description and image
    for j in a.index:
        print(j)

        if str(a.loc[j,"description"]) == 'nan' and str(a.loc[j,"image"])== 'nan':
            print('drop')
            a=a.drop(j)
    a=a.reset_index(drop=True)

    

    ## Removing results that are not of Karachi
    for l in a.index:
        print(l)

        if 'karachi' not in str(a.loc[l,"Name"]).lower():
            print('drop')
            a=a.drop(l)
    a=a.reset_index(drop=True)
    
    ## Removing results that are not present in that location and have no image
    for m in a.index:
        print(m)

        if str(lo) not in str(a.loc[m,"description"]).lower() and str(a.loc[m,"image"]).lower() == 'nan' :
            print('drop')
            a=a.drop(m)
    a=a.reset_index(drop=True)

    ## further random cleaning
    for n in a.index:
        print(n)

        if 'ڪراچي' in str(a.loc[n,"Name"]).lower():
            print('drop')
            a=a.drop(n)
    a=a.reset_index(drop=True)

    ## Removing results that dont have any description and image
    for o in a.index:
        print(o)

        if str(a.loc[o,"image"])== 'nan':
            print('drop')
            a=a.drop(o)
    a=a.reset_index(drop=True)

    return(a)

