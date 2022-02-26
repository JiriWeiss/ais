import asyncio
from encodings import utf_8
from bs4 import BeautifulSoup
import pyppeteer
import os
import json
import pandas as pd
from pathlib import Path
import re
import urllib.request


    

async def main():
    
    with open("outputs/Names.json", "r") as f:
        urls = json.load(f)
    
    print(urls)
    
    



asyncio.get_event_loop().run_until_complete(main())