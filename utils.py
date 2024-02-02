import os
import zipfile
import shutil
import urllib.request
import gdown
import subprocess
from pytube import YouTube
from pydub import AudioSegment
def convert_to_wav(old_path):
    new_path = old_path.replace('mp3','wav')
    audio = AudioSegment.from_mp3(old_path)
    audio.export(new_path, format="wav")
    return new_path
def get_video_length(video_url):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the duration in seconds
        duration_seconds = yt.length
        
        return duration_seconds

    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_zip(extraction_folder, zip_name):
    os.makedirs(extraction_folder)
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(extraction_folder)
    os.remove(zip_name)

    index_filepath, model_filepath = None, None
    for root, dirs, files in os.walk(extraction_folder):
        for name in files:
            if name.endswith('.index') and os.stat(os.path.join(root, name)).st_size > 1024 * 100:
                index_filepath = os.path.join(root, name)

            if name.endswith('.pth') and os.stat(os.path.join(root, name)).st_size > 1024 * 1024 * 40:
                model_filepath = os.path.join(root, name)

    if not model_filepath:
        raise Exception(f'No .pth model file was found in the extracted zip. Please check {extraction_folder}.')

    # move model and index file to extraction folder
    os.rename(model_filepath, os.path.join(extraction_folder, os.path.basename(model_filepath)))
    if index_filepath:
        os.rename(index_filepath, os.path.join(extraction_folder, os.path.basename(index_filepath)))

    # remove any unnecessary nested folders
    for filepath in os.listdir(extraction_folder):
        if os.path.isdir(os.path.join(extraction_folder, filepath)):
            shutil.rmtree(os.path.join(extraction_folder, filepath))

def download_online_model(url, dir_name='custom'):
    try:
        print(f'[~] Downloading voice model with name {dir_name}...')
        zip_name = url.split('/')[-1]
        extraction_folder = os.path.join('rvc_models', dir_name)
        if os.path.exists(extraction_folder):
            shutil.rmtree(extraction_folder)

        if 'pixeldrain.com' in url:
            url = f'https://pixeldrain.com/api/file/{zip_name}'

        urllib.request.urlretrieve(url, zip_name)

        print('[~] Extracting zip...')
        extract_zip(extraction_folder, zip_name)
        print(f'[+] {dir_name} Model successfully downloaded!')

    except Exception as e:
        raise Exception(str(e))

def generate_ai_cover(SONG_INPUT,RVC_DIRNAME):
    PITCH_CHANGE = 0 
    PITCH_CHANGE_ALL = 0 
    INDEX_RATE = 0.5 
    FILTER_RADIUS = 3 
    PITCH_DETECTION_ALGO = "rmvpe" 
    CREPE_HOP_LENGTH = 128 
    PROTECT = 0.33 
    REMIX_MIX_RATE = 0.25  
    MAIN_VOL = 10 
    BACKUP_VOL = 0 
    INST_VOL = 0 
    REVERB_SIZE = 0.15 
    REVERB_WETNESS = 0.2 
    REVERB_DRYNESS = 0.8 
    REVERB_DAMPING = 0.7 
    OUTPUT_FORMAT = "mp3" 

    command = [
        "python",
        "src/main.py",
        "-i", SONG_INPUT,
        "-dir", RVC_DIRNAME,
        "-p", str(PITCH_CHANGE),
        "-k",
        "-ir", str(INDEX_RATE),
        "-fr", str(FILTER_RADIUS),
        "-rms", str(REMIX_MIX_RATE),
        "-palgo", PITCH_DETECTION_ALGO,
        "-hop", str(CREPE_HOP_LENGTH),
        "-pro", str(PROTECT),
        "-mv", str(MAIN_VOL),
        "-bv", str(BACKUP_VOL),
        "-iv", str(INST_VOL),
        "-pall", str(PITCH_CHANGE_ALL),
        "-rsize", str(REVERB_SIZE),
        "-rwet", str(REVERB_WETNESS),
        "-rdry", str(REVERB_DRYNESS),
        "-rdamp", str(REVERB_DAMPING),
        "-oformat", OUTPUT_FORMAT
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line, end='')
    process.wait()

def move_model(destination_dir):
    file_extension = ".pt"
    # List files in the directory
    files = os.listdir(destination_dir)
    # Check if any file with the desired extension exists
    file_exists = any(file.endswith(file_extension) for file in files)

    if file_exists:
        print(f"A file with the {file_extension} extension exists in the directory.")
    else:
        all_items = os.listdir(destination_dir)
        # Filter for subdirectories (folders)
        subfolders = [item for item in all_items if os.path.isdir(os.path.join(destination_dir, item))]

        source_dir = os.path.join(destination_dir,subfolders[0])
        # Ensure that the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # List files in the source directory
        files = os.listdir(source_dir)

        # Iterate through the files and move the ones ending with ".pth"
        for file in files:
            if file.endswith(".pth"):
                source_file = os.path.join(source_dir, file)
                destination_file = os.path.join(destination_dir, file)
                shutil.move(source_file, destination_file)
                print(f"Moved {file} to {destination_dir}")
        for file in files:
            if file.endswith(".index"):
                source_file = os.path.join(source_dir, file)
                destination_file = os.path.join(destination_dir, file)
                shutil.move(source_file, destination_file)
                print(f"Moved {file} to {destination_dir}")

