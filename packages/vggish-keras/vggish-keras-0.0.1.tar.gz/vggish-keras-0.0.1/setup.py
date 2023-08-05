''''''
import os
import sys

import setuptools

import download

if len(sys.argv) > 1 and sys.argv[1] == 'sdist':
    # exclude the weight files in sdist
    weight_files = []
else:
    weight_files = [download.download_file(f, url) for f, url in download.FILES]


setuptools.setup(name='vggish-keras',
                 version='0.0.1',
                 description='VGGish in Keras.',
                 long_description=open(
                    os.path.join(os.path.dirname(__file__), 'README.md')
                ).read().strip(),
                 long_description_content_type='text/markdown',
                 author='Bea Steers',
                 author_email='bea.steers@gmail.com',
                 url='https://github.com/beasteers/VGGish',
                 packages=setuptools.find_packages(),
                 package_data={'vggish': weight_files},
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
                    'tensorflow<=1.14',
                    'pumpp',
                 ],
                 license='MIT License',
                 zip_safe=False,
                 keywords='vggish audio audioset keras tensorflow')
