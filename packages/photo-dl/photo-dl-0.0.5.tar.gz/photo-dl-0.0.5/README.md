# photo-dl

photo-dl is a command-line downloader which helps to crawl photo albums from [Supported sites](#supported-sites)



## Installation

#### Dependencies

- python >= 3.4
- requests >= 2.12.0
- lxml >= 3.7.0

#### Install via Pip

$ pip install --upgrade photo-dl

#### Install from source

$ git clone https://github.com/windrises/photo-dl

$ cd photo-dl

$ python setup.py install



## Usage

assign a url or .txt file which one url one line

$ photo-get  url

$ photo-get xxx.txt

#### Examples

$ photo-get  https://www.meituri.com/t/1820/

$ photo-get urls.txt



## Supported sites

Temporarily only supports one website

| site                     | example                         |
| :----------------------- | :------------------------------ |
| https://www.meituri.com/ | https://www.meituri.com/t/1820/ |
|                          | https://www.meituri.com/a/7893/ |