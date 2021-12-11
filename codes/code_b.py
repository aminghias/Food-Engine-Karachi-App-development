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

subscriptionKey_bing = "722b24f0a3314d509ea3378d2e9a69c1"
customConfigId_bing = "ff55cf0a-0790-4326-80b8-c7c7d882ec6e"

def search_bing(food,locat,cit):
    
    search_item = food + ' ' + locat + ' ' + cit 
    print(search_item)

    
    # For Bing search


    rg=range(0,10)
    url_bing = 'https://api.bing.microsoft.com/v7.0/custom/search?' + 'q=' + search_item + '&' + 'customconfig=' + customConfigId_bing
    r = requests.get(url_bing, headers={'Ocp-Apim-Subscription-Key': subscriptionKey_bing}).json()
    df=pd.DataFrame(columns=['Name','url','description','image'])
    print(r)
    dm = r['webPages']['value']

    for i in rg:


        n= dm[i]['name']
        url=dm[i]['url']
        try:
            d=dm[i]['snippet']
        except:
            d='NaN'
        try:
            im=dm[i]['openGraphImage']['contentUrl']
        except:
            im='NaN'
        print(i)
        df = df.append({'Name':n,
                   'url':url,'description':d,'image':im}, ignore_index=True) 
   
    df_bing=df
    
    return(df_bing)






    