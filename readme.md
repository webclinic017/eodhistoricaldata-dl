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

## Usage

The program always defaults to picking up where it left off. As such, if there is already `tracker.csv` file the program will use it. If you would like the program to start from scratch, make sure that the output directory is empty. 

## Caveats

You will need a paid subscription to [eodhistoricaldata.com](eodhistoricaldata.com).

Additionally, this tool will only retrieve stocks listed in the United States. 