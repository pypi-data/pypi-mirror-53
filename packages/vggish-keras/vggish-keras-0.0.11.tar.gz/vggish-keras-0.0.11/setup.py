''''''
import os
import sys
import setuptools

import gzip
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

DRIVE_URL = 'https://docs.google.com/uc?export=download&id={id}'

FILES = [
    # Weights from DTao
    # ('vggish_keras/model/audioset_top.h5',
    #  DRIVE_URL.format(id='1mhqXZ8CANgHyepum7N4yrjiyIg6qaMe6')),
    #
    # ('vggish_keras/model/audioset_no_top.h5',
    #  DRIVE_URL.format(id='16JrWEedwaZFVZYvn1woPKCuWx85Ghzkp')),
    #
    # ('vggish_keras/model/audioset_pca_params.npz',
    #  'https://storage.googleapis.com/audioset/vggish_pca_params.npz'),

    # merged weights
    ('vggish_keras/model/audioset_weights.h5',
     DRIVE_URL.format(id='1qhpbp5OPqNIXpDYdxqEM-yzKi43OSNP2'))
]

def download_file(path, url=None, decompress=True):
    if not os.path.isfile(path):
        if url:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print('Downloading file {} from {} ...'.format(path, url))

            if decompress:
                tar_path = path + '.gz'
                urlretrieve(url, tar_path)

                print('Decompressing {} to {} ...'.format(tar_path, path))
                with gzip.open(tar_path, 'rb') as source:
                    with open(path, 'wb') as target:
                        target.write(source.read())

                print('Removing {}...'.format(tar_path))
                os.remove(tar_path)

            else:
                urlretrieve(url, tar_path)

            print('Done. {} exists? {}'.format(path, os.path.isfile(path)))
            return path
        print('Could not download {}. No url provided.'.format(path))
    print('File {} already exists.')
    return path

if len(sys.argv) > 1 and sys.argv[1] == 'sdist':
    # exclude the weight files in sdist
    weight_files = []
else:
    weight_files = [download_file(os.path.abspath(f), url) for f, url in FILES]
    print(weight_files)

setuptools.setup(
    name='vggish-keras',
    version='0.0.11',
    description='VGGish in Keras.',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.md')
    ).read().strip(),
    long_description_content_type='text/markdown',
    author='Bea Steers',
    author_email='bea.steers@gmail.com',
    url='https://github.com/beasteers/VGGish',
    packages=setuptools.find_packages(),
    package_data={'vggish_keras': weight_files},
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        'numpy',
        'tensorflow',
        'pumpp',
    ],
    license='MIT License',
    zip_safe=False,
    keywords='vggish audio audioset keras tensorflow')
