from re import match
from sys import exit
from datetime import datetime
from random import choice
import csv


def main():
    """creates list 'music' at the begginign each time,
    what allows to have updated list for working actions in case,
    when last action was adding new album."""
    music = create_music_list()
    info()
    choosen_action = choosing_action()
    if choosen_action == "1":
        add_new_album()
    elif choosen_action == "2":
        artist = input("\nSearched artist: ").lower()
        find_albums_by_artist(artist, music)
    elif choosen_action == "3":
        year = input("\nSearched year: ")
        while not match("^[1-2][0-9]{3}$", year):
            print("\nWrong input.")
            year = input("\nSearched year: ")
        year = int(year)
        find_albums_by_year(year, music)
    elif choosen_action == "4":
        album = input("\nSearched album: ").lower()
        find_artist_by_album(album, music)
    elif choosen_action == "5":
        letters = input("\nSearch for: ").lower()
        find_albums_by_letters(letters, music)
    elif choosen_action == "6":
        genre = input("\nSearched genre: ").lower()
        find_albums_by_genre(genre, music)
    elif choosen_action == "7":
        calculate_albums_age(music)
    elif choosen_action == "8":
        genre = input("\nSearched genre: ").lower()
        random_album_by_genre(genre, music)
    elif choosen_action == "9":
        artist = input("\nSearched artist: ").lower()
        amount_of_albums_by_artist(artist, music)
    elif choosen_action == "10":
        the_longest_album(music)
    else:
        exit()
    answer = continue_or_exit()
    if answer == "yes":
        main()
    else:
        exit()


def create_music_list():
    """Creates list in specified format"""
    music = open("music_collector.csv", "r")
    music_reader = csv.reader(music, delimiter="|")
    music_data = list(music_reader)
    music_list = []
    for data in music_data:
        name_tupple = (data[0][0:-1], data[1][1:-1])
        info_tupple = (int(data[2]), data[3][1:-1], data[4][1:])
        music_list.append((name_tupple, info_tupple))
    music.close()
    return music_list


def info():
    print("""\nWelcome in the CoolMusic! Choose the action:\n
         1) Add new album
         2) Find albums by artist
         3) Find albums by year
         4) Find musician by album
         5) Find albums by letter(s)
         6) Find albums by genre
         7) Calculate the age of all albums
         8) Choose a random album by genre
         9) Show the amount of albums by an artist
        10) Find the longest-time album
         0) Exit\n""")


def choosing_action():
    """Validates choosen action"""
    choosen_action = input("\nChoose action number: ")
    while not match("^[0-9]$|^10$|^exit$", choosen_action):
        print("\nWrong input. Choose number between 0 and 10")
        choosen_action = input("\nChoose action number: ")
    return choosen_action


def add_new_album():
    """Takes input about new album. Validates input where needed.
    Writes given data to csv file."""
    print("\nADDING NEW ALBUM")
    artist_name = input("\nArtist name: ")
    album_name = input("\nAlbum name: ")
    year_of_release = input("\nYear of release: ")
    while not match("^[1-2][0-9]{3}$", year_of_release):
        print("\nWrong input.")
        year_of_release = input("\nYear of release: ")
    genre = input("\nGenre: ")
    length = input("\nLength: ")
    while not match("^[0-9]{2,3}:[0-5][0-9]$", length):
        print("\nWrong input. Proper format is: \"mm:ss\"")
        length = input("\nLengh: ")
    music = open("music_collector.csv", "a")
    music_writer = csv.writer(music, delimiter="|")
    music_writer.writerow([artist_name + " ",
                           " " + album_name + " ",
                           " " + year_of_release + " ",
                           " " + genre + " ",
                           " " + length])
    music.close()
    print("\n\n{} {} added.\n".format(artist_name, album_name))


def find_albums_by_letters(letters, music):
    found = False
    for album in music:
        lowered = album[0][1].lower()
        if lowered.find(letters) != -1:
            print(album[0])
            found = True
    if found is False:
        print("\nNOTHING FOUND")


def find_artist_by_album(album_name, music):
    found = False
    for album in music:
        if album[0][1].lower() == album_name:
            print(album[0])
            found = True
            break
    if found is False:
        print("\nNOTHING FOUND")


def find_albums_by_artist(artist, music):
    found = False
    for album in music:
        if album[0][0].lower() == artist:
            print(album[0])
            found = True
    if found is False:
        print("\nNOTHING FOUND")


def find_albums_by_year(year, music):
    found = False
    for album in music:
        if album[1][0] == year:
            print(album[0])
            found = True
    if found is False:
        print("\nNOTHING FOUND")


def find_albums_by_genre(genre, music):
    found = False
    for album in music:
        if album[1][1] == genre:
            print(album[0])
            found = True
    if found is False:
        print("\nNOTHING FOUND")


def calculate_albums_age(music):
    for album in music:
        age = datetime.now().year - album[1][0]
        print("\n{}\nAge: {} years".format(album[0], age))


def random_album_by_genre(genre, music):
    possible_albums = []
    for album in music:
        if album[1][1] == genre:
            possible_albums.append(album[0])
    if possible_albums != []:
        print(choice(possible_albums))
    else:
        print("\nNOTHING FOUND")


def amount_of_albums_by_artist(artist, music):
    amount = 0
    for album in music:
        if album[0][0].lower() == artist:
            amount += 1
    print("\nThere is/are {} album(s) by {}".format(amount, artist.upper()))


def the_longest_album(music):
    maximum = 0
    for album in music:
        lenght = int("".join(album[1][2].split(":")))
        if lenght > maximum:
            maximum = lenght
            data = album
    print("\nThe longest album is: {}, it's {} m".format(data[0], data[1][2]))


def continue_or_exit():
    """Validation for exiting or continue working"""
    answer = input("\nAnother operation ?\nType \"yes\" or \"no\": ").lower()
    while not match("^yes$|^no$", answer):
        answer = input("\nWrong input. \nType \"yes\" or \"no\": ").lower()
    return answer


main()
