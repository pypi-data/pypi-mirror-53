import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YahooFinanceDataLoader",
    version="0.1.0",
    
    author="Maverick",
    author_email="maverickjet@protonmail.com",
    
    description="Allows to download YahooFinance stock data to your local disk.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/alv2017/Python---YahooFinanceDataLoader",
    keywords='Yahoo Finance stock price csv',
    packages=setuptools.find_packages(),
    
    install_requires=['requests~=2.20.00'],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='~=3.6',
)