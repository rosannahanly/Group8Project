from sqlalchemy import create_engine
from six.moves.urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize
import time

def get_data():
    """Get weather data from openweathermap"""
    #send a query to the API and decode the bytes it returns
    query = urlopen("http://api.openweathermap.org/data/2.5/forecast?id=7778677&units=metric&APPID=6986e64d5d176d1782825a12f2677fe4").read().decode('utf-8')
    #return the obtained string as a dictionary
    data = json.loads(query)
    df = pd.DataFrame.from_dict(json_normalize(data['list'][0]['weather']), orient='columns')
    for i in range(1,39):
        df1 = pd.DataFrame.from_dict(json_normalize(data['list'][i]['weather']), orient='columns')
        df = df.append(df1, ignore_index=True)
    #df = pd.DataFrame(data['list']['dt_txt'])
    df2 = pd.DataFrame.from_dict(json_normalize(data['list']), orient='columns')
    dataframe = pd.concat([df, df2], axis=1)
    return dataframe[['dt_txt','main']]

def save_data_to_db(dataframe):
    #Assigning the engine variable values
    engine = create_engine("mysql+pymysql://Group8:COMP30670@dublinbikes-rse.c3hjycqhuxxq.eu-west-1.rds.amazonaws.com:3306/DublinBikes")
    #Creating the connection with the database
    conn = engine.connect()
    #passing into scrapper functions
    #Replaces the real time info in the RealTime table in the Amazon RDS database every 2 mins
    dataframe.to_sql(name='WeatherPredictor',con=conn, if_exists='replace', index=False)
    conn.close()


while True:
    data = get_data()
    save_data_to_db(data)
    time.sleep(24*60*60)