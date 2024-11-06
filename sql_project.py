import os
import mysql.connector
import pygame.mixer as mixer
from tkinter import *
from tkinter import filedialog

# Initialize the pygame mixer
mixer.init()

# Database connection
def create_database():
    conn = mysql.connector.connect(
        host="localhost",        # MySQL host
        user="root",             # MySQL username
        password="@Smg550fy" # MySQL password
    )
    cursor = conn.cursor()

    # Create the database and table
    cursor.execute("CREATE DATABASE IF NOT EXISTS music_player")
    cursor.execute("USE music_player")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        path VARCHAR(255) NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Function to insert a song into the database
def insert_song(name, path):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Smg550fy",
        database="music_player"
    )
    cursor = conn.cursor()

    cursor.execute("INSERT INTO songs (name, path) VALUES (%s, %s)", (name, path))

    conn.commit()
    conn.close()

# Function to load songs from the database into the Listbox
def load_from_db(listbox):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Smg550fy",
        database="music_player"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM songs')
    songs = cursor.fetchall()
    for song in songs:
        listbox.insert(END, song[0])  # Display song names in the Listbox
    conn.close()

# Function to load songs from a directory and save them to the database
def load(listbox):
    directory = filedialog.askdirectory(title='Open a songs directory')
    if directory:
        os.chdir(directory)
        tracks = os.listdir()

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@Smg550fy",
            database="music_player"
        )
        cursor = conn.cursor()

        for track in tracks:
            if track.endswith(".mp3"):  # Only add .mp3 files
                cursor.execute('SELECT * FROM songs WHERE name=? AND path=?', (track, directory))
                result = cursor.fetchone()
                if not result:
                    cursor.execute('INSERT INTO songs (name, path) VALUES (%s, %s)', (track, directory))
                    listbox.insert(END, track)  # Add the song to the Listbox

        conn.commit()
        conn.close()

# Function to play the selected song
def play_song(song_name: StringVar, songs_list: Listbox, status: StringVar):
    song_name.set(songs_list.get(ACTIVE))
    song = songs_list.get(ACTIVE)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Smg550fy",
        database="music_player"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT path FROM songs WHERE name=%s', (song,))
    result = cursor.fetchone()

    if result:
        song_path = result[0] + '/' + song
        mixer.music.load(song_path)
        mixer.music.play()
        status.set("Song PLAYING")
    conn.close()

# Function to stop the song
def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Song STOPPED")

# Function to pause the song
def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Song PAUSED")

# Function to resume the song
def resume_song(status: StringVar):
    mixer.music.unpause()
    status.set("Song RESUMED")

# Create the database and the songs table if they don't exist
create_database()

# Tkinter GUI setup
root = Tk()
root.geometry('700x220')
root.title('Vansh Music Player')
root.resizable(0, 0)

song_frame = LabelFrame(root, text='Current Song', bg='black', width=400, height=80)
song_frame.place(x=0, y=0)

button_frame = LabelFrame(root, text='Control Buttons', bg='black', width=400, height=120)
button_frame.place(y=80)

listbox_frame = LabelFrame(root, text='Playlist', bg='black')
listbox_frame.place(x=400, y=0, height=200, width=300)

current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='Gold')
playlist.pack(fill=BOTH, padx=5, pady=5)

# Load songs from the database into the playlist when the program starts
load_from_db(playlist)

Label(song_frame, text='CURRENTLY PLAYING:', bg='Red', font=('Times', 10, 'bold')).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, bg='Goldenrod', font=("Times", 12), width=25)
song_lbl.place(x=150, y=20)

pause_btn = Button(button_frame, text='Pause', bg='yellow', font=("Georgia", 13), width=7,
                    command=lambda: pause_song(song_status))
pause_btn.place(x=15, y=10)

stop_btn = Button(button_frame, text='Stop', bg='red', font=("Georgia", 13), width=7,
                  command=lambda: stop_song(song_status))
stop_btn.place(x=105, y=10)

play_btn = Button(button_frame, text='Play', bg='green', font=("Georgia", 13), width=7,
                  command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=10)

resume_btn = Button(button_frame, text='Resume', bg='Orange', font=("Georgia", 13), width=7,
                    command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=10)

load_btn = Button(button_frame, text='Load Directory', bg='hotpink', font=("Georgia", 13), width=35,
                  command=lambda: load(playlist))
load_btn.place(x=10, y=55)

root.update()
root.mainloop()


