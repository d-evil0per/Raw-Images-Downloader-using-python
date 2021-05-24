we need to request the endpoint with the payload and store the response in a variable and after that, we will extract the links and save them in an excel sheet. But first, let's import the libraries required for this task.

```python
from typing import Union
import JSON
import pandas as pd 
import requests
import urllib
import os 
from fake_useragent import UserAgent
from requests.exceptions import HTTPError
```
It looks scary but let me break down what is the usage of these many libraries in this program.
-  [from typing import Union](https://docs.python.org/3/library/typing.html)  - this is used for type-hinting and in our case, we are using union to tell the function that it can return either HTTERROR or a dictionary type data. you will understand its usage when we use it later in the code.
-  [import json](https://docs.python.org/3/library/json.html) - to store and exchange data in JSON format
-  [import pandas as pd ](https://pandas.pydata.org/docs/getting_started/index.html) - to create a  [data frame](https://www.geeksforgeeks.org/python-pandas-dataframe/#:~:text=Pandas%20DataFrame%20is%20two%2Ddimensional,fashion%20in%20rows%20and%20columns.)  and save the [data frame](https://www.geeksforgeeks.org/python-pandas-dataframe/#:~:text=Pandas%20DataFrame%20is%20two%2Ddimensional,fashion%20in%20rows%20and%20columns.) into the excel sheet.
-  [import requests](https://realpython.com/python-requests/) - to send the get request with the payload to get the response from the server.
- [import urllib](https://docs.python.org/3/library/urllib.html)  - we have used the `urllib.parse.urlencode` module to format the URL / endpoint in a proper format.
-   [import os ](https://docs.python.org/3/library/os.html) - for using operating system dependent functionality like creating folders and files 

-  [from fake_useragent import UserAgent](https://pypi.org/project/fake-useragent/) - grabs up-to-date useragent which will use be used in the header of the request.
-  [from requests.exceptions import HTTPError](https://docs.python-requests.org/en/master/_modules/requests/exceptions/)  - to catch the httperrror while requesting to the server.

Now let's create a function that will handle the calling of the request and sending back the response in the JSON format.

```python
def call_request(url) -> Union[HTTPError, dict]:
    user_agent = UserAgent()
    headers = headers={'User-Agent': str(user_agent)}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e

    return response.json()
```
- In the above code, we created a function called `call_request` which takes URL as an input and returns either HTTPError or a dictionary as a response.
- inside the `call_request` function we are requesting the URL with the header and if it throws an error we are returning the error else returning the response in JSON.

Let's call the function with the URL and extract the images from the response. So, for the payload let's search for 10 images of `food photography` and save the links along with the keyword name in an excel sheet.

```python
if __name__== "__main__":
    genre="food photography"
    per_page=10
    page=1
    parameter={"query":genre,"per_page":per_page,"page":page}
    query= urllib.parse.urlencode(parameter)
    url=f"https://unsplash.com/napi/search/photos?{query}"
    response=call_request(url)
    image_list=[]
    if len(response['results'])>0:
        for i in range(len(response['results'])):
            temp={ "Genre":genre, "link":response['results'][i]['urls']['raw']}
            image_list.append(temp)


    xls_data = pd.DataFrame(image_list)
    xls_data.to_excel("image_list.xlsx", engine='xlsxwriter', index=False)
```
- In the above script we have declared some variables `genre`, `per_page`, `page` to store the basic details of the payload that we are going to use in the request. it is totally optional you can also put these in the payload itself.
- creating a dictionary for the payload so that we can encode it into the proper format using the `urllib.parse.urlencode` module.
- creating the endpoint with the base URL and the payload.
- then we sent the request and checked if the request contains a results element with a size greater than zero.
- if it's greater than zero then we created the dictionary to add each link with a keyword into the list.
- Once the list is created we have converted that list into [data frame](https://www.geeksforgeeks.org/python-pandas-dataframe/#:~:text=Pandas%20DataFrame%20is%20two%2Ddimensional,fashion%20in%20rows%20and%20columns.)
- with the help of [import pandas as pd ](https://pandas.pydata.org/docs/getting_started/index.html) we save the data frame to excel.

Once it gets saved into the excel sheet it will look something like this:


![excel.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1621878997848/jeXyqGaKv.png)

Now the question arises this article was about downloading the images, So where are my images? I want it in my drive I don't want any links. Well, have some patience we have just started. 

Let's now talk about how do we save it or download it from those links.

## Downloading the images from the links

To download those images, we need to add few lines of codes here and there in our main block. 

```python
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
    
```

It's the same as the previous code but in extra it will download and save the images in our local file system. let's discuss those lines of code

```python
image_folder_path= os.getcwd()+"\images"
if not os.path.isdir(image_folder_path):
        os.mkdir(image_folder_path)

```
- we created a directory called `images` under the current working directory. if the directory was not there at first to save all the images inside it. 

```python
filename = response['results'][i]['urls']['raw'].split('/')[-1].split('?')[0]+".jpg"
folder_path=os.path.join(image_folder_path,genre)
if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
filepath=os.path.join(folder_path,filename)
r = requests.get(response['results'][i]['urls']['raw'], allow_redirects=True)
open(filepath.replace("\\", "/"), 'wb').write(r.content)
```
- We extracted the filename from the image URLs and created the directory according to the keyword if it is not present.
- created the absolute path of the file and request the image URL and read its content and save it in a jpg file at the absolute path.

Now if you run the script it will create the directory with keyword name and store all the images inside that directory. for example,


![save.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1621880005059/ECwTWZNBa.png)


## Bonus Points

- You can download images related to multiple keywords all you have to create a keyword list and call the request for each keyword in a loop.

```python
keywords=['gaming','pokemon','PUBG']
for key in keywords:
    genre =key
    per_page=10
    page=1
    ............
```
- you can extract the image based on certain conditions such as ( most liked, by the user, etc. ) just study the response and data coming in it.

- you can also download all the images till the last page.  if you check the response there is an element that gives information about total pages.

- you can get only 30 images per page even if you pass value greater than 30.





