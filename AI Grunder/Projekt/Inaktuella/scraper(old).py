import os
import requests
from bs4 import BeautifulSoup

Google_Images = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

Image_Folder = 'Google Images'


def main():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    download_images()


def download_images():
    data = input('Enter your search keywords: ')
    num_images = int(input('Enter the number of images you want: '))

    print('Searching images...')

    search_url = Google_Images + 'q=' + data

    response = requests.get(search_url, headers=u_agnt)
    html = response.text

    b_soup = BeautifulSoup(html, 'html.parser')
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    count = 0
    image_links = []
    for res in results:
        try:
            link = res['data-src']
            image_links.append(link)
            count += 1
            if count >= num_images:
                break

        except KeyError:
            continue

    print(f'Found {len(image_links)} images')
    print('Start downloading...')

    for i, image_link in enumerate(image_links):
        response = requests.get(image_link)
        image_name = Image_Folder + '/' + data + str(i+1) + '.jpg'
        with open(image_name, 'wb') as file:
            file.write(response.content)

    print('Download completed!')


if __name__ == '__main__':
    main()
