import sqlite3
import requests
from PIL import ImageTk, Image
from io import BytesIO
from tkinter import Tk, Frame, Label, Scrollbar, Listbox, Button, Entry, END, VERTICAL, Toplevel, Canvas
import webbrowser
import insert_page as ip


def Tkinter():
    conn = sqlite3.connect("novel_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM novels")
    data = cursor.fetchall()

    cursor.close()

    window = Tk()
    window.title("Novel Database")
    window.geometry("800x600")

    frame = Frame(window)
    frame.pack(fill="both", expand=True)

    search_frame = Frame(frame)
    search_frame.pack(fill="x", padx=10, pady=10)

    search_entry = Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True)

    button_frame = Frame(frame)
    button_frame.pack(fill="x", padx=10)

    connection = sqlite3.connect('novel_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT novel_link FROM novels")
    urls = cursor.fetchall()

    connection.close()

    def update_all_novels():
        for url in urls:
            ip.insert(url[0])

    button1 = Button(button_frame, text="Update All", command=update_all_novels)
    button1.pack(side="left", padx=5)

    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(frame, yscrollcommand=scrollbar.set)
    listbox.pack(fill="both", expand=True)

    scrollbar.config(command=listbox.yview)

    def populate_listbox():
        for item in data:
            listbox.insert(END, item[1])

    def clear_listbox():
        listbox.delete(0, END)

    def show_novel_window(event):
        if listbox.curselection():  
            selected_item = listbox.get(listbox.curselection())
            if selected_item:
                selected_data = next((item for item in data if item[1] == selected_item), None)
                if selected_data:
                    novel_title = selected_data[1]
                    novel_image_url = selected_data[5]
                    novel_description = selected_data[3]
                    novel_other_names = selected_data[4]
                    novel_type = selected_data[6]
                    novel_language = selected_data[7]
                    novel_artist = selected_data[8]
                    novel_year = selected_data[9]
                    novel_original_chapters = selected_data[10]
                    Novel_license_status = selected_data[11]
                    Novel_finished_translation = selected_data[12]
                    Novel_original_publisher = selected_data[13]
                    Novel_release_frequency = selected_data[14]

                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT genre_name FROM genres JOIN novel_genres ON genres.genre_id = novel_genres.genre_id WHERE novel_genres.novel_id = ?",
                        (selected_data[0],))
                    genres = [row[0] for row in cursor.fetchall()]

                    cursor.execute(
                        "SELECT tag_name FROM tags JOIN novel_tags ON tags.tag_id = novel_tags.tag_id WHERE novel_tags.novel_id = ?",
                        (selected_data[0],))
                    tags = [row[0] for row in cursor.fetchall()]

                    cursor.close()

                    open_novel_window(novel_title, novel_image_url, novel_description, novel_other_names, novel_type, genres,
                                    tags, novel_language, novel_artist, novel_year, novel_original_chapters,
                                    Novel_license_status, Novel_finished_translation, Novel_original_publisher,
                                    Novel_release_frequency)



    def open_novel_window(novel_title, novel_image_url, novel_description, novel_other_names, novel_type, genres, tags,
                        novel_language, novel_artist, novel_year, novel_original_chapters, Novel_license_status,
                        Novel_finished_translation, Novel_original_publisher, Novel_release_frequency):
        global search_as_you_type
        novel_window = Toplevel(window)
        novel_window.title(novel_title)
        novel_window.geometry("800x600")

        canvas = Canvas(novel_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(novel_window, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        response = requests.get(novel_image_url)
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        image = image.resize((200, 200)) 
        image_tk = ImageTk.PhotoImage(image)

        novel_image_label = Label(content_frame, image=image_tk)
        novel_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        novel_title_value_label = Label(content_frame, text=novel_title, font=("Arial", 18), wraplength=500,
                                        justify="left")
        novel_title_value_label.grid(row=0, column=1, padx=10, pady=10)

        tags_genres_frame = Frame(content_frame)
        tags_genres_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

        genre_label = Label(tags_genres_frame, text="Genres:", font=("Arial", 12))
        genre_label.grid(row=1, column=0, padx=10, pady=(0, 2), sticky="w")

        genre_value_label = Label(tags_genres_frame, text=", ".join(genres), font=("Arial", 12), wraplength=200,
                                justify="left")
        genre_value_label.grid(row=2, column=0, padx=10, pady=(0, 2), sticky="w")

        tags_label = Label(tags_genres_frame, text="Tags:", font=("Arial", 12))
        tags_label.grid(row=3, column=0, padx=10, pady=(0, 2), sticky="w")

        tags_value_label = Label(tags_genres_frame, text=", ".join(tags), font=("Arial", 12), wraplength=200,
                                justify="left")
        tags_value_label.grid(row=4, column=0, padx=10, pady=(0, 2), sticky="w")
        
        connection = sqlite3.connect('novel_database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT novel_link FROM novels WHERE novel_title = ?", (novel_title,))
        url = cursor.fetchall()

        connection.close()

        def update_novel():
            ip.insert(url[0][0])

        update_button = Button(tags_genres_frame, text="Update", command=update_novel)
        update_button.grid(row=0, column=0)

        novel_details_frame = Frame(content_frame)
        novel_details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

        detail_label = Label(novel_details_frame, text="Description:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_description, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Other Names:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_other_names, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Novel Type:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_type, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Language:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_language, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Artist:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_artist, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Year:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_year, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Original Chapters:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=novel_original_chapters, font=("Arial", 12),
                                wraplength=500, justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="License Status:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=Novel_license_status, font=("Arial", 12), wraplength=500,
                                justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Finished Translation:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=Novel_finished_translation, font=("Arial", 12),
                                wraplength=500, justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Original Publisher:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=Novel_original_publisher, font=("Arial", 12),
                                wraplength=500, justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        detail_label = Label(novel_details_frame, text="Release Frequency:", font=("Arial", 12))
        detail_label.pack(anchor="w")

        detail_value_label = Label(novel_details_frame, text=Novel_release_frequency, font=("Arial", 12),
                                wraplength=500, justify="left")
        detail_value_label.pack(anchor="w", padx=10, pady=2)

        novel_image_label.image = image_tk

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        novel_window.bind("<MouseWheel>", on_mousewheel)

        chapters_frame = Frame(content_frame)
        chapters_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        chapters_label = Label(chapters_frame, text="Chapters:", font=("Arial", 12))
        chapters_label.pack(anchor="w")

        chapters_scrollbar = Scrollbar(chapters_frame, orient=VERTICAL)
        chapters_scrollbar.pack(side="right", fill="y")

        chapters_listbox = Listbox(chapters_frame, font=("Arial", 12), yscrollcommand=chapters_scrollbar.set)
        chapters_listbox.pack(side="left", fill="both", expand=True)

        chapters_scrollbar.config(command=chapters_listbox.yview)

        connection = sqlite3.connect('novel_database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT novel_id FROM novels WHERE novel_title = ?", (novel_title,))
        novel_id = cursor.fetchone()[0]

        cursor.execute("SELECT chapter_name, chapter_url FROM chapters WHERE novel_id = ?", (novel_id,))
        chapters = cursor.fetchall()
        connection.close()

        for chapter in chapters:
            chapter_name = chapter[0]
            chapter_url = chapter[1]
            chapters_listbox.insert(END, chapter_name)

        def open_chapter(chapter_url):
            webbrowser.open(chapter_url)

        for i, chapter in enumerate(chapters):
            chapter_name = chapter[0]
            chapter_url = chapter[1]
            chapters_listbox.itemconfig(i, foreground="blue")
            chapters_listbox.bind("<Button-1>", lambda e, chapter_url=chapter_url: open_chapter(chapter_url))



        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))



    def search_execute(event):
        search_update(event) 


    def search_update(event):
        search_text = search_entry.get().strip().lower()
        filtered_data = [item for item in data if search_text in item[1].lower()]
        clear_listbox()
        for item in filtered_data:
            listbox.insert(END, item[1])

    global search_as_you_type
    search_as_you_type = False
    
    def toggle_search_mode():
        global search_as_you_type
        if search_as_you_type:
            search_toggle_button.configure(text="Search (Enter)")
            search_entry.unbind("<KeyRelease>")
            search_entry.unbind("<Return>")
            search_entry.bind("<Return>", search_update) 
        else:
            search_toggle_button.configure(text="Search (Type)")
            search_entry.bind("<KeyRelease>", search_update)
            search_entry.unbind("<Return>")  
        search_as_you_type = not search_as_you_type

    search_toggle_button = Button(button_frame, text="Search (Enter)", command=toggle_search_mode)
    search_toggle_button.pack(side="left", padx=5)

    search_entry.bind("<Return>", search_update)

    populate_listbox()

    listbox.bind("<Double-Button-1>", show_novel_window)

    window.mainloop()
