import pygame
import sys

from genre import Genre
from playlist import PlayList
from song import Song

global current_user
MEDIA_DIR = "./media/"

songs = [Song("circles", "3:35", "2019-08-30", Genre.POP),
         Song("birds_of_a_feather", "4:14", "2021-11-19", Genre.POP),
         Song("juna", "3:25", "2000-01-01", Genre.OTHER),
         Song("wet_dream", "2:33", "2000-01-01", Genre.ROCK),
         Song("heavy", "4:13", "2000-01-01", Genre.OTHER)]

def reproduce_song(song):
    # Inicializar el mixer
    pygame.mixer.init()

    # Cargar canción
    pygame.mixer.music.load(MEDIA_DIR + song + ".mp3")

    # Reproducir
    pygame.mixer.music.play()

    print(f"Reproduciendo {song}... ")
    while True:
        comando = input("Pulsa (pausa, reanudar, stop, salir): ").strip().lower()

        if comando == "pausa":
            pygame.mixer.music.pause()
        elif comando == "reanudar":
            pygame.mixer.music.unpause()
        elif comando == "stop":
            pygame.mixer.music.stop()
        elif comando == "salir":
            pygame.mixer.music.stop()
            break
        else:
            print("Comando no válido")

def reproduce_playList(name):
    pygame.mixer.init()

    current_playlist_songs = []
    for playlist in current_user.playlists:
        if playlist.name == name:
            current_playlist_songs = playlist.songs

    if not current_playlist_songs:
        print("La playlist no existe o está vacía.")
        return

    index = 0
    print("################################################")
    print("Songs in the playlist:")
    for song in current_playlist_songs:
        print(f"- {song.name:<35} - {song.duration}")
    print("################################################")

    def play_song(i):
        pygame.mixer.music.load(MEDIA_DIR + current_playlist_songs[i].name + ".mp3")
        pygame.mixer.music.play()
        print(f"Reproduciendo {current_playlist_songs[i].name}...")

    play_song(index)

    while True:
        comando = input("Pulsa (siguiente, pausa, reanudar, stop, salir): ").strip().lower()

        if comando == "siguiente":
            index = (index + 1) % len(current_playlist_songs)  # ciclo por la playlist
            play_song(index)
        elif comando == "pausa":
            pygame.mixer.music.pause()
        elif comando == "reanudar":
            pygame.mixer.music.unpause()
        elif comando == "stop":
            pygame.mixer.music.stop()
        elif comando == "salir":
            pygame.mixer.music.stop()
            break
        else:
            print("Comando no válido")


def login():
    from login import Login
    print_logo()
    global current_user
    login = Login()
    login.load_users()

    while True:
        print("\t\t\t\t1. Login\t\t\t\t2. Create User")
        print("\t\t\t\t\t\t     0. Salir")
        print("\n**********************************************************************")

        choice = input("Elige una opción: ")

        if choice == '1':
            if login.is_login_correct():
                current_user = login.get_current_user()
                return True
        elif choice == '2':
            login.create_new_user()
        elif choice == '3':
            print("Saliendo de la aplicación.")
            return False
        else:
            print("Opción no válida. Inténtalo de nuevo.")


def menu():
    while True:
        print_logo()

        print("\t1. Reproducir PlayList\t\t\t2. Reproducir Canción")
        print("\t3. Crear Playlist\t\t\t\t4. Tu Wrapped")
        print("\t\t\t\t\t\t  0. Salir")
        print("\n**********************************************************************")

        try:
            choice = int(input("Elige una opción: "))

            if choice == 1:
                for playlist in current_user.playlists:
                    print(f"- {playlist.name}")
                reproduce_playList(input("Ingresa el nombre de la playList: "))

            elif choice == 2:
                for song in songs:
                    print(f"- {song.name}")
                reproduce_song(input("Ingresa el nombre de la canción: "))

            elif choice == 3:
                playlist_name = input("Ingresa el nombre de la nueva playlist: ")
                new_playlist = current_user.create_playlist(playlist_name)
                while True:
                    for song in songs:
                        print(f"- {song.name}")
                    song_name = input("Ingresa el nombre de la canción a agregar (o 'salir' para terminar): ")
                    if song_name.lower() == 'salir':
                        break
                    song_found = False
                    for song in songs:
                        if song.name == song_name:
                            new_playlist.add_song(song)
                            song_found = True
                            break
                    if not song_found:
                        raise NameError("La canción no existe en la base de datos.")
                new_playlist.save_to_file()

            elif choice == 4:
                print("TODO: Wrapped")
                # Tu Wrapped
                # Aquí puedes implementar la funcionalidad de Wrapped
                # Debe de aparecer: Tu usuario,
                # cuantas playlist tienes,
                # tu canción mas usada en distintas plalylist,
                # tu género más escuchado,
                # Artista favorito
            elif choice == 0:
                print("Adiós!")
                sys.exit(0)
            else:
                print("[ERROR] Tu opción es incorrecta. ¡Intenta de nuevo!")
        except ValueError:
            print("[ERROR] Debes escribir un número válido!")
        except Exception as e:
            print(f"[ERROR] {e}")

def print_logo():
    print("**********************************************************************")
    print("*                                                                    *")
    print("*                             SPOTIFY                                *")
    print("*                                                                    *")
    print("**********************************************************************\n")

if __name__ == "__main__":
    while not login():
        pass
    menu()