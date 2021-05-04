import requests
from bs4 import BeautifulSoup
import urllib.request

url = 'https://www.google.com/search?q=lappuggla&tbm=isch&sxsrf=ALeKk02slt7IgK2KdgC8vp_luY1BJWMgLA%3A1620049628315&source=hp&biw=1280&bih=610&ei=3P6PYK-bEeSZlwT24rSwCw&oq=lappuggla&gs_lcp=CgNpbWcQAzIECCMQJzICCAAyAggAMgIIADICCAAyAggAMgIIADIGCAAQBRAeMgQIABAYMgQIABAYOgUIABCxAzoECAAQHlCsD1iPFmDqFmgAcAB4AIABXogB3ASSAQE5mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ved=0ahUKEwiv-fKU063wAhXkzIUKHXYxDbYQ4dUDCAc&uact=5'

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

images = soup.find_all("img", attrs={"alt": "Post image"})

number = 0

for image in images:
    image_src = image["src"]
    print(image_src)
    urllib.request.urlretrieve(image_src, str(number))
    number += 1
