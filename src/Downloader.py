from pytube import YouTube
import os
import time

path = "/Users/jvale03/Documents" # update your path 

def download_audio(url,output_path=""):
    try:
        # Creates YouTube object
        youtube = YouTube(url)
        
        # Select the audio stream
        audio_stream = youtube.streams.filter(only_audio=True).first()
        
        # Verificy if it youtube video exists
        if not audio_stream:
            print("\033[31mNo audio streams found\033[m")
            return
        
        # Define output path
        output_path = audio_stream.download(output_path=output_path)
        
        # Rename youtube audios to have extension .mp3
        base, ext = os.path.splitext(output_path)
        new_file = base + '.mp3'
        os.rename(output_path, new_file)
        
        audio_name = output_path.split("/")
        print(f"\033[1mDownloaded:\033[m {audio_name[-1]}")
        
    except Exception as e:
        print(f"\033[31mError downloading audio: {e}\033[m")


def download_list(output_path,file="audio_list.txt"):
    # open file with audios list
    with open(file,"r") as f:
        content = f.readlines()

    print("---------------")
    print(f"\033[32mDownload started...\033[m\n")
    
    # download each audio of the file
    for audio in content:
        download_audio(audio,output_path)

    print(f"\033[32m\nDownload completed!\033[m")

# method to define the path to save the audios
def defining_path():
    paths_list = []
    i=0
    print("\033[1mPaths: \033[m")

    for dir_path in os.listdir(path):
        dir_path = os.path.join(path,dir_path)
        paths_list.append(dir_path)
        print(f" {i}: {paths_list[i]}")
        i+=1

    while True:
        choice = input("\nChoose your path to save the audios: ")
        if choice.isdigit():
            choice = int(choice)
            if choice > i or choice < 0:
                print("\033[31mInvalid!\033[m")
            else:
                break
        else:
            print("\033[31mInvalid!\033[m")

    true_false = input(f"Are you sure you want to choose \033[1m'{paths_list[choice]}'\033[m? y/n: ")

    if true_false == "y" or true_false == "":
        initial_time = time.time()
        download_list(paths_list[choice])
        return time.time() - initial_time 
    
    return 0

def main():
    choice = 0
    while True:
        choice = input("1: Download one audio\n2: Download multiple audios\nInput: ")
        if choice.isdigit():
            choice = int(choice)
            if choice > 2 or choice < 1:
                print("\033[31mInvalid!\033[m")
            else:
                break
        else:
            print("\033[31mInvalid!\033[m")
    final_time = 0
    if choice == 1:
        print("---------------")
        url = input("Enter here your URL: ")
        print("---------------")
        initial_time = time.time()
        download_audio(url)
        final_time = time.time() - initial_time
        print("---------------")
        print(f"It took {round(final_time,1)} seconds!")
    elif choice == 2:
        print("---------------")
        final_time = defining_path()
        print("---------------")
        print(f"It took {round(final_time/60,2)} minutes!")

        

main()