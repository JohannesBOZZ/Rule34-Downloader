import requests # request img from web
import shutil # save img locally
import os # just for the file extension in line 24
from rule34Py import rule34Py
import customtkinter 
import tkinter
from datetime import datetime

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('900x420')
root.title("Rule34 Downloader")
root.resizable(False,False)

def GUI():
    if count_entry.get() != '':
        count = int(count_entry.get())
    else:
        count = 1

    promt = promt_entry.get()

    if page_id_entry.get() != '':
        pageID = int(page_id_entry.get())
    else:
        pageID = 0
    if chackbox_videos.get()==0:
        promt += ' -video'
    print(count, pageID, promt)
            
    r34Py = rule34Py()
    search = r34Py.search([promt],  limit=count)#das in der liste wird auf rule34.xxx gesucht, das limeit geht nicht über 1000
    

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
            #phat wo die Datein rauskommen in meinen fall "C:/Users/JohannesBOZZ"
            src = "C:/Users/JohannesBOZZ/AppData/Local/Programs/Python/Python310/.Programme/" + file_name
            #ühat wo die Dateien hin sollen
            dst = "D:/Bilder/temp"
            if result.image:
                shutil.move(src, dst)#für bilder

            else:
                shutil.move(src, dst + '/' + file_name + '.mp4')#für videos
        else:
            print('Image Couldn\'t be retrieved')
    for result in search:
        filename, file_extension = os.path.splitext(result.image)
        # call function to start downloading
        if result.image:
            download(result.image, str(result.id) + file_extension)#für bild download
        else:
            download(result.video, str(result.id) + file_extension)#für video download   

    now = datetime.now()
    status_textbox.configure(state="normal")
    status_textbox.insert("0.0",'[' + str(now.strftime("%Y/%m/%d, %H:%M:%S")) + '] Download was sucessfully\n')
    status_textbox.configure(state="disabled")

#Styling der GUI
frame = customtkinter.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)
label = customtkinter.CTkLabel(master=frame,
                               text='Rule34 Downloader',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
#eingabe wie viele bilder man will
count_entry = customtkinter.CTkEntry(master=frame, 
                                placeholder_text='Count',
                                font=('sora', 16),
                                width=100,
                                height=24,
                                corner_radius=5)
count_entry.place(relx=0.12, rely=0.3, anchor=tkinter.CENTER)

page_id_entry = customtkinter.CTkEntry(master=frame, 
                                placeholder_text='Page',
                                font=('sora', 16),
                                width=60,
                                height=24,
                                corner_radius=5)
page_id_entry.place(relx=0.2535, rely=0.3, anchor=tkinter.CENTER)
#eingabe welche eigenschaften die bilder haben sollen
promt_entry = customtkinter.CTkEntry(master=frame, 
                                    placeholder_text='Promt',
                                    font=('sora', 16),
                                    width=260,
                                    height=24,
                                    corner_radius=5)
promt_entry.place(relx=0.482, rely=0.3, anchor=tkinter.CENTER)
#ob man videos dabei haben will
chackbox_videos = customtkinter.CTkCheckBox(master=frame, 
                                            text='Videos',
                                            height=24,
                                            corner_radius=5)
chackbox_videos.place(relx=0.72, rely=0.3, anchor=tkinter.CENTER)
#button um den download vorgang zu starten
button = customtkinter.CTkButton(master=frame,
                                    height=32,
                                    corner_radius=5,
                                    text='Download', 
                                    command=GUI)
button.place(relx=0.858, rely=0.3, anchor=tkinter.CENTER)
#textbox wo reingschrieben wird wen der procces fertig ist
status_textbox = customtkinter.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=750,
                                        height=200,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    
root.mainloop()
