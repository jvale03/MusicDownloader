from pytube import YouTube
import os
import time
import subprocess

input_command = None
output_command = None
bitrate = None
output_path = ""
path = "/Users/jvale03/Documents" # update your path 


def run_command():
        command = f'ffmpeg -i "{input_command}" -b:a {bitrate} "{output_command}"' # 64 96 128 192 320
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def sanitize_filename(filename):
    return filename.replace(" ", "_").replace("(", "").replace(")", "").replace("&", "and")


def download_audio(url, d_type):
    global input_command, output_path, output_command
    try:
        # Creates YouTube object
        youtube = YouTube(url)
        
        # Select the audio stream
        audio_stream = youtube.streams.filter(only_audio=True).first()
        
        # Verify if the YouTube video exists and has audio streams
        if not audio_stream:
            print("\033[31mNo audio streams found for this video\033[m")
            return
        
        # Define output path
        output_path = audio_stream.download(output_path=output_path)
        
        # Rename YouTube audios to have extension .mp3
        base, ext = os.path.splitext(output_path)
        new_file = base + '.mp3'
        os.rename(output_path, new_file)

        audio_name = new_file.split("/")

        if d_type != 0:
            input_command = new_file
            audio_name[-1] = sanitize_filename(audio_name[-1])
            output_command = "/".join(audio_name)
            try:
                run_command()
            except subprocess.CalledProcessError as e:
                print(f"\033[31mError executing command: {e.stderr.decode()}.\033[m")
                return

        print(f"\033[1mDownloaded:\033[m {audio_name[-1]}")

    except Exception as e:
        print(f"\033[31mError downloading audio:  {str(e)}\033[m")


def download_list(file="audio_list.txt"):
    # open file with audios list
    with open(file,"r") as f:
        content = f.readlines()

    print("---------------")
    print(f"\033[32mDownload started...\033[m\n")
    
    # download each audio of the file
    for audio in content:
        download_audio(audio,1)

    print(f"\033[32m\nDownload completed!\033[m")

# method to define the path to save the audios
def defining_path():
    global output_path
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
            if choice > i-1 or choice < 0:
                print("\033[31mInvalid!\033[m")
            else:
                break
        else:
            print("\033[31mInvalid!\033[m")

    true_false = input(f"Are you sure you want to choose \033[1m'{paths_list[choice]}'\033[m? y/n: ")

    if true_false == "y" or true_false == "":
        initial_time = time.time()
        output_path = paths_list[choice]
        download_list()
        return time.time() - initial_time 
    
    return 0

def defining_audio_quality():
    global bitrate
    choice = -1
    while True:
        choice = input("1: 320kbps (2,5MB/min)\n2: 192kbps (1,5MB/min)\n3: 128kbps (1MB/min)\n4: 96kbps (0,75MB/min)\n5: 64kbps (0,5MB/min)\n6: 32mbps (0,25MB/min)\n")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                bitrate = "320k"
                break
            elif choice == 2:
                bitrate = "192k"
                break
            elif choice == 3:
                bitrate = "128k"
                break
            elif choice == 4:
                bitrate = "96k"
                break
            elif choice == 5:
                bitrate = "64k"
                break
            elif choice == 6:
                bitrate = "32k"
                break

            else:
                print("\033[31mInvalid!\033[m")

        else:
            print("\033[31mInvalid!\033[m")


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
        download_audio(url,0)
        final_time = time.time() - initial_time
        print("---------------")
        print(f"It took {round(final_time,1)} seconds!")
    elif choice == 2:
        print("---------------")
        defining_audio_quality()
        print("---------------")
        final_time = defining_path()
        print("---------------")
        print(f"It took {round(final_time/60,2)} minutes!")

        

main()