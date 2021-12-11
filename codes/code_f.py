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


CLIENT_ID_4s = 'RGW4SIWSLHM1ARZ04AKEVOSTH2451TPTLUZPTNRV5P541QCY' # your Foursquare ID
CLIENT_SECRET_4s = '4ASACGFVZ03ESPLD1J4NLHNU0EAXYP14DWQCGZ40VZTX2FJ4' # your Foursquare Secret
ACCESS_TOKEN_4s = '4SPR3UKNVX5VULYGSH1Y4I2LV35I5YKFCR105GJT1KTXSSWI' # your FourSquare Access Token
VERSION_4s = '20180604'
LIMIT_4s = 30
radius_4s = 1000


def search_4s(food,locat,cit):
    
    search_item = food + ' ' + locat + ' ' + cit 
    print(search_item)

    #For Foursquare


    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    location = locat +' '+ cit

    # entering the location name
    getLoc = loc.geocode(location)

    # printing address
    print(getLoc.address)

    # printing latitude and longitude
    print("Latitude = ", getLoc.latitude, "\n")
    print("Longitude = ", getLoc.longitude)
    latitude = getLoc.latitude
    longitude = getLoc.longitude
    print(latitude, longitude)

    # search_item = 'burger'
    search_item = food
    url_4s= 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&oauth_token={}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID_4s, CLIENT_SECRET_4s, latitude, longitude,ACCESS_TOKEN_4s, VERSION_4s, search_item, radius_4s, LIMIT_4s)

    result_4s = requests.get(url_4s).json()
    print(result_4s)

    dmf=result_4s['response']['venues']



    l=[]
    for i in range(len(dmf)):
        l.append(dmf[i]['id'])
    l

    # Seraching each venue now


    df_f=pd.DataFrame(columns=['Name','Contact','address','url','ratings','comments','image'])

    for i in l:
        venue_id_4s = i
        url='https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&oauth_token={}&v={}'.format(venue_id_4s, CLIENT_ID_4s, CLIENT_SECRET_4s,ACCESS_TOKEN_4s, VERSION_4s)
        print(url)
        
        result1 = requests.get(url).json()
        print(result1['response']['venue'].keys())
        

        a=result1['response']['venue']
        print(a)
        

        name_4s=a['name']
        try:
            c=a['contact']['phone']
        except:
            c= 'Nan'
        try:
            d=a['location']['address']
        except:
            d ='Nan'
        try:
            u =a['url']
        except:
            u = 'Nan'
        try:
            rat=a['rating']
        except:
            rat = 0
        try:
            com =a['tips']['groups'][1]['items'][0]['text']
        except:
            com = 'Nan'
        
        try:
            im=a['photos']['groups'][0]['items'][0]
            image=im['prefix']+str(im['width'])+'x'+str(im['height'])+im['suffix']
        except:
            image= 'Nan'

        df_f=df_f.append({'Name':name_4s,'Contact':c,'address':d,'url':u,'ratings':rat,'comments':com,'image':image}, ignore_index=True)


        
    test=df_f
    for index in test.index:
        print(index)
        print(test.loc[index,"ratings"])
        print(test.loc[index,"comments"])
        if test.loc[index,"ratings"] == 0 and test.loc[index,"comments"]== 'Nan':
            print('drop')
            test=test.drop(index)
            
    test_sorted = test.sort_values(['ratings'], ascending=[False])
    test_sorted=test_sorted.reset_index(drop=True)
    df_4s=test_sorted 

    ## Removing results that dont have any description and image
    for j in df_4s.index:
        print(j)

        if str(df_4s.loc[j,"image"])== 'nan':
            print('drop')
            df_4s=df_4s.drop(j)
    df_4s=df_4s.reset_index(drop=True)


    return(df_4s)    
    
