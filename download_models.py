import os
import zipfile
import urllib.request
import progressbar

class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

BASE_DIR = os.getcwd()

def extract_zip(extraction_folder, zip_name):
    if not os.path.exists(extraction_folder):
        os.makedirs(extraction_folder)
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(extraction_folder)
    os.remove(zip_name)


def download_online_model(url):
        zip_name = url.split('/')[-1]

        if 'pixeldrain.com' in url:
            url = f'https://pixeldrain.com/api/file/{zip_name}'

        urllib.request.urlretrieve(url, zip_name)

        print('[~] Extracting zip...')
        extract_zip(BASE_DIR, zip_name,MyProgressBar())
        print('[+] Models successfully downloaded!')



url = 'https://pixeldrain.com/u/rwzXYbc6'
#download_online_model(url)

extract_zip(BASE_DIR, "D7r3MCDh")