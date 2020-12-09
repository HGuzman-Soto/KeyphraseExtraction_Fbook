# Modified heavily for specific use from https://github.com/apurvmishra99/facebook-scraper-selenium

# Facebook Scraper Selenium

Scrape Facebook Public Posts without using Facebook API

## What It can Do

- Scrape Public Post Text

  - Raw Text

- Scrape Public Post Comments

## Install Requirements

Please make sure chrome is installed and `chromedriver` is placed in the same directory as the file

Find out which version of `chromedriver` you need to download in this link [Chrome Web Driver](http://chromedriver.chromium.org/downloads).

Place your Facebook login in info into `facebook_credentials.txt`

```sh
pip install -r requirements.txt
```

## Usage

#### Use scraper.py to print to screen or to file

```
usage: scraper.py [-h] -page PAGE -len LEN [-infinite INFINITE] [-usage USAGE]
                  [-comments COMMENTS]

Facebook Page Scraper

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -page PAGE, -p PAGE   The Facebook Public Page you want to scrape
  -len LEN, -l LEN      Number of Posts you want to scrape

optional arguments:
  -infinite INFINITE, -i INFINITE
                        Scroll until the end of the page (1 = infinite)
                        (Default is 0)
  -usage USAGE, -u USAGE
                        What to do with the data: Print on Screen (PS), Write
                        to Text File (WT) (Default is WT)
  -comments COMMENTS, -c COMMENTS
                        Scrape ALL Comments of Posts (y/n) (Default is n).
                        When enabled for pages where there are a lot of
                        comments it can take a while

```

Return value

```python
[
{'Post': 'Text text text text text....',
 'Link' : 'https://link.com',
 'Image' : 'https://image.com',
 'Comments': {
        'name1' : {
            'text' : 'Text text...',
            'link' : 'https://link.com',
            'image': 'https://image.com'
         }
        'name2' : {
            ...
            }
         ...
         },
 'Reaction' : { # Reaction only contains the top3 reactions
        'LIKE' : int(number_of_likes),
        'HAHA' : int(number_of_haha),
        'WOW'  : int(number_of_wow)
         }}
  ...
]
```
