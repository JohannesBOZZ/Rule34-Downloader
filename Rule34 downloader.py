import requests # request img from web
import shutil # save img locally
import os # just for the file extension in line 24

from rule34Py import rule34Py
r34Py = rule34Py()
search = r34Py.search([""], page_id=0, limit=1000)# prompts in the list, max limit ist 1000 (limit from rule34.xxx) and the First image to be downloadet = pageID * count,

def download(url, file_name):
    res = requests.get(url, stream = True)
    
    # rule34.xxx apis will always return a status
    # of 200 (which kinda sucks)
    if res.status_code == 200:
        
        # open a file to write to
        with open(file_name,'wb') as f:
            
            # write the raw body data of the requests
            # response to that file
            shutil.copyfileobj(res.raw, f)
            
        print('Image sucessfully Downloaded: ',file_name)
        # path where the image gets saved
        src = "C:/Users/JohannesBOZZ/AppData/Local/Programs/Python/Python310/.Programme/" + file_name
        # path where the image should be moved to
        dst = "D:/Bilder/temp"
        if result.image:
            shutil.move(src, dst)# for images
        else:
            shutil.move(src, dst + '/' + file_name + '.mp4')# for videos
    else:
        print('Image Couldn\'t be retrieved')



for result in search:
    filename, file_extension = os.path.splitext(result.image)
    
    # call function to start downloading
    if result.image:
        download(result.image, str(result.id) + file_extension)# for images download
    else:
        download(result.video, str(result.id) + file_extension)# for video download