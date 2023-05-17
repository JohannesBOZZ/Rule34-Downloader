import requests # request img from web
import shutil # save img locally
import os # just for the file extension in line 24
from rule34Py import rule34Py
import customtkinter 
import tkinter
from datetime import datetime
# Default theme for CustomTKinter
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('900x420')
root.title("Rule34 Downloader")
root.resizable(False,False)

def GUI():
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
    print(count, pageID, prompt)
            
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
            download(result.video, str(result.id) + file_extension)# for videos download   
    # message after process is done
    now = datetime.now()
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",'[' + str(now.strftime("%Y/%m/%d, %H:%M:%S")) + '] Download was sucessfully\n')
    status_textbox.configure(state="disabled")

# GUI Styling
frame = customtkinter.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)
label = customtkinter.CTkLabel(master=frame,
                               text='Rule34 Downloader',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
# nput how many images you wont
count_entry = customtkinter.CTkEntry(master=frame, 
                                placeholder_text='Count',
                                font=('sora', 16),
                                width=100,
                                height=24,
                                corner_radius=5)
count_entry.place(relx=0.12, rely=0.3, anchor=tkinter.CENTER)
# input on which page you want so download (First image to be downloadet = pageID * count)
page_id_entry = customtkinter.CTkEntry(master=frame, 
                                placeholder_text='Page',
                                font=('sora', 16),
                                width=60,
                                height=24,
                                corner_radius=5)
page_id_entry.place(relx=0.2535, rely=0.3, anchor=tkinter.CENTER)
# input for rule34 search 
prompt_entry = customtkinter.CTkEntry(master=frame, 
                                    placeholder_text='Prompt',
                                    font=('sora', 16),
                                    width=260,
                                    height=24,
                                    corner_radius=5)
prompt_entry.place(relx=0.482, rely=0.3, anchor=tkinter.CENTER)
# if you wont videos(when activated images and Videos)
chackbox_videos = customtkinter.CTkCheckBox(master=frame, 
                                            text='Videos',
                                            height=24,
                                            corner_radius=5)
chackbox_videos.place(relx=0.72, rely=0.3, anchor=tkinter.CENTER)
# button to start download process
button = customtkinter.CTkButton(master=frame,
                                    height=32,
                                    corner_radius=5,
                                    text='Download', 
                                    command=GUI)
button.place(relx=0.858, rely=0.3, anchor=tkinter.CENTER)
# textbox whith exit message
status_textbox = customtkinter.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=750,
                                        height=200,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    
root.mainloop()
