import requests # request img from web
import shutil # save img locally
import os # just for the file extension in line 24
import math
from rule34Py import rule34Py
import time
r34Py = rule34Py()
Limit1= 10
prompt = [""]
if Limit1 <= 1000:
    search = r34Py.search(prompt, ignore_max_limit=True, limit=Limit1)# prompts in the list, max limit ist 1000 (limit from rule34.xxx) and the First image to be downloadet = pageID * count,
else:
    Limit = Limit1
    search = []
    page = 0
    print('else')
    for x in range(math.ceil(Limit/1000)):
        if Limit >= 1000:
            search += r34Py.search(prompt, page_id=page, limit=1000)# prompts in the list, max limit ist 1000 (limit from rule34.xxx) and the First image to be downloadet = pageID * count,
            Limit -= 1000
            page += 1
        else:
            page = int(Limit1 / Limit -1)
            print(f'else:{page} <------page id')

            search += r34Py.search(prompt, page_id=page, limit=Limit)# prompts in the list, max limit ist 1000 (limit from rule34.xxx) and the First image to be downloadet = pageID * count,

#print(search)
print(len(search))
def download(url, file_name):
    res = requests.get(url, stream = True)
    # rule34.xxx apis will always return a status
    # of 200 (which kinda sucks)
    if res.status_code == 200:
        # open a file to write to
        with open(file_name,'wb') as f:
            #for chunk in res.iter_content(chunk_size=8192):
             #   f.write(chunk)
            # write the raw body data of the requests
            # response to that file

            shutil.copyfileobj(res.raw, f)

        print('Image sucessfully Downloaded: ',file_name)
        # path where the image gets saved
        src = r"C:\Users\JohannesBOZZ\AppData\Local\Programs\Python\Python310\.Programme" + "\\" + file_name
        # path where the image should be moved to
        dst = r"D:\Bilder\test\test run"
        if result.image:
            shutil.move(src, dst)# for images
        else:
            shutil.move(src, dst + '/' + file_name + '.mp4')# for videos
    else:
        print('Image Couldn\'t be retrieved')


start = time.time()

for result in search:
    filename, file_extension = os.path.splitext(result.image)
    
    # call function to start downloading
    if result.image:
        download(result.image, str(result.id) + file_extension)# for images download
    else:
        download(result.video, str(result.id) + file_extension)# for video download
ende = time.time()
print(round(ende - start, 2), 'seconds')