import os
import requests
import logging
from pathlib import Path

from tqdm import tqdm

logging.captureWarnings(True)


class ImageOptimCompression(object):

    input_path = input('What is the Directory Path?')

    def __init__(self):
        self.username = 'svkzzxkccz'
        self.quality = 'full'
        self.endpoint = 'https://im2.io'

        self.output_dir = ''
        self.raw_image_dir = ''

    def build_url(self):
        url_parts = [
            self.endpoint,
            self.username,
            self.quality
        ]
        url = '/'.join(url_parts)
        return url

    def create_dirs(self):
        os.rename(f'{Path(self.input_path).joinpath("images")}', f'{Path(self.input_path).joinpath("non_compressed")}')

        os.makedirs(Path(self.input_path).joinpath('images'), exist_ok=True)
        self.output_dir = Path(self.input_path).joinpath('images')
        self.raw_image_dir = Path(self.input_path).joinpath('non_compressed')
        return

    def request(self, url):
        os.chdir(self.raw_image_dir)
        image_dir_size = []
        for item in tqdm(os.listdir(self.raw_image_dir)):
            image_dir_size.append(os.stat(item).st_size >> 10)
            name = item.split('.', 1)[0]
            extension = item.split('.', 1)[1]
            files = {'upload_file': open(item, 'rb')}
            r = requests.post(str(url), files=files, stream=True)
            image = str(name) + '.' + extension

            with open(Path(self.output_dir).joinpath(image), 'wb') as fd:
                for chunk in r.iter_content(chunk_size=1048):
                    fd.write(chunk)

        # GET INPUT/OUTPUT DIRECTORY SIZES
        compressed_dir_size = []
        os.chdir(self.output_dir)
        for i in os.listdir(self.output_dir):
            compressed_dir_size.append(os.stat(i).st_size >> 10)

        print('non_compressed directory =', str(sum(image_dir_size)) + 'kb')
        print('images directory =', str(sum(compressed_dir_size)) + 'kb')


if __name__ == '__main__':
    worker = ImageOptimCompression()
    worker.__init__()
    worker.build_url()
    worker.create_dirs()
    worker.request(worker.build_url())
