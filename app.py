import configparser as envParser
import requests as req

#init config
envParser = envParser.ConfigParser()
envParser.read('.env')

#Find the value of a defined Key
def env(key_name:str,section_name='MAIN'):
    return envParser.get(section_name,key_name,fallback=False)


#Send slack message using slack app webhook URLs
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

send_message_to_slack('hello world of py')
