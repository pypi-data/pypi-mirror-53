from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pysimilarity',
    version='0.1.0',
    description='Determine similarity between datasets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JuanCorp/pysimilarity',
    author='JuanCorp',
    author_email='juan.nunez.corp@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='similarity data machine learning',
    packages=['pysimilarity'],
    python_requires='>=3, <4',
    install_requires=['pandas', 'numpy', 'scipy', 'scikit-learn']

)
