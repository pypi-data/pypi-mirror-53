''''''
import os
import sys
import setuptools

import tarfile
import requests

DRIVE_URL = 'https://drive.google.com/uc?id={id}&export=download'
DRIVE_CONFIRM_URL = 'https://drive.google.com/uc?id={id}&export=download&confirm={confirm}'

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
     '1QbMNrhu4RBUO6hIcpLqgeuVye51XyMKM')
]

def download_file(path, gdrive_id=None):
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print('Downloading file {} to {} ...'.format(gdrive_id, path))

        sess = requests.Session()
        r = sess.get(DRIVE_URL.format(id=gdrive_id))
        confirm = next(
            (v for k, v in r.cookies.get_dict().items()
             if 'download_warning_' in k), None)

        if confirm:
            print('Using confirmation code {}...'.format(confirm))
            r = sess.get(DRIVE_CONFIRM_URL.format(id=gdrive_id, confirm=confirm))

        print(r.headers)

        with open(path, 'wb') as f:
            f.write(r.content)

        print('Done. {} exists? {}'.format(path, os.path.isfile(path)))
        return path
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
    version='0.0.13',
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
