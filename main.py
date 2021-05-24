from typing import Union
import json
import pandas as pd 
import requests
import urllib
import os 
from fake_useragent import UserAgent
from requests.exceptions import HTTPError




def call_request(url) -> Union[HTTPError, dict]:
    user_agent = UserAgent()
    headers = headers={'User-Agent': str(user_agent)}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e

    return response.json()

if __name__== "__main__":
    genre="food photography"
    per_page=10
    page=1
    image_folder_path= os.getcwd()+"\images"
    if not os.path.isdir(image_folder_path):
        os.mkdir(image_folder_path)
    parameter={"query":genre,"per_page":per_page,"page":page}
    query= urllib.parse.urlencode(parameter)
    url=f"https://unsplash.com/napi/search/photos?{query}"
    response=call_request(url)
    image_list=[]
    if len(response['results'])>0:
        for i in range(len(response['results'])):
            filename = response['results'][i]['urls']['raw'].split('/')[-1].split('?')[0]+".jpg"
            folder_path=os.path.join(image_folder_path,genre)
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
            filepath=os.path.join(folder_path,filename)
            r = requests.get(response['results'][i]['urls']['raw'], allow_redirects=True)
            open(filepath.replace("\\", "/"), 'wb').write(r.content)
            temp={ "Genre":genre, "link":response['results'][i]['urls']['raw']}
            image_list.append(temp)
    
    
    xls_data = pd.DataFrame(image_list)
    xls_data.to_excel("image_list.xlsx", engine='xlsxwriter', index=False)
    
