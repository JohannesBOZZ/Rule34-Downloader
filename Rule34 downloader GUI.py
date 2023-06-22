import requests # request img from web
import shutil # save img locally
import os # just for the file extension in line 24
import customtkinter as ctk
import tkinter
import time
from rule34Py import rule34Py
from pathlib import Path
from datetime import datetime
# Default theme for CustomTKinter
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('900x420')
root.title("Rule34 Downloader")
root.resizable(False,False)

global file_count
# gets the download path
downloads_path = str(Path.home() / "Downloads")
print(f'Download path: {downloads_path}')
# Change the current working directory to the new output folder
os.chdir(downloads_path)
status = 'an error occurred'
def GUI():
    # starts counting time
    start_time = time.time()
    file_count = 0
    # converts count entry to int and sets default value to 1
    if count_entry.get() != '':
        count = int(count_entry.get())
    else:
        count = 1
    # gets prompt
    prompt = prompt_entry.get()
    # converts page_id entry to int and sets default value to 0
    if page_id_entry.get() != '':
        pageID = int(page_id_entry.get())
    else:
        pageID = 0
    # adding a '-video' to prompt  if checkbox isen't checkt
    if chackbox_videos.get()==0:
        prompt += ' -video'
    # adding a ' -ai_generated' to prompt  if checkbox isen't checkt
    if chackbox_ai.get() == 0:
        prompt += ' -ai_generated'
    print(count, pageID, prompt)
    if not os.path.exists(downloads_path + "\\" + prompt):
        os.makedirs(downloads_path + "\\" + prompt)
    
            
    r34Py = rule34Py()
    search = r34Py.search([prompt], page_id=pageID,  limit=count)
    

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
            try:
                src = os.getcwd() + "\\" + file_name   
                # path where the image should be moved to
                dst = downloads_path + "\\" + prompt
                if result.image:
                    shutil.move(src, dst)# for images
                else:
                    shutil.move(src, dst)# for videos       + '/' + file_name + '.mp4'
                global status
                status = f'Download was sucessfully. downloaded {file_count + 1} files'
            except:
                #removes file when already downloaded
                os.remove(downloads_path + '/' + file_name)
                status = 'File already exists'

        else:
            print('Image Couldn\'t be retrieved')
    for result in search:
        filename, file_extension = os.path.splitext(result.image)
        # call function to start downloading
        if result.image:
            download(result.image, str(result.id) + file_extension)# for images download
        else:
            download(result.video, str(result.id) + '.mp4')# for videos download   
        file_count += 1
        

    # ends counting time
    end_time = time.time()
    # calculates the time taken
    execution_time = end_time - start_time
    # converts the time in min and sec or only sec
    if execution_time >= 60:
        execution_time = execution_time /60
        minutes = int(execution_time)
        seconds = float((execution_time - minutes) * 60)
        process_time = f' in {minutes}min {round(seconds, 1)}s'
    else:
        process_time = f' in {round(execution_time, 1)}s'
    # real time
    now = datetime.now()
    # message after process is done
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] {status} {process_time}\n')
    status_textbox.configure(state="disabled")



# GUI Styling
frame = ctk.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)

label = ctk.CTkLabel(master=frame,
                               text='Rule34 Downloader',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
# input how many images you wont
count_entry = ctk.CTkEntry(master=frame, 
                                placeholder_text='Count',
                                font=('sora', 16),
                                width=65,
                                height=24,
                                corner_radius=5)
count_entry.place(relx=0.1, rely=0.3, anchor=tkinter.CENTER)
# input on which page you want so download (First image to be downloadet = pageID * count)
page_id_entry = ctk.CTkEntry(master=frame, 
                                placeholder_text='Page',
                                font=('sora', 16),
                                width=60,
                                height=24,
                                corner_radius=5)
page_id_entry.place(relx=0.2035, rely=0.3, anchor=tkinter.CENTER)
# input for rule34 search 
prompt_entry = ctk.CTkEntry(master=frame, 
                                    placeholder_text='Prompt',
                                    font=('sora', 16),
                                    width=260,
                                    height=24,
                                    corner_radius=5)
prompt_entry.place(relx=0.422, rely=0.3, anchor=tkinter.CENTER)
# if you wont videos(when activated images and Videos)
chackbox_videos = ctk.CTkCheckBox(master=frame, 
                                            text='Videos',
                                            height=24,
                                            corner_radius=5)
chackbox_videos.place(relx=0.66, rely=0.3, anchor=tkinter.CENTER)
# if you wont AI generated images
chackbox_ai = ctk.CTkCheckBox(master=frame, 
                                            text='AI',
                                            height=24,
                                            corner_radius=5)
chackbox_ai.place(relx=0.762, rely=0.3, anchor=tkinter.CENTER)
# button to start download process
button = ctk.CTkButton(master=frame,
                                    height=32,
                                    corner_radius=5,
                                    text='Download', 
                                    command=GUI)
button.place(relx=0.858, rely=0.3, anchor=tkinter.CENTER)
# textbox whith exit message
status_textbox = ctk.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=750,
                                        height=200,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

root.mainloop()
