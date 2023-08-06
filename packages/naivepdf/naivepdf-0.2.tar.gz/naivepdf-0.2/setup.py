from setuptools import setup

README = open('README.md', 'r').read()

setup(
    name='naivepdf',
    version='0.2',
    author='naivefeeling',
    author_email='625424539@qq.com',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=['naivepdf', 'naivepdf.decoder', 'naivepdf.encoding', 'naivepdf.utils'],
    package_data={'naivepdf': ['cmap/*/*', 'Adobe-Core35_AFMs-314/*']},
    description='yet another pdf texts and tables extractor',
    url='https://github.com/naivefeeling/naivepdf.git',  # use the URL to the github repo
    keywords=['pdf', 'pdfparser', 'pdfextract'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)
