import os
import time
import random
import img2pdf
import pathlib
import requests
import fake_useragent

from pathlib import Path
from proxy import proxies_auth

SCRIPT_DIRECTORY_PATH = pathlib.Path.cwd()
IMAGES_FILE_DIRECTORY = Path(SCRIPT_DIRECTORY_PATH, "Images")
RESULT_FILE_DIRECTORY = Path(SCRIPT_DIRECTORY_PATH, "Result")


URL = 'https://catalog-n.com/images/pitstop12/pitstop-8-2023'
USER = fake_useragent.UserAgent().random
HEADER = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'User_agent': USER}

def get_data() -> int:
    '''Get data from webpages and count them
    
    Returns:
        last_page (int): last page of magazine/jornal
        
    '''
    item = 1
    while True:
        if item < 10:
            url = URL + f"-0{item}.jpg"
        else:
            url = URL + f"-{item}.jpg"
               
        try:
            response = requests.get(url=url, headers=HEADER, proxies=proxies_auth)
            response.raise_for_status()
            download_images(response.content, item)
            item +=1
            time.sleep(random.randrange(2,4))
        except Exception:
            break
    last_page = item-1
    print(f'last page is {last_page}')
    return last_page
   
def download_images(response: bytes, item: int) -> None:
    '''Download images (pages) from website to local directory
    
    Parameters: 
        response (bytes): content of response
        item (int): page counter   
    
    '''
    with open(f'{IMAGES_FILE_DIRECTORY}/{item}.jpg', 'wb') as file:
            file.write(response)
            print(f"Downloaded image №{item}")

def img_list() -> list:
    '''Create sorted by name list of pages(images)
    
    Returns:
        image_list (list): sorted list of pages(images)
        
    '''
    image_list = []
    sorted_files = sorted(os.listdir(IMAGES_FILE_DIRECTORY), key=get_number)
    for filename in sorted_files:
        if filename.endswith(".jpg"):
            with open(os.path.join(IMAGES_FILE_DIRECTORY, filename), 'rb') as file:
                image_list.append(file.read())
    return image_list

def get_number(filename: list) -> int:
    '''Split the file name into number part and format to sort files by names
    
    Parameters: 
        filename (list): files from local directory
        
    Returns:
        number_filename_part (int): the numeric part of the filename
    
    '''
    num_filename_part = int(filename.split('.')[0])
    return num_filename_part
    
def create_pdf_magazine(images_list: list, last_page: int) -> None:
    '''Create .pdf file where 1 page .pdf = 1 page of wev-magaxine/journal
    
    Parameters: 
       images_list (list): sorted list of pages(images)
       last_page (int): last page of magazine/jornal
    
    '''
    with open (f"{RESULT_FILE_DIRECTORY}/Magazine.pdf", 'wb') as pdf_file:
        pdf_file.write(img2pdf.convert(images_list))
    print(f'The magazine successfully created. It consist of {last_page} page(s)!')
    
def main():
    last_page = get_data()
    images_list = img_list()
    create_pdf_magazine(images_list, last_page)

    
if __name__=="__main__":
    main()