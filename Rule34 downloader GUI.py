import requests # request img from web
import shutil # save img locally
import os # just for the file extension in line 24
import customtkinter as ctk
import tkinter
import math
import time
from rule34Py import rule34Py
from pathlib import Path
from datetime import datetime
from PIL import Image
# Default theme for CustomTKinter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

root = ctk.CTk()
root.geometry('900x563')
root.title("Rule34 Downloader")
root.resizable(False,False)

# gets the download path
downloads_path = str(Path.home() / "Downloads")
print(f'Download path: {downloads_path}')
# Change the current working directory to the new output folder
os.chdir(downloads_path)
status = 'an error occurred'
print(f'grade im: {os.getcwd()}')
def GUI():
    # starts counting time
    start_time = time.time()
    # converts count entry to int and sets default value to 1
    if count_entry.get() != '':
        count = int(count_entry.get())
    else:
        count = 1
    # gets prompt
    prompt = prompt_entry.get()
    # adding a '-video' to prompt  if checkbox isen't checkt
    if chackbox_videos.get()==0:
        prompt += ' -video'
    # adding a ' -ai_generated' to prompt  if checkbox isen't checkt
    if chackbox_ai.get() == 0:
        prompt += ' -ai_generated'
    print(count, prompt)

    if dstination.get() != '':
        path_name = dstination.get()
    else:
        path_name = downloads_path
    if  new_dst_folder.get() != '':
        folder_name = '\\' + new_dst_folder.get()
        if not os.path.exists(path_name + "\\" + folder_name):
            os.makedirs(path_name + "\\" + folder_name)
    else:
        folder_name = '\\' + prompt
        if not os.path.exists(path_name + "\\" + prompt):
            os.makedirs(path_name + "\\" + prompt)
    
            
    r34Py = rule34Py()
    # locks if count is over 1000  
    try:
        if count <= 1000:
            search = r34Py.search([prompt], limit=count)
        else:
            Limit = count
            search = []
            page = 0
            for x in range(math.ceil(Limit/1000)):
                if Limit >= 1000:
                    search += r34Py.search([prompt], page_id=page, limit=1000)
                    Limit -= 1000
                    page += 1
                    print(len(search), 'elemente')
                else:
                    page = int(count / Limit -1)
                    search += r34Py.search([prompt], page_id=page, limit=Limit)
        print(len(search), ' elemente found')
        now = datetime.now()
        status_textbox.configure(state="normal")
        status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] Found {len(search)} Posts\n')
        status_textbox.configure(state="disabled")
    except Exception as e:
        now = datetime.now()
        status_textbox.configure(state="normal")
        status_textbox.insert("0.0",f'[{str(now.strftime("%Y/%m/%d, %H:%M:%S"))}] Found only {len(search)} Posts\n')
        status_textbox.configure(state="disabled")


    def download(url, file_name, file_count, result):
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
                src = downloads_path + "\\" + file_name
                # path where the image should be moved to
                new_path =  path_name + folder_name
                dst = new_path + "\\" + file_name
                mode = f'{option_menu_from.get()} {option_menu_convert.get()}'
                if mode == 'all JPG':
                    convert_to_jpg(src, new_path, int(jpg_quality.get()), ("png", "jpg", "jpeg"), str(result.id), dst, file_count)
                elif mode == 'all PNG':
                    convert_to_png(src, new_path, ("png", "jpg", "jpeg"), str(result.id), dst, file_count)
                elif mode == 'PNG JPG':
                    convert_to_jpg(src, new_path, int(jpg_quality.get()), ("png"), str(result.id), dst, file_count)
                elif mode == 'JPG PNG':
                    convert_to_png(src, new_path, ("jpg", "jpeg"), file_name, str(result.id), dst, file_count)
                elif mode == 'JPG JPG':
                    convert_to_jpg(src, new_path, int(jpg_quality.get()), ("jpg", "jpeg"), str(result.id), dst, file_count)
                elif mode == 'PNG PNG':
                    convert_to_png(src, new_path, ("png"), file_name, str(result.id), dst, file_count)
                else:
                    shutil.move(src, dst)
                    progress_bar_def(file_count)


                
                global status
                status = f'sucessfully downloaded {file_count} files'
            except Exception as e:
                #removes file when already downloaded
                status = e

        else:
            print('Image Couldn\'t be retrieved')
    file_count = 0


    for result in search:
        filename, file_extension = os.path.splitext(result.image)
        file_count += 1
        
        download_successful = False
        
        while not download_successful:
            try:
                if result.image:
                    download(result.image, str(result.id) + file_extension, file_count, result)  # For image download
                else:
                    download(result.video, str(result.id) + '.mp4', file_count, result)  # For video download         
                download_successful = True
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Waiting for 10 seconds before retrying...")
                for x in range(10):
                    progress_bar.update()
                    print(f'{x+1} seconds')
                    time.sleep(1)
    

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

def convert_to_jpg(input_file, output_file, quality: int, extensions, file_name, dst, file_count):
    print('quality is ', quality)
    if quality == 0:
        raise Exception('please enter a quality')
    wb = chackbox_wb.get()

    if input_file.endswith(extensions):
                output_path = output_file + '\\' + file_name + ".jpg"
            # Checks whether checkbox wb is selected or not
                img=None
                if wb:
                    img = Image.open(input_file).convert('L')
                else:
                    img = Image.open(input_file).convert("RGB")
                img.save(output_path, "JPEG", quality=quality)
                os.remove(input_file)
                progress_bar_def(file_count)
    else:
                shutil.move(input_file, dst)
                progress_bar_def(file_count)



def convert_to_png(input_file, output_file, extensions, file_name, dst, file_count):
    wb = chackbox_wb.get()

    if input_file.endswith(extensions):
                output_path = output_file + '\\' + file_name + ".png"
                img=None
                if wb:
                    img = Image.open(input_file).convert('L')
                else:
                    img = Image.open(input_file)
                img.save(output_path, 'PNG')
                os.remove(input_file)
                progress_bar_def(file_count)
    else: 
                shutil.move(input_file, dst)
                progress_bar_def(file_count)


def mode(self):
    mode = f'{option_menu_from.get()} {option_menu_convert.get()}'
    # shows jpg_quality and chackbox_wb
    if 'JPG' in option_menu_convert.get():
        jpg_quality.place(relx=0.6, rely=0.4, anchor=tkinter.W)
        chackbox_wb.place(relx=0.8, rely=0.4, anchor=tkinter.W)
    # shows chackbox_wb and hidersjpg_quality
    elif 'PNG' in option_menu_convert.get():
        chackbox_wb.place(relx=0.6, rely=0.4, anchor=tkinter.W)
        jpg_quality.place_forget()
    # hides jpg_quality and chackbox_wb
    elif option_menu_convert.get() == 'None':
        chackbox_wb.place_forget()
        jpg_quality.place_forget()


def progress_bar_def(test):
    Value = int(test) / int(count_entry.get())
    progress_bar_text.configure(text=f'{round(Value * 100)} %')
    progress_bar_text.update()
    progress_bar.set(Value)
    progress_bar.update()


# GUI Styling
frame = ctk.CTkFrame(master=root, fg_color='transparent')
frame.pack(pady=16, padx=24, fill='both', expand=True)

label = ctk.CTkLabel(master=frame,
                               text='Rule34 Downloader',
                               font=("sora", 32))
label.place(relx=0.5, rely=0.06, anchor=tkinter.CENTER)
# input how many images you wont
count_entry = ctk.CTkEntry(master=frame, 
                                placeholder_text='Count',
                                font=('sora', 16),
                                width=90,
                                height=24,
                                corner_radius=5)
count_entry.place(relx=0.02, rely=0.2, anchor=tkinter.W)
# input on which page you want so download (First image to be downloadet = pageID * count)
# input for rule34 search 
prompt_entry = ctk.CTkEntry(master=frame, 
                                    placeholder_text='Prompt',
                                    font=('sora', 16),
                                    width=380,
                                    height=24,
                                    corner_radius=5)
prompt_entry.place(relx=0.15, rely=0.2, anchor=tkinter.W)
# if you wont videos(when activated images and Videos)
chackbox_videos = ctk.CTkCheckBox(master=frame, 
                                            text='Videos',
                                            height=24,
                                            corner_radius=5)
chackbox_videos.place(relx=0.63, rely=0.2, anchor=tkinter.W)
# if you wont AI generated images
chackbox_ai = ctk.CTkCheckBox(master=frame, 
                                            text='AI',
                                            height=24,
                                            corner_radius=5)
chackbox_ai.place(relx=0.74, rely=0.2, anchor=tkinter.W)
# button to start download process
dstination = ctk.CTkEntry(master=frame,
                            placeholder_text='Output folder (default is Downloads)',
                            font=("sora", 16),
                            width=490,
                            height=24,
                            corner_radius=5)
dstination.place(relx=0.02, rely=0.3, anchor=tkinter.W)

new_dst_folder = ctk.CTkEntry(master=frame,
                            placeholder_text='New folder name (optional)',
                            font=("sora", 16),
                            width=310,
                            height=24,
                            corner_radius=5)
new_dst_folder.place(relx=0.98, rely=0.3, anchor=tkinter.E)
# entry for quality by jpg
jpg_quality = ctk.CTkEntry(master=frame,
                            placeholder_text='JPG Quality',
                            font=("sora", 16),
                            width=150,
                            height=24,
                            corner_radius=5)

convert_only_from_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='Convert only from',
                                bg_color='transparent')
convert_only_from_lable.place(relx=0.02, rely=0.4, anchor=tkinter.W)
# menu for changing the sort mode
option_menu_from = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 16),
                                width=120,
                                height=24,
                                corner_radius=5,
                                values=['all', 'PNG', 'JPG'],
                                command=mode,)
option_menu_from.place(relx=0.22, rely=0.4, anchor=tkinter.W)

to_lable = ctk.CTkLabel(master=frame,
                                font=('sora', 16),
                                text='to',
                                bg_color='transparent')
to_lable.place(relx=0.385, rely=0.4, anchor=tkinter.W)
# menu for changing the convert mode
option_menu_convert = ctk.CTkOptionMenu(master=frame,
                                font=('sora', 16),
                                width=120,
                                height=24,
                                corner_radius=5,
                                values=['None', 'JPG', 'PNG'],
                                command=mode,)
option_menu_convert.place(relx=0.43, rely=0.4, anchor=tkinter.W)
# if you wont AI generated images
chackbox_wb = ctk.CTkCheckBox(master=frame, 
                                font=('sora', 16),
                                text='White & Black',
                                height=24,
                                corner_radius=5)

button = ctk.CTkButton(master=frame,
                                    height=32,
                                    corner_radius=5,
                                    text='Download', 
                                    command=GUI)
button.place(relx=0.98, rely=0.2, anchor=tkinter.E)
# textbox whith exit message
status_textbox = ctk.CTkTextbox(master=frame,
                                        font=('sora', 16),
                                        width=824,
                                        height=230,
                                        bg_color='#242424',
                                        corner_radius=5)
status_textbox.place(relx=0.5, rely=0.695, anchor=tkinter.CENTER)
status_textbox.configure(state="disabled")

progress_bar = ctk.CTkProgressBar(master=frame,
                                width=780,
                                mode='determinate',)
progress_bar.place(relx=0.02, rely=0.97, anchor=tkinter.W)
progress_bar.set(0)

progress_bar_text = ctk.CTkLabel(master=frame,
                                text='0%',
                                bg_color='transparent')
progress_bar_text.place(relx=0.95, rely=0.97, anchor=tkinter.W)


root.mainloop()
