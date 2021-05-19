import configparser as envParser
import requests as req
import pandas as pd

#Init config
envParser = envParser.ConfigParser()
envParser.read('.env')

#Find the value of a defined Key
def env(key_name:str,section_name='MAIN'):
    return envParser.get(section_name,key_name,fallback=False)


#Send a slack message using a webhook URL
def send_message_to_slack(message:str):
    url = env('webhook_url',section_name='SLACK')
    params = {
        "text":message,
        "channel":env('channel',section_name='SLACK')   
    }

    response = req.post(url=url,json=params)
    
    if response.status_code != 200:
        return False
    return True

def get_one_quote_and_mark_it_as_selected():
    csv = pd.read_csv('quotes.csv')
    
    randomly_selected_row = csv[csv['selected'] == 0].sample()
    
    #mark quote as selected
    csv.loc[randomly_selected_row.index,'selected'] = 1
    csv.to_csv('quotes.csv',index=False)

    return randomly_selected_row['quote'].item()

message = get_one_quote_and_mark_it_as_selected()

if message:
    send_message_to_slack(str(message))
