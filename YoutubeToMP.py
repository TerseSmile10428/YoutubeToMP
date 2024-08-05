import os
import threading
from ctypes import *
from tkinter import *
from tkinter import filedialog, messagebox
from hPyT import *
from moviepy.editor import AudioFileClip
from pytube import YouTube

# Configuration

# Color
background_Color = "#1c1c1c"
text_Color = "#FFFFFF"
widget_Color = "#333333"
line_color = "#CCCCCC"
selected_color = "#FFFFFF"
unSelected_color = "#CCCCCC"

background_Colorblue = "#015C92"
text_Colorblue = "#FFFFFF"
widget_Colorblue = "#2D82B5"
line_colorblue = "#2D82B5"
selected_colorblue = "#FFFFFF"
unSelected_colorblue = "#CCCCCC"

background_Colorwhite = "#E7E7E7"
text_Colorwhite = "#000000"
widget_Colorwhite = "#D1D1D1"
line_colorwhite = "#333333"
selected_colorwhite = "#000000"
unSelected_colorwhite = "#333333"

background_Colorpurple = "#371F76"
text_Colorpurple = "#FFFFFF"
widget_Colorpurple = "#643B9F"
line_colorpurple = "#643B9F"
selected_Colorpurple = "#FFFFFF"
unSelected_Colorpurple = "#CCCCCC"

background_Colorred = "#B71C1C"
text_Colorred = "#FFFFFF"
widget_Colorred = "#C62828"
line_colorred = "#C62828"
selected_Colorred = "#FFFFFF"
unSelected_Colorred = "#CCCCCC"

background_colorgreen = "#3D723F"
text_colorgreen = "#FFFFFF"
widget_colorgreen = "#4A864C"
line_colorgreen = "#4A864C"
selected_colorgreen = "#FFFFFF"
unSelected_colorgreen = "#CCCCCC"

myappid = 'YoutubeToMP'
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def download_mp3(url, save_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=save_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        audio_clip = AudioFileClip(out_file)
        audio_clip.write_audiofile(new_file, codec='libmp3lame', bitrate='192k')
        audio_clip.close()
        os.remove(out_file)

        if not os.path.exists(new_file):
            raise Exception("Failed to create MP3 file.")
        return new_file
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while downloading MP3: {e}")
        return None


def download_mp4(url, save_path):
    try:
        yt = YouTube(url)
        # Filter streams to get those with resolutions of 1080p or higher
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        # Find the highest resolution that is at least 1080p
        stream = next((s for s in streams if int(s.resolution[:-1]) >= 1080), streams.first())
        out_file = stream.download(output_path=save_path)

        if not os.path.exists(out_file):
            raise Exception("Failed to create MP4 file.")
        return out_file
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while downloading MP4: {e}")
        return None


def download():
    url = youtubeLink_entry.get()
    file_type = file_type_var.get()
    save_path = save_path_var.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter the YouTube URL.")
        return
    if not save_path:
        messagebox.showwarning("Input Error", "Please select a save location.")
        return

    download_thread = threading.Thread(target=background_download, args=(url, file_type, save_path))
    download_thread.start()


def background_download(url, file_type, save_path):
    if file_type == 'mp3':
        downloaded_file = download_mp3(url, save_path)
    else:
        downloaded_file = download_mp4(url, save_path)

    if downloaded_file:
        messagebox.showinfo("Success", f"Downloaded and converted to {file_type.upper()}: \n{downloaded_file}")


def browse_save_location():
    save_path = filedialog.askdirectory()
    if save_path:
        save_path_var.set(save_path)


# Function to handle focus in for youtubeLink_entry
def on_focus_in_youtubeLink_entry(event=None):
    if youtubeLink_entry.get() == 'Paste link':
        youtubeLink_entry.delete(0, 'end')
        youtubeLink_entry.config(fg=text_Colorwhite if selected_layout.get() == "white" else text_Color)


# Function to handle focus in for locationLink_entry
def on_focus_in_locationLink_entry(event=None):
    if locationLink_entry.get() == 'Paste here':
        locationLink_entry.delete(0, 'end')
        locationLink_entry.config(fg=text_Colorwhite if selected_layout.get() == "white" else text_Color)


# Function to handle focus out for youtubeLink_entry
def on_focus_out_youtubeLink_entry(event=None):
    if youtubeLink_entry.get() == '':
        youtubeLink_entry.insert(0, 'Paste link')
    youtubeLink_entry.config(fg=text_Colorwhite if selected_layout.get() == "white" else text_Color)


# Function to handle focus out for locationLink_entry
def on_focus_out_locationLink_entry(event=None):
    if locationLink_entry.get() == '':
        locationLink_entry.insert(0, 'Paste here')
    locationLink_entry.config(fg=text_Colorwhite if selected_layout.get() == "white" else text_Color)


def toggle_radio(button):
    is_colored_layout = selected_layout.get() in ["blue", "purple", "red", "green", "gray"]

    selected_image_suffix = 'Gray' if is_colored_layout else 'White'
    unselected_image_suffix = 'Gray' if is_colored_layout else 'White'

    if button == 1:
        MP3_radioButton.config(image=globals()[f'Active{selected_image_suffix}'])
        MP4_radioButton.config(image=globals()[f'InActive{unselected_image_suffix}'])
        file_type_var.set("mp3")
    elif button == 2:
        MP3_radioButton.config(image=globals()[f'InActive{unselected_image_suffix}'])
        MP4_radioButton.config(image=globals()[f'Active{selected_image_suffix}'])
        file_type_var.set("mp4")


# Change event binding to unfocused entry fields on click
def focus_out_all_entries(event):
    widget = event.widget
    if widget not in (youtubeLink_entry, locationLink_entry):
        on_focus_out_youtubeLink_entry()
        on_focus_out_locationLink_entry()


def switch_button(button):
    layout = selected_layout.get()
    is_colored_layout = layout in ["blue", "purple", "red", "green", "gray"]

    selected_image_suffix = 'Gray' if is_colored_layout else 'White'
    unselected_image_suffix = 'Gray' if is_colored_layout else 'White'

    if button == "home":
        home_button.config(image=globals()[f'HomeButtonSelected{selected_image_suffix}'])
        settings_image_button.config(image=globals()[f'SettingsButtonUnSelected{unselected_image_suffix}'])
        show_screen("home")
    elif button == "settings":
        home_button.config(image=globals()[f'HomeButtonUnSelected{unselected_image_suffix}'])
        settings_image_button.config(image=globals()[f'SettingsButtonSelected{selected_image_suffix}'])
        show_screen("settings")


def show_screen(screen):
    if screen == "home":
        home_frame.place(x=0, y=0)
        settings_frame.place_forget()
    elif screen == "settings":
        home_frame.place_forget()
        settings_frame.place(x=0, y=0)


def show_gray_preview():
    preview_widget.configure(image=gray_preview_widget_image)
    print("Gray preview applied")


def show_blue_preview():
    preview_widget.configure(image=BluePreviewWidget)
    print("Blue preview applied")


def show_white_preview():
    preview_widget.configure(image=white_preview_widget_image)
    print("White preview applied")


def show_purple_preview():
    preview_widget.configure(image=PurplePreviewWidget)
    print("purple preview applied")


def show_red_preview():
    preview_widget.configure(image=RedPreviewWidget)
    print("purple preview applied")


def show_green_preview():
    preview_widget.configure(image=GreenPreviewWidget)
    print("green preview applied")


def apply_color(event=None):
    if selected_layout.get() == "gray":
        show_gray()
    elif selected_layout.get() == "white":
        show_white()
    elif selected_layout.get() == "blue":
        show_blue()
    elif selected_layout.get() == "purple":
        show_purple()
    elif selected_layout.get() == "red":
        show_red()
    elif selected_layout.get() == "green":
        show_green()
    # can add more conditions for other colors if needed
    print(f"Color applied: {selected_layout.get()}")


def show_gray():
    root.iconbitmap(r"Assets/TitleIcon/GrayIcon.ico")
    title_bar_color.set(root, background_Color)
    root.config(bg=background_Color)
    home_frame.config(bg=background_Color)
    frame_1_for_title.config(bg=background_Color)
    frame_2_for_title.config(bg=background_Color)
    frame_3_for_title.config(bg=background_Color)
    frame_4_for_title.config(bg=background_Color)
    title.config(bg=background_Color, image=YoutubeToVideoTitle)
    frame_1_for_link_entry_and_label.config(bg=background_Color)
    frame_2_for_link_entry_and_label.config(bg=background_Color)
    label_frame.config(bg=background_Color)
    youtubeLink_label.config(bg=background_Color, image=YoutubeLinkText)
    entry_image.config(image=YoutubeEntryGray, bg=background_Color)
    frame_for_paste_button.config(bg=widget_Color)
    youtubeLink_entry.config(bg=widget_Color, fg=text_Color)
    Paste_button.config(image=PasteButtonGray, bg=widget_Color)
    frame_for_format_label.config(bg=background_Color)
    format_label.config(bg=background_Color, image=FormatText)
    radio_buttons_frame.config(bg=background_Color)
    Widget_for_radio_button_MP3.config(image=RadioWidgetGray, bg=background_Color)
    MP3_radioButton.config(bg=widget_Color, fg=text_Color, image=ActiveGray)
    MP3_text.config(bg=widget_Color, image=SongText)
    Widget_for_radio_button_MP4.config(image=RadioWidgetGray, bg=background_Color)
    MP4_radioButton.config(bg=widget_Color, fg=text_Color, image=InActiveGray)
    MP4_text.config(bg=widget_Color, image=VideoText)
    frame_1_for_location_entry_and_label.config(bg=background_Color)
    frame_2_for_location_entry_and_label.config(bg=background_Color)
    frame_for_label_location.config(bg=background_Color)
    location_label.config(bg=background_Color, image=LocationEntryText)
    location_entry.config(bg=background_Color, fg=text_Color, image=LocationEntryGray)
    locationLink_entry.config(bg=widget_Color, fg=text_Color)
    convert_button.config(bg=background_Color, fg=text_Color, image=ConvertWidgetGray)
    browse_button.config(bg=background_Color, fg=text_Color, image=BrowseWidgetGray)
    frame1_for_screen_buttons.config(bg=background_Color)
    frame_line_for_down_buttons.config(bg=line_color)
    frame2_for_screen_buttons.config(bg=background_Color)
    home_button.config(image=HomeButtonUnSelectedGray, bg=background_Color)
    settings_image_button.config(image=SettingsButtonUnSelectedGray, bg=background_Color)
    settings_frame.config(bg=background_Color)
    frame_1_for_settings_title.config(bg=background_Color)
    frame_2_for_settings_title.config(bg=background_Color)
    frame_3_for_settings_title.config(bg=background_Color)
    frame_4_for_settings_title.config(bg=background_Color)
    settings_title.config(bg=background_Color, image=settings_title_image)
    frame_1_for_layout.config(bg=background_Color)
    frame_2_for_layout.config(bg=background_Color)
    frame_for_label_layout.config(bg=background_Color)
    layout_label.config(bg=background_Color, image=label_color_layout)
    layout_widget.config(bg=background_Color, image=layout_widget_image)
    gray_layout_button.config(bg=widget_Color)
    blue_layout_button.config(bg=widget_Color)
    white_layout_button.config(bg=widget_Color)
    purple_layout_button.config(bg=widget_Color)
    red_layout_button.config(bg=widget_Color)
    green_layout_button.config(bg=widget_Color)
    frame_1_for_preview.config(bg=background_Color)
    frame_2_for_preview.config(bg=background_Color)
    frame_for_preview_text.config(bg=background_Color)
    preview_text.config(image=preview_text_image, bg=background_Color)
    preview_widget.config(bg=background_Color)
    apply_button.config(image=apply_button_image, bg=background_Color)
    app_version_text.config(image=app_version_text_image, bg=background_Color)


def show_blue():
    root.iconbitmap(r"Assets/TitleIcon/BlueIcon.ico")
    title_bar_color.set(root, background_Colorblue)
    root.config(bg=background_Colorblue)
    home_frame.config(bg=background_Colorblue)
    frame_1_for_title.config(bg=background_Colorblue)
    frame_2_for_title.config(bg=background_Colorblue)
    frame_3_for_title.config(bg=background_Colorblue)
    frame_4_for_title.config(bg=background_Colorblue)
    title.config(bg=background_Colorblue, image=YoutubeToVideoTitle)
    frame_1_for_link_entry_and_label.config(bg=background_Colorblue)
    frame_2_for_link_entry_and_label.config(bg=background_Colorblue)
    label_frame.config(bg=background_Colorblue)
    youtubeLink_label.config(bg=background_Colorblue, image=YoutubeLinkText)
    entry_image.config(image=YoutubeEntryBlue, bg=background_Colorblue)
    frame_for_paste_button.config(bg=widget_Colorblue)
    youtubeLink_entry.config(bg=widget_Colorblue, fg=text_Colorblue)
    Paste_button.config(image=PasteButtonGray, bg=widget_Colorblue)
    frame_for_format_label.config(bg=background_Colorblue)
    format_label.config(bg=background_Colorblue, image=FormatText)
    radio_buttons_frame.config(bg=background_Colorblue)
    Widget_for_radio_button_MP3.config(image=RadioWidgetBlue, bg=background_Colorblue)
    MP3_radioButton.config(bg=widget_Colorblue, fg=text_Colorblue, image=ActiveGray)
    MP3_text.config(bg=widget_Colorblue, image=SongText)
    Widget_for_radio_button_MP4.config(image=RadioWidgetBlue, bg=background_Colorblue)
    MP4_radioButton.config(bg=widget_Colorblue, fg=text_Colorblue, image=InActiveGray)
    MP4_text.config(bg=widget_Colorblue, image=VideoText)
    frame_1_for_location_entry_and_label.config(bg=background_Colorblue)
    frame_2_for_location_entry_and_label.config(bg=background_Colorblue)
    frame_for_label_location.config(bg=background_Colorblue)
    location_label.config(bg=background_Colorblue, image=LocationEntryText)
    location_entry.config(bg=background_Colorblue, fg=text_Colorblue, image=LocationEntryBlue)
    locationLink_entry.config(bg=widget_Colorblue, fg=text_Colorblue)
    convert_button.config(bg=background_Colorblue, fg=text_Colorblue, image=ConvertWidgetBlue)
    browse_button.config(bg=background_Colorblue, fg=text_Colorblue, image=BrowseWidgetBlue)
    frame1_for_screen_buttons.config(bg=background_Colorblue)
    frame_line_for_down_buttons.config(bg=line_colorblue)
    frame2_for_screen_buttons.config(bg=background_Colorblue)
    home_button.config(image=HomeButtonUnSelectedGray, bg=background_Colorblue)
    settings_image_button.config(image=SettingsButtonUnSelectedGray, bg=background_Colorblue)
    settings_frame.config(bg=background_Colorblue)
    frame_1_for_settings_title.config(bg=background_Colorblue)
    frame_2_for_settings_title.config(bg=background_Colorblue)
    frame_3_for_settings_title.config(bg=background_Colorblue)
    frame_4_for_settings_title.config(bg=background_Colorblue)
    settings_title.config(bg=background_Colorblue, image=settings_title_image)
    frame_1_for_layout.config(bg=background_Colorblue)
    frame_2_for_layout.config(bg=background_Colorblue)
    frame_for_label_layout.config(bg=background_Colorblue)
    layout_label.config(bg=background_Colorblue, image=label_color_layout)
    layout_widget.config(bg=background_Colorblue, image=LayoutWidgetBlue)
    gray_layout_button.config(bg=widget_Colorblue)
    blue_layout_button.config(bg=widget_Colorblue)
    white_layout_button.config(bg=widget_Colorblue)
    purple_layout_button.config(bg=widget_Colorblue)
    red_layout_button.config(bg=widget_Colorblue)
    green_layout_button.config(bg=widget_Colorblue)
    frame_1_for_preview.config(bg=background_Colorblue)
    frame_2_for_preview.config(bg=background_Colorblue)
    frame_for_preview_text.config(bg=background_Colorblue)
    preview_text.config(image=preview_text_image, bg=background_Colorblue)
    preview_widget.config(bg=background_Colorblue)
    apply_button.config(image=BlueApplyButton, bg=background_Colorblue)
    app_version_text.config(image=app_version_text_image, bg=background_Colorblue)


def show_white():
    root.iconbitmap(r"Assets/TitleIcon/WhiteIcon.ico")
    title_bar_color.set(root, background_Colorwhite)
    root.config(bg=background_Colorwhite)
    home_frame.config(bg=background_Colorwhite)
    frame_1_for_title.config(bg=background_Colorwhite)
    frame_2_for_title.config(bg=background_Colorwhite)
    frame_3_for_title.config(bg=background_Colorwhite)
    frame_4_for_title.config(bg=background_Colorwhite)
    title.config(bg=background_Colorwhite, image=YoutubeToVideoWhiteTitle)
    frame_1_for_link_entry_and_label.config(bg=background_Colorwhite)
    frame_2_for_link_entry_and_label.config(bg=background_Colorwhite)
    label_frame.config(bg=background_Colorwhite)
    youtubeLink_label.config(bg=background_Colorwhite, image=YoutubeLinkWhiteText)
    entry_image.config(image=YoutubeEntryWhite, bg=background_Colorwhite)
    frame_for_paste_button.config(bg=widget_Colorwhite)
    youtubeLink_entry.config(bg=widget_Colorwhite, fg=text_Colorwhite)
    Paste_button.config(image=PasteButtonWhite, bg=widget_Colorwhite)
    frame_for_format_label.config(bg=background_Colorwhite)
    format_label.config(bg=background_Colorwhite, image=FormatWhiteText)
    radio_buttons_frame.config(bg=background_Colorwhite)
    Widget_for_radio_button_MP3.config(image=RadioWidgetWhite, bg=background_Colorwhite)
    MP3_radioButton.config(bg=widget_Colorwhite, fg=text_Colorwhite, image=ActiveWhite)
    MP3_text.config(bg=widget_Colorwhite, image=SongWhiteText)
    Widget_for_radio_button_MP4.config(image=RadioWidgetWhite, bg=background_Colorwhite)
    MP4_radioButton.config(bg=widget_Colorwhite, fg=text_Colorwhite, image=InActiveWhite)
    MP4_text.config(bg=widget_Colorwhite, image=VideoWhiteText)
    frame_1_for_location_entry_and_label.config(bg=background_Colorwhite)
    frame_2_for_location_entry_and_label.config(bg=background_Colorwhite)
    frame_for_label_location.config(bg=background_Colorwhite)
    location_label.config(bg=background_Colorwhite, image=LocationWhiteText)
    location_entry.config(bg=background_Colorwhite, fg=text_Colorwhite, image=LocationEntryWhite)
    locationLink_entry.config(bg=widget_Colorwhite, fg=text_Colorwhite)
    convert_button.config(bg=background_Colorwhite, fg=text_Colorwhite, image=ConvertWidgetWhite)
    browse_button.config(bg=background_Colorwhite, fg=text_Colorwhite, image=BrowseWidgetWhite)
    frame1_for_screen_buttons.config(bg=background_Colorwhite)
    frame_line_for_down_buttons.config(bg=line_colorwhite)
    frame2_for_screen_buttons.config(bg=background_Colorwhite)
    home_button.config(image=HomeButtonUnSelectedWhite, bg=background_Colorwhite)
    settings_image_button.config(image=SettingsButtonUnSelectedWhite, bg=background_Colorwhite)
    settings_frame.config(bg=background_Colorwhite)
    frame_1_for_settings_title.config(bg=background_Colorwhite)
    frame_2_for_settings_title.config(bg=background_Colorwhite)
    frame_3_for_settings_title.config(bg=background_Colorwhite)
    frame_4_for_settings_title.config(bg=background_Colorwhite)
    settings_title.config(bg=background_Colorwhite, image=settings_title_image_white)
    frame_1_for_layout.config(bg=background_Colorwhite)
    frame_2_for_layout.config(bg=background_Colorwhite)
    frame_for_label_layout.config(bg=background_Colorwhite)
    layout_label.config(bg=background_Colorwhite, image=white_label_color_layout)
    layout_widget.config(bg=background_Colorwhite, image=white_layout_widget)
    gray_layout_button.config(bg=widget_Colorwhite)
    blue_layout_button.config(bg=widget_Colorwhite)
    white_layout_button.config(bg=widget_Colorwhite)
    purple_layout_button.config(bg=widget_Colorwhite)
    red_layout_button.config(bg=widget_Colorwhite)
    green_layout_button.config(bg=widget_Colorwhite)
    frame_1_for_preview.config(bg=background_Colorwhite)
    frame_2_for_preview.config(bg=background_Colorwhite)
    frame_for_preview_text.config(bg=background_Colorwhite)
    preview_text.config(image=white_preview_text, bg=background_Colorwhite)
    preview_widget.config(bg=background_Colorwhite)
    apply_button.config(image=white_apply_button, bg=background_Colorwhite)
    app_version_text.config(image=white_app_version_text, bg=background_Colorwhite)


def show_purple():
    root.iconbitmap(r"Assets/TitleIcon/PurpleIcon.ico")
    title_bar_color.set(root, background_Colorpurple)
    root.config(bg=background_Colorpurple)
    home_frame.config(bg=background_Colorpurple)
    frame_1_for_title.config(bg=background_Colorpurple)
    frame_2_for_title.config(bg=background_Colorpurple)
    frame_3_for_title.config(bg=background_Colorpurple)
    frame_4_for_title.config(bg=background_Colorpurple)
    title.config(bg=background_Colorpurple, image=YoutubeToVideoTitle)
    frame_1_for_link_entry_and_label.config(bg=background_Colorpurple)
    frame_2_for_link_entry_and_label.config(bg=background_Colorpurple)
    label_frame.config(bg=background_Colorpurple)
    youtubeLink_label.config(bg=background_Colorpurple, image=YoutubeLinkText)
    entry_image.config(image=YoutubeEntryPurple, bg=background_Colorpurple)
    frame_for_paste_button.config(bg=widget_Colorpurple)
    youtubeLink_entry.config(bg=widget_Colorpurple, fg=text_Colorpurple)
    Paste_button.config(image=PasteButtonGray, bg=widget_Colorpurple)
    frame_for_format_label.config(bg=background_Colorpurple)
    format_label.config(bg=background_Colorpurple, image=FormatText)
    radio_buttons_frame.config(bg=background_Colorpurple)
    Widget_for_radio_button_MP3.config(image=RadioWidgetPurple, bg=background_Colorpurple)
    MP3_radioButton.config(bg=widget_Colorpurple, fg=text_Colorpurple, image=ActiveGray)
    MP3_text.config(bg=widget_Colorpurple, image=SongText)
    Widget_for_radio_button_MP4.config(image=RadioWidgetPurple, bg=background_Colorpurple)
    MP4_radioButton.config(bg=widget_Colorpurple, fg=text_Colorpurple, image=InActiveGray)
    MP4_text.config(bg=widget_Colorpurple, image=VideoText)
    frame_1_for_location_entry_and_label.config(bg=background_Colorpurple)
    frame_2_for_location_entry_and_label.config(bg=background_Colorpurple)
    frame_for_label_location.config(bg=background_Colorpurple)
    location_label.config(bg=background_Colorpurple, image=LocationEntryText)
    location_entry.config(bg=background_Colorpurple, fg=text_Colorpurple, image=LocationEntryPurple)
    locationLink_entry.config(bg=widget_Colorpurple, fg=text_Colorpurple)
    convert_button.config(bg=background_Colorpurple, fg=text_Colorpurple, image=ConvertWidgetPurple)
    browse_button.config(bg=background_Colorpurple, fg=text_Colorpurple, image=BrowseWidgetPurple)
    frame1_for_screen_buttons.config(bg=background_Colorpurple)
    frame_line_for_down_buttons.config(bg=line_colorpurple)
    frame2_for_screen_buttons.config(bg=background_Colorpurple)
    home_button.config(image=HomeButtonUnSelectedGray, bg=background_Colorpurple)
    settings_image_button.config(image=SettingsButtonUnSelectedGray, bg=background_Colorpurple)
    settings_frame.config(bg=background_Colorpurple)
    frame_1_for_settings_title.config(bg=background_Colorpurple)
    frame_2_for_settings_title.config(bg=background_Colorpurple)
    frame_3_for_settings_title.config(bg=background_Colorpurple)
    frame_4_for_settings_title.config(bg=background_Colorpurple)
    settings_title.config(bg=background_Colorpurple, image=settings_title_image)
    frame_1_for_layout.config(bg=background_Colorpurple)
    frame_2_for_layout.config(bg=background_Colorpurple)
    frame_for_label_layout.config(bg=background_Colorpurple)
    layout_label.config(bg=background_Colorpurple, image=label_color_layout)
    layout_widget.config(bg=background_Colorpurple, image=LayoutWidgetPurple)
    gray_layout_button.config(bg=widget_Colorpurple)
    blue_layout_button.config(bg=widget_Colorpurple)
    white_layout_button.config(bg=widget_Colorpurple)
    purple_layout_button.config(bg=widget_Colorpurple)
    red_layout_button.config(bg=widget_Colorpurple)
    green_layout_button.config(bg=widget_Colorpurple)
    frame_1_for_preview.config(bg=background_Colorpurple)
    frame_2_for_preview.config(bg=background_Colorpurple)
    frame_for_preview_text.config(bg=background_Colorpurple)
    preview_text.config(image=preview_text_image, bg=background_Colorpurple)
    preview_widget.config(bg=background_Colorpurple)
    apply_button.config(image=PurpleApplyButton, bg=background_Colorpurple)
    app_version_text.config(image=app_version_text_image, bg=background_Colorpurple)


def show_red():
    root.iconbitmap(r"Assets/TitleIcon/RedIcon.ico")
    title_bar_color.set(root, background_Colorred)
    root.config(bg=background_Colorred)
    home_frame.config(bg=background_Colorred)
    frame_1_for_title.config(bg=background_Colorred)
    frame_2_for_title.config(bg=background_Colorred)
    frame_3_for_title.config(bg=background_Colorred)
    frame_4_for_title.config(bg=background_Colorred)
    title.config(bg=background_Colorred, image=YoutubeToVideoTitle)
    frame_1_for_link_entry_and_label.config(bg=background_Colorred)
    frame_2_for_link_entry_and_label.config(bg=background_Colorred)
    label_frame.config(bg=background_Colorred)
    youtubeLink_label.config(bg=background_Colorred, image=YoutubeLinkText)
    entry_image.config(image=YoutubeEntryRed, bg=background_Colorred)
    frame_for_paste_button.config(bg=widget_Colorred)
    youtubeLink_entry.config(bg=widget_Colorred, fg=text_Colorred)
    Paste_button.config(image=PasteButtonGray, bg=widget_Colorred)
    frame_for_format_label.config(bg=background_Colorred)
    format_label.config(bg=background_Colorred, image=FormatText)
    radio_buttons_frame.config(bg=background_Colorred)
    Widget_for_radio_button_MP3.config(image=RadioWidgetRed, bg=background_Colorred)
    MP3_radioButton.config(bg=widget_Colorred, fg=text_Colorred, image=ActiveGray)
    MP3_text.config(bg=widget_Colorred, image=SongText)
    Widget_for_radio_button_MP4.config(image=RadioWidgetRed, bg=background_Colorred)
    MP4_radioButton.config(bg=widget_Colorred, fg=text_Colorred, image=InActiveGray)
    MP4_text.config(bg=widget_Colorred, image=VideoText)
    frame_1_for_location_entry_and_label.config(bg=background_Colorred)
    frame_2_for_location_entry_and_label.config(bg=background_Colorred)
    frame_for_label_location.config(bg=background_Colorred)
    location_label.config(bg=background_Colorred, image=LocationEntryText)
    location_entry.config(bg=background_Colorred, fg=text_Colorred, image=LocationEntryRed)
    locationLink_entry.config(bg=widget_Colorred, fg=text_Colorred)
    convert_button.config(bg=background_Colorred, fg=text_Colorred, image=ConvertWidgetRed)
    browse_button.config(bg=background_Colorred, fg=text_Colorred, image=BrowseWidgetRed)
    frame1_for_screen_buttons.config(bg=background_Colorred)
    frame_line_for_down_buttons.config(bg=line_colorred)
    frame2_for_screen_buttons.config(bg=background_Colorred)
    home_button.config(image=HomeButtonUnSelectedGray, bg=background_Colorred)
    settings_image_button.config(image=SettingsButtonUnSelectedGray, bg=background_Colorred)
    settings_frame.config(bg=background_Colorred)
    frame_1_for_settings_title.config(bg=background_Colorred)
    frame_2_for_settings_title.config(bg=background_Colorred)
    frame_3_for_settings_title.config(bg=background_Colorred)
    frame_4_for_settings_title.config(bg=background_Colorred)
    settings_title.config(bg=background_Colorred, image=settings_title_image)
    frame_1_for_layout.config(bg=background_Colorred)
    frame_2_for_layout.config(bg=background_Colorred)
    frame_for_label_layout.config(bg=background_Colorred)
    layout_label.config(bg=background_Colorred, image=label_color_layout)
    layout_widget.config(bg=background_Colorred, image=LayoutWidgetRed)
    gray_layout_button.config(bg=widget_Colorred)
    blue_layout_button.config(bg=widget_Colorred)
    white_layout_button.config(bg=widget_Colorred)
    purple_layout_button.config(bg=widget_Colorred)
    red_layout_button.config(bg=widget_Colorred)
    green_layout_button.config(bg=widget_Colorred)
    frame_1_for_preview.config(bg=background_Colorred)
    frame_2_for_preview.config(bg=background_Colorred)
    frame_for_preview_text.config(bg=background_Colorred)
    preview_text.config(image=preview_text_image, bg=background_Colorred)
    preview_widget.config(bg=background_Colorred)
    apply_button.config(image=RedApplyButton, bg=background_Colorred)
    app_version_text.config(image=app_version_text_image, bg=background_Colorred)


def show_green():
    root.iconbitmap(r"Assets/TitleIcon/GreenIcon.ico")
    title_bar_color.set(root, background_colorgreen)
    root.config(bg=background_colorgreen)
    home_frame.config(bg=background_colorgreen)
    frame_1_for_title.config(bg=background_colorgreen)
    frame_2_for_title.config(bg=background_colorgreen)
    frame_3_for_title.config(bg=background_colorgreen)
    frame_4_for_title.config(bg=background_colorgreen)
    title.config(bg=background_colorgreen, image=YoutubeToVideoTitle)
    frame_1_for_link_entry_and_label.config(bg=background_colorgreen)
    frame_2_for_link_entry_and_label.config(bg=background_colorgreen)
    label_frame.config(bg=background_colorgreen)
    youtubeLink_label.config(bg=background_colorgreen, image=YoutubeLinkText)
    entry_image.config(image=YoutubeEntryGreen, bg=background_colorgreen)
    frame_for_paste_button.config(bg=widget_colorgreen)
    youtubeLink_entry.config(bg=widget_colorgreen, fg=text_colorgreen)
    Paste_button.config(image=PasteButtonGray, bg=widget_colorgreen)
    frame_for_format_label.config(bg=background_colorgreen)
    format_label.config(bg=background_colorgreen, image=FormatText)
    radio_buttons_frame.config(bg=background_colorgreen)
    Widget_for_radio_button_MP3.config(image=RadioWidgetGreen, bg=background_colorgreen)
    MP3_radioButton.config(bg=widget_colorgreen, fg=text_colorgreen, image=ActiveGray)
    MP3_text.config(bg=widget_colorgreen, image=SongText)
    Widget_for_radio_button_MP4.config(image=RadioWidgetGreen, bg=background_colorgreen)
    MP4_radioButton.config(bg=widget_colorgreen, fg=text_colorgreen, image=InActiveGray)
    MP4_text.config(bg=widget_colorgreen, image=VideoText)
    frame_1_for_location_entry_and_label.config(bg=background_colorgreen)
    frame_2_for_location_entry_and_label.config(bg=background_colorgreen)
    frame_for_label_location.config(bg=background_colorgreen)
    location_label.config(bg=background_colorgreen, image=LocationEntryText)
    location_entry.config(bg=background_colorgreen, fg=text_colorgreen, image=LocationEntryGreen)
    locationLink_entry.config(bg=widget_colorgreen, fg=text_colorgreen)
    convert_button.config(bg=background_colorgreen, fg=text_colorgreen, image=ConvertWidgetGreen)
    browse_button.config(bg=background_colorgreen, fg=text_colorgreen, image=BrowseWidgetGreen)
    frame1_for_screen_buttons.config(bg=background_colorgreen)
    frame_line_for_down_buttons.config(bg=line_colorgreen)
    frame2_for_screen_buttons.config(bg=background_colorgreen)
    home_button.config(image=HomeButtonUnSelectedGray, bg=background_colorgreen)
    settings_image_button.config(image=SettingsButtonUnSelectedGray, bg=background_colorgreen)
    settings_frame.config(bg=background_colorgreen)
    frame_1_for_settings_title.config(bg=background_colorgreen)
    frame_2_for_settings_title.config(bg=background_colorgreen)
    frame_3_for_settings_title.config(bg=background_colorgreen)
    frame_4_for_settings_title.config(bg=background_colorgreen)
    settings_title.config(bg=background_colorgreen, image=settings_title_image)
    frame_1_for_layout.config(bg=background_colorgreen)
    frame_2_for_layout.config(bg=background_colorgreen)
    frame_for_label_layout.config(bg=background_colorgreen)
    layout_label.config(bg=background_colorgreen, image=label_color_layout)
    layout_widget.config(bg=background_colorgreen, image=LayoutWidgetGreen)
    gray_layout_button.config(bg=widget_colorgreen)
    blue_layout_button.config(bg=widget_colorgreen)
    white_layout_button.config(bg=widget_colorgreen)
    purple_layout_button.config(bg=widget_colorgreen)
    red_layout_button.config(bg=widget_colorgreen)
    green_layout_button.config(bg=widget_colorgreen)
    frame_1_for_preview.config(bg=background_colorgreen)
    frame_2_for_preview.config(bg=background_colorgreen)
    frame_for_preview_text.config(bg=background_colorgreen)
    preview_text.config(image=preview_text_image, bg=background_colorgreen)
    preview_widget.config(bg=background_colorgreen)
    apply_button.config(image=GreenApplyButton, bg=background_colorgreen)
    app_version_text.config(image=app_version_text_image, bg=background_colorgreen)


def remove_focus(event):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = root.winfo_x()
    y = root.winfo_y()

    # Check if the window is out-of-screen bounds
    if x < 0 or y < 0 or (x + window_width) > screen_width or (y + window_height) > screen_height:
        # Bring the window to the center if out of bounds
        new_x = max(0, min(x, screen_width - window_width))
        new_y = max(0, min(y, screen_height - window_height))
        root.geometry(f'{window_width}x{window_height}+{new_x}+{new_y}')

    root.focus()  # Focus back to the root widget to remove focus from entries
    root.update()  # Update to ensure focus is properly removed


# Function to recursively bind frames
def bind_all_frames(parent):
    for child in parent.winfo_children():
        if isinstance(child, Frame):
            child.bind("<Button-1>", remove_focus)
        bind_all_frames(child)  # Recursively bind frames inside this frame


# Ensure the mainloop() is not being restarted elsewhere in the code
root = Tk()
selected_layout = StringVar()
root.title("‎")
root.iconbitmap(r"Assets/TitleIcon/GrayIcon.ico")
root.geometry('374x638')
root.configure(background=background_Color)

# Load images

# Local things (for all layouts except white and some white)
settingsTitleImage = PhotoImage(file='../Project1/Assets/LocalThings/SettingsTitle.png')
YoutubeToVideoTitle = PhotoImage(file="../Project1/Assets/LocalThings/YoutubeToVideoTitle.png")
YoutubeLinkText = PhotoImage(file="../Project1/Assets/LocalThings/YoutubeLinkText.png")
FormatText = PhotoImage(file="../Project1/Assets/LocalThings/FormatText.png")
SongText = PhotoImage(file="../Project1/Assets/LocalThings/SongText.png")
VideoText = PhotoImage(file="../Project1/Assets/LocalThings/VideoText.png")
LocationEntryText = PhotoImage(file="../Project1/Assets/LocalThings/LocationEntryText.png")
white_layout = PhotoImage(file="../Project1/Assets/LocalThings/WhiteLayoutButton.png")
red_layout = PhotoImage(file="../Project1/Assets/LocalThings/RedLayoutButton.png")
purple_layout = PhotoImage(file="../Project1/Assets/LocalThings/PurpleLayoutButton.png")
green_layout = PhotoImage(file="../Project1/Assets/LocalThings/GreenLayoutButton.png")
gray_layout = PhotoImage(file="../Project1/Assets/LocalThings/GrayLayoutButton.png")
blue_layout = PhotoImage(file="../Project1/Assets/LocalThings/BlueLayoutButton.png")
PasteButtonGray = PhotoImage(file="../Project1/Assets/LocalThings/PasteButtonGray.png")
app_version_text_image = PhotoImage(file="../Project1/Assets/LocalThings/GrayAppVersionText.png")
settings_title_image = PhotoImage(file='../Project1/Assets/LocalThings/SettingsTitle.png')
preview_text_image = PhotoImage(file='../Project1/Assets/LocalThings/GrayPreviewText.png')
label_color_layout = PhotoImage(file="../Project1/Assets/LocalThings/LayoutText.png")

# Down Buttons
HomeButtonSelectedGray = PhotoImage(file="../Project1/Assets/DownButtons/HomeButtonSelectedGray.png")
HomeButtonUnSelectedGray = PhotoImage(file="../Project1/Assets/DownButtons/HomeButtonUnSelectedGray.png")
SettingsButtonSelectedGray = PhotoImage(file="../Project1/Assets/DownButtons/SettingsButtonSelectedGray.png")
SettingsButtonUnSelectedGray = PhotoImage(file="../Project1/Assets/DownButtons/SettingsButtonUnSelectedGray.png")
HomeButtonUnSelectedWhite = PhotoImage(file="../Project1/Assets/DownButtons/HomeButtonUnSelectedWhite.png")
SettingsButtonSelectedWhite = PhotoImage(file="../Project1/Assets/DownButtons/SettingsButtonSelectedWhite.png")
SettingsButtonUnSelectedWhite = PhotoImage(file="../Project1/Assets/DownButtons/SettingsButtonUnSelectedWhite.png")

# Gray Layout
YoutubeEntryGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/Entrys/GrayEntryWidget.png")
RadioWidgetGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/Widgets/RadioWidgetGray.png")
InActiveGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/RadioButtons/InactiveGray.png")
ActiveGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/RadioButtons/activeGray.png")
LocationEntryGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/Entrys/EntryWidgetGray.png")
BrowseWidgetGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/Buttons/BrowseWidgetGray.png")
ConvertWidgetGray = PhotoImage(file="../Project1/Assets/HomeFrame/GrayLayout/Buttons/ConvertWidgetGray.png")
apply_button_image = PhotoImage(file="../Project1/Assets/SettingsFrame/GrayLayout/Buttons/GrayApplyButton.png")
layout_widget_image = PhotoImage(file="../Project1/Assets/SettingsFrame/GrayLayout/Widgets/LayoutWidget.png")
gray_preview_widget_image = PhotoImage(
    file='../Project1/Assets/SettingsFrame/GrayLayout/Widgets/GrayPreviewWidget.png')

# Blue Layout
YoutubeEntryBlue = PhotoImage(file="../Project1/Assets/HomeFrame/BlueLayout/Entrys/EntryBlueWidget.png")
RadioWidgetBlue = PhotoImage(file="../Project1/Assets/HomeFrame/BlueLayout/Widgets/RadioWidget.png")
LocationEntryBlue = PhotoImage(file="../Project1/Assets/HomeFrame/BlueLayout/Entrys/EntryBlueWidget.png")
BrowseWidgetBlue = PhotoImage(file="../Project1/Assets/HomeFrame/BlueLayout/Buttons/BrowseButton.png")
ConvertWidgetBlue = PhotoImage(file="../Project1/Assets/HomeFrame/BlueLayout/Buttons/ConvertButton.png")
BluePreviewWidget = PhotoImage(file="../Project1/Assets/SettingsFrame/BlueLayout/Widgets/PreviewLayout.png")
LayoutWidgetBlue = PhotoImage(file="../Project1/Assets/SettingsFrame/BlueLayout/Widgets/LayoutWidget.png")
BlueApplyButton = PhotoImage(file="../Project1/Assets/SettingsFrame/BlueLayout/Buttons/ApplyButton.png")

# White Layout
YoutubeToVideoWhiteTitle = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Texts/YoutubetoVideoWhiteTitle.png")
YoutubeLinkWhiteText = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Texts/YoutubeLinkText.png")
YoutubeEntryWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Entrys/EntryWidgetWhite.png")
PasteButtonWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Buttons/PasteButtonWhite.png")
FormatWhiteText = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Texts/FormatWhiteText.png")
RadioWidgetWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Widgets/RadioWidgetWhite.png")
InActiveWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/RadioButtons/InactiveWhite.png")
ActiveWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/RadioButtons/activeWhite.png")
SongWhiteText = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Texts/SongText.png")
VideoWhiteText = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Texts/VideoText.png")
LocationWhiteText = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Texts/LocationText.png")
LocationEntryWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Entrys/EntryWidgetWhite.png")
BrowseWidgetWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Buttons/BrowseWidgetWhite.png")
ConvertWidgetWhite = PhotoImage(file="../Project1/Assets/HomeFrame/WhiteLayout/Buttons/ConvertWidgetWhite.png")
HomeButtonSelectedWhite = PhotoImage(file="../Project1/Assets/DownButtons/HomeButtonSelectedWhite.png")
settings_title_image_white = PhotoImage(file='../Project1/Assets/SettingsFrame/WhiteLayout/Texts/SettingsTextTitleWhite.png')
white_label_color_layout = PhotoImage(file="../Project1/Assets/SettingsFrame/WhiteLayout/Texts/WhiteLayoutText.png")
white_layout_widget = PhotoImage(file="../Project1/Assets/SettingsFrame/WhiteLayout/Texts/WhiteLayoutWidget.png")
white_preview_text = PhotoImage(file="../Project1/Assets/SettingsFrame/WhiteLayout/Texts/WhitePreviewText.png")
white_apply_button = PhotoImage(file="../Project1/Assets/SettingsFrame/WhiteLayout/Texts/WhiteApplyButton.png")
white_app_version_text = PhotoImage(file="../Project1/Assets/SettingsFrame/WhiteLayout/Texts/WhiteAppVersionText.png")
white_preview_widget_image = PhotoImage(
    file='../Project1/Assets/SettingsFrame/WhiteLayout/Widgets/WhitePreviewWidget.png')

# Purple Layout
YoutubeEntryPurple = PhotoImage(file="../Project1/Assets/HomeFrame/PurpleLayout/Entrys/EntryWidget.png")
RadioWidgetPurple = PhotoImage(file="../Project1/Assets/HomeFrame/PurpleLayout/Widgets/RadioWidget.png")
LocationEntryPurple = PhotoImage(file="../Project1/Assets/HomeFrame/PurpleLayout/Entrys/EntryWidget.png")
BrowseWidgetPurple = PhotoImage(file="../Project1/Assets/HomeFrame/PurpleLayout/Buttons/BrowseButton.png")
ConvertWidgetPurple = PhotoImage(file="../Project1/Assets/HomeFrame/PurpleLayout/Buttons/ConvertButton.png")
PurplePreviewWidget = PhotoImage(file="../Project1/Assets/SettingsFrame/PurpleLayout/Widgets/PreviewLayout.png")
LayoutWidgetPurple = PhotoImage(file="../Project1/Assets/SettingsFrame/PurpleLayout/Widgets/LayoutWidget.png")
PurpleApplyButton = PhotoImage(file="../Project1/Assets/SettingsFrame/PurpleLayout/Buttons/ApplyButton.png")

# Red Layout
YoutubeEntryRed = PhotoImage(file="../Project1/Assets/HomeFrame/RedLayout/Entrys/RedEntry.png")
RadioWidgetRed = PhotoImage(file="../Project1/Assets/HomeFrame/RedLayout/Widgets/RadioWidget.png")
LocationEntryRed = PhotoImage(file="../Project1/Assets/HomeFrame/RedLayout/Entrys/RedEntry.png")
BrowseWidgetRed = PhotoImage(file="../Project1/Assets/HomeFrame/RedLayout/Buttons/BrowseButton.png")
ConvertWidgetRed = PhotoImage(file="../Project1/Assets/HomeFrame/RedLayout/Buttons/ConvertButton.png")
RedPreviewWidget = PhotoImage(file="../Project1/Assets/SettingsFrame/RedLayout/Widgets/PreviewLayout.png")
LayoutWidgetRed = PhotoImage(file="../Project1/Assets/SettingsFrame/RedLayout/Widgets/LayoutWidget.png")
RedApplyButton = PhotoImage(file="../Project1/Assets/SettingsFrame/RedLayout/Buttons/ApplyButton.png")

# Green Layout
YoutubeEntryGreen = PhotoImage(file="../Project1/Assets/HomeFrame/GreenLayout/Entrys/EntryWidget.png")
RadioWidgetGreen = PhotoImage(file="../Project1/Assets/HomeFrame/GreenLayout/Widgets/RadioWidget.png")
LocationEntryGreen = PhotoImage(file="../Project1/Assets/HomeFrame/GreenLayout/Entrys/EntryWidget.png")
BrowseWidgetGreen = PhotoImage(file="../Project1/Assets/HomeFrame/GreenLayout/Buttons/BrowseButton.png")
ConvertWidgetGreen = PhotoImage(file="../Project1/Assets/HomeFrame/GreenLayout/Buttons/ConvertButton.png")
GreenPreviewWidget = PhotoImage(file="../Project1/Assets/SettingsFrame/GreenLayout/Widgets/PreviewWidget.png")
LayoutWidgetGreen = PhotoImage(file="../Project1/Assets/SettingsFrame/GreenLayout/Widgets/LayoutWidget.png")
GreenApplyButton = PhotoImage(file="../Project1/Assets/SettingsFrame/GreenLayout/Buttons/ApplyButton.png")

var = IntVar()

home_frame = Frame(root, width=374, height=568, bg=background_Color)
home_frame.place(x=0, y=0)

frame_1_for_title = Frame(home_frame, width=390, height=72, bg=background_Color)
frame_1_for_title.place(x=0, y=0)

frame_2_for_title = Frame(frame_1_for_title, width=358, height=48, bg=background_Color)
frame_2_for_title.place(x=8, y=16)

frame_3_for_title = Frame(frame_2_for_title, width=262, height=22, bg=background_Color)
frame_3_for_title.place(x=48, y=12)

frame_4_for_title = Frame(frame_3_for_title, width=204, height=22, bg=background_Color)
frame_4_for_title.place(x=29, y=0)

title = Label(frame_4_for_title, image=YoutubeToVideoTitle, bg=background_Color)
title.place(x=30, y=0)

# Link entry and label.
frame_1_for_link_entry_and_label = Frame(home_frame, width=374, height=112, bg=background_Color)
frame_1_for_link_entry_and_label.place(x=0, y=72)

frame_2_for_link_entry_and_label = Frame(frame_1_for_link_entry_and_label, width=358, height=88, bg=background_Color)
frame_2_for_link_entry_and_label.place(x=8, y=12)

label_frame = Frame(frame_2_for_link_entry_and_label, width=358, height=32, bg=background_Color)
label_frame.place(x=0, y=0)

youtubeLink_label = Label(label_frame, image=YoutubeLinkText, bg=background_Color)
youtubeLink_label.place(x=0, y=0)

# Image and entry field
entry_image = Label(frame_2_for_link_entry_and_label, image=YoutubeEntryGray, border=0, bg=background_Color)
entry_image.place(x=0, y=32)

frame_for_paste_button = Frame(entry_image, width=24, height=24, bg=widget_Color)
frame_for_paste_button.place(x=318, y=16)

youtubeLink_entry = Entry(entry_image, border=0, bg=widget_Color, font=('bold', 16), fg=text_Color)
youtubeLink_entry.insert(0, 'Paste link')
youtubeLink_entry.bind('<FocusIn>', on_focus_in_youtubeLink_entry)
youtubeLink_entry.bind('<FocusOut>', on_focus_out_youtubeLink_entry)
youtubeLink_entry.place(x=20, y=5, height=50, width=300)  # Adjusted y-coordinate to avoid overlap with the image

Paste_button = Button(frame_for_paste_button, border=0, bg=widget_Color, image=PasteButtonGray,
                      command=lambda: youtubeLink_entry.insert(0, root.clipboard_get()), activebackground=widget_Color)
Paste_button.place(x=0, y=0)

frame_for_format_label = Frame(home_frame, width=54, height=45, bg=background_Color)
frame_for_format_label.place(x=8, y=201)

format_label = Label(frame_for_format_label, image=FormatText, bg=background_Color)
format_label.place(x=0, y=0)

file_type_var = StringVar(value="mp3")
selected_layout = StringVar(value="gray")


def file_type_vari(variable):
    file_type_var.set(variable)


radio_buttons_frame = Frame(home_frame, width=256, height=151, bg=background_Color)
radio_buttons_frame.place(x=61, y=200)

Widget_for_radio_button_MP3 = Label(radio_buttons_frame, image=RadioWidgetGray,
                                    bg=background_Color)
Widget_for_radio_button_MP3.place(x=20, y=20)

# Create labels to act as radio buttons
MP3_radioButton = Label(Widget_for_radio_button_MP3, image=ActiveGray, border=0, bg=widget_Color)
MP3_radioButton.place(x=12, y=11)
MP3_radioButton.bind("<Button-1>", lambda e: toggle_radio(1))

MP3_text = Label(Widget_for_radio_button_MP3, image=SongText, bg=widget_Color)
MP3_text.place(x=47, y=18)

Widget_for_radio_button_MP4 = Label(radio_buttons_frame, image=RadioWidgetGray,
                                    bg=background_Color)
Widget_for_radio_button_MP4.place(x=20, y=82)

MP4_radioButton = Label(Widget_for_radio_button_MP4, image=InActiveGray, border=0, bg=widget_Color)
MP4_radioButton.place(x=12, y=11)
MP4_radioButton.bind("<Button-1>", lambda e: toggle_radio(2))

MP4_text = Label(Widget_for_radio_button_MP4, image=VideoText, bg=widget_Color)
MP4_text.place(x=47, y=18)

frame_1_for_location_entry_and_label = Frame(home_frame, width=390, height=112, bg=background_Color)
frame_1_for_location_entry_and_label.place(x=0, y=339)

frame_2_for_location_entry_and_label = Frame(frame_1_for_location_entry_and_label, width=358, height=88,
                                             bg=background_Color)
frame_2_for_location_entry_and_label.place(x=8, y=12)

frame_for_label_location = Frame(frame_2_for_location_entry_and_label, width=358, height=32, bg=background_Color)
frame_for_label_location.place(x=0, y=0)

location_label = Label(frame_for_label_location, bg=background_Color, image=LocationEntryText)
location_label.place(x=0, y=0)

location_entry = Label(frame_2_for_location_entry_and_label, image=LocationEntryGray, border=0, bg=background_Color)
location_entry.place(x=0, y=32)

save_path_var = StringVar()
locationLink_entry = Entry(location_entry, border=0, bg=widget_Color, font=('bold', 16), fg=text_Color,
                           textvariable=save_path_var)
locationLink_entry.insert(0, 'Paste here')
locationLink_entry.bind('<FocusIn>', on_focus_in_locationLink_entry)
locationLink_entry.bind('<FocusOut>', on_focus_out_locationLink_entry)
locationLink_entry.place(x=20, y=5, height=50, width=300)

# Bind a click event to the root to unfocus the entries when clicking anywhere else
root.bind_all('<Button-1>', focus_out_all_entries, add="+")

# Convert Button
convert_button = Label(home_frame, image=ConvertWidgetGray, bg=background_Color)
convert_button.place(x=53, y=512)
convert_button.bind("<Button-1>", lambda e: download())

# Browse Button
browse_button = Label(home_frame, image=BrowseWidgetGray, bg=background_Color)
browse_button.place(x=106, y=460)
browse_button.bind("<Button-1>", lambda e: browse_save_location())

frame1_for_screen_buttons = Frame(root, width=390, height=70, bg=background_Color)
frame1_for_screen_buttons.place(x=0, y=568)

frame_line_for_down_buttons = Frame(frame1_for_screen_buttons, width=390, height=1, bg=line_color)
frame_line_for_down_buttons.place(x=0, y=0)

frame2_for_screen_buttons = Frame(frame1_for_screen_buttons, width=358, height=54, bg=background_Color)
frame2_for_screen_buttons.place(x=8, y=8)

home_button = Label(frame2_for_screen_buttons, width=114, height=54, bg=background_Color, image=HomeButtonSelectedGray)
home_button.place(x=65, y=0)
home_button.bind("<Button-1>", lambda e: switch_button("home"))

settings_image_button = Label(frame2_for_screen_buttons, width=114, height=54, bg=background_Color,
                              image=SettingsButtonUnSelectedGray)
settings_image_button.place(x=179, y=0)
settings_image_button.bind("<Button-1>", lambda e: switch_button("settings"))

settings_frame = Frame(root, bg=background_Color, width=374, height=568)
settings_frame.place_forget()

frame_1_for_settings_title = Frame(settings_frame, width=390, height=72, bg=background_Color)
frame_1_for_settings_title.place(x=0, y=0)

frame_2_for_settings_title = Frame(frame_1_for_settings_title, width=358, height=48, bg=background_Color)
frame_2_for_settings_title.place(x=8, y=16)

frame_3_for_settings_title = Frame(frame_2_for_settings_title, width=262, height=22, bg=background_Color)
frame_3_for_settings_title.place(x=48, y=12)

frame_4_for_settings_title = Frame(frame_3_for_settings_title, width=204, height=22, bg=background_Color)
frame_4_for_settings_title.place(x=29, y=0)

settings_title = Label(frame_4_for_settings_title, image=settings_title_image, bg=background_Color)
settings_title.place(x=60, y=0)

frame_1_for_layout = Frame(settings_frame, width=390, height=220, bg=background_Color)
frame_1_for_layout.place(x=0, y=72)

frame_2_for_layout = Frame(frame_1_for_layout, width=358, height=172, bg=background_Color)
frame_2_for_layout.place(x=8, y=12)

frame_for_label_layout = Frame(frame_2_for_layout, width=358, height=32, bg=background_Color)
frame_for_label_layout.place(x=0, y=0)

layout_label = Label(frame_for_label_layout, image=label_color_layout, bg=background_Color)
layout_label.place(x=0, y=0)

layout_widget = Label(frame_2_for_layout, image=layout_widget_image, bg=background_Color)
layout_widget.place(x=0, y=32)

gray_layout_button = Label(layout_widget, image=gray_layout, bg=widget_Color)
gray_layout_button.place(x=50, y=17)
gray_layout_button.bind("<Button-1>", lambda e: [selected_layout.set("gray"), show_gray_preview()])

blue_layout_button = Label(layout_widget, image=blue_layout, bg=widget_Color)
blue_layout_button.place(x=156, y=17)
blue_layout_button.bind("<Button-1>", lambda e: [selected_layout.set("blue"), show_blue_preview()])

white_layout_button = Label(layout_widget, image=white_layout, bg=widget_Color)
white_layout_button.place(x=263, y=17)
white_layout_button.bind("<Button-1>", lambda e: [selected_layout.set("white"), show_white_preview()])

purple_layout_button = Label(layout_widget, image=purple_layout, bg=widget_Color)
purple_layout_button.place(x=50, y=73)
purple_layout_button.bind("<Button-1>", lambda e: [selected_layout.set("purple"), show_purple_preview()])

red_layout_button = Label(layout_widget, image=red_layout, bg=widget_Color)
red_layout_button.place(x=156, y=73)
red_layout_button.bind("<Button-1>", lambda e: [selected_layout.set("red"), show_red_preview()])

green_layout_button = Label(layout_widget, image=green_layout, bg=widget_Color)
green_layout_button.place(x=263, y=73)
green_layout_button.bind("<Button-1>", lambda e: [selected_layout.set("green"), show_green_preview()])

frame_1_for_preview = Frame(settings_frame, width=390, height=100, bg=background_Color)
frame_1_for_preview.place(x=0, y=246)

frame_2_for_preview = Frame(frame_1_for_preview, width=358, height=88, bg=background_Color)
frame_2_for_preview.place(x=8, y=9)

frame_for_preview_text = Frame(frame_2_for_preview, width=358, height=32, bg=background_Color)
frame_for_preview_text.place(x=0, y=10)

preview_text = Label(frame_for_preview_text, image=preview_text_image, bg=background_Color)
preview_text.place(x=0, y=0)

preview_widget = Label(frame_2_for_preview, image=gray_preview_widget_image, bg=background_Color)
preview_widget.place(x=0, y=32)

apply_button = Label(settings_frame, image=apply_button_image, bg=background_Color)
apply_button.place(x=110, y=337)
apply_button.bind("<Button-1>", apply_color)

app_version_text = Label(settings_frame, image=app_version_text_image, bg=background_Color)
app_version_text.place(x=0, y=544)

root.resizable(False, False)
title_bar_color.set(root, background_Color)
switch_button("home")
bind_all_frames(root)

root.mainloop()
