# eodhistoricaldata-dl

Tool for downloading data from [eodhistoricaldata.com](eodhistoricaldata.com).

## Installation

First, clone this repository, and install its requirements.

```
git clone https://github.com/ngafar/eodhistoricaldata-dl.git
pip install -r requirements.txt
```

Next, get an API key from [eodhistoricaldata.com](eodhistoricaldata.com).

Finally, create a `.env` file, and add the following line:

```
API_KEY = "PASTE_YOUR_KEY_HERE"
```

## Caveats

This tool requires a paid subscription to [eodhistoricaldata.com](eodhistoricaldata.com).

Additionally, this tool will only retrieve stocks listed in the United States. 