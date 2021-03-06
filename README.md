# winning_links
a lightweight library that parses JSON logs from an online store and finds affiliate links that attracted customers

# Requirements
- Python 3.8.2

# Guide
## Setup
Windows:
``` shell script
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps winning-links
```

Linux:
``` shell script
pip install --index-url https://test.pypi.org/simple/ --no-deps winning-links
```

## Usage as a library
If you have logs in the form of
``` json
[
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-05-23T18:59:13.286000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/products/id?=10",
        "document.referer": "https://shop.com/",
        "date": "2018-05-23T18:59:20.119000Z"
    }
]
```
just import ```winning_links``` and use its ```find_winning_links``` function
``` python
from winning_links import import winning_links

with open('log.json') as log_fh:
    log_str = log_fh.read()
tuples = winning_links.find_winning_links(log_str, client_ids=True)
print(tuples)
```

If your logs have custom key names pass additional arguments ot the ```find_winning_links``` function
``` python
tuples = winning_links.find_winning_links(
    log_str,
    client_ids=True
    client_key='<CUSTOM_CLIENT_KEY>',
    location_key='<CUSTOM_LOCATION_KEY>',
    referer_key='<CUSTOM_REFERER_KEY>',
    date_key='<CUSTOM_DATE_KEY>',
)
```

If you only need links and don't need client IDs go for

``` python
tuples = winning_links.find_winning_links(log_str, client_ids=False)
```

# Usage as a script
You may also run ```winning_links``` as a that takes a JSON log file name as the first argument and an JSON output file name as the second argument 
``` shell script
python winning_links.py log.json outpus.json
```

# Demonstration on Windows
Create and activate a virtual environment so that you could clean everything up after the demonstration:
``` shell script
mkdir winning_links_demo && cd winning_links_demo
python -m venv env
env\Scripts\activate
```

Install the dateutil package:
```shell script
python -m pip install -U python-dateutil
```

Install the winning_inks package from Test PyPi:
``` shell script
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps winning-links
```

Create a sample JSON log:
``` json
# log.json
[
    {
    "client_id": "user7",
    "User-Agent": "Chrome 65",
    "document.location": "https://shop.com/",
    "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
    "date": "2018-05-23T18:59:13.286000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/products/id?=10",
        "document.referer": "https://shop.com/",
        "date": "2018-05-23T18:59:20.119000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/products/id?=25",
        "document.referer": "https://shop.com/products/id?=10",
        "date": "2018-05-23T19:04:20.119000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/cart",
        "document.referer": "https://shop.com/products/id?=25",
        "date": "2018-05-23T19:05:13.123000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://shop.com/cart",
        "date": "2018-05-23T19:05:59.224000Z"
    }
]
```

Run the script:
```shell script
python -m winning_links log.json output.json
```

View the just created output.json with the user and her link:
```shell script
notepad output.json
```
``` json
# output.json
[["user7", "https://referal.ours.com/?ref=0xc0ffee"]]
```

Do the clean-up:
``` shell script
deactivate
cd ..
rmdir/q/s winning_links_demo
```

# For Developers
Pass the --debug=DEBUG argument to the script for extensive logging:
``` shell script
python -m winning_links log.json output.json --debug=DEBUG
```