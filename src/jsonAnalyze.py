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
from sympy import *


width, height = 1440, 900

URL = "https://www.unob.cz/Stranky/default.aspx"

async def get_urls(browser, url):
    """Return a page after waiting for the given selector"""
    page = await browser.newPage()
    await page.goto(url)
    urls = await page.evaluate("""() => {
        const links = document.querySelectorAll(".ecm-uo-motive-nav a")
        const urls = Array.from(links).map(link => link.href)
        return urls
    }
    """)
    return urls

async def get_RightList(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    urls = await page.evaluate("""() => {
        const links = document.querySelectorAll(".box-right-list a")
        const urls = Array.from(links).map(link => link.href)
        return urls
    }
    """)
    return urls

async def get_Lide(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    urls = await page.evaluate("""() => {
        const links = document.querySelectorAll(".ms-WPBody  a")
        const urls = Array.from(links).map(link => link.href)
        return urls
    }
    """)
    return urls

async def get_data(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    data = await page.evaluate("""() => {
        const content = document.querySelectorAll("td")
        const ps = Array.from(content).map(element => element.textContent)
        return ps
    }
    """)
    return data



async def main():
    result = {"FacURL" : [], "KatURL" : [], "RightListURL" : [], "LideURL" : [], "NamesURL" : [], "info" : []}
    fakulty = {"fvt" : [], "fvl" : [], "fvz" : []}
    fvl = {"katedry" : [], "lide" : []}
    fvt = {"katedry" : []}
    fvz = {"katedry" : []}
    browser = await pyppeteer.launch()
    
    #page = await get_page(browser, URL.format(0), "div.ecm-uo-motive-nav")
    urls = await get_urls(browser, URL)
    """ 
    fakulty["fvl"].append(urls[0])
    fakulty["fvt"].append(urls[1])
    fakulty["fvz"].append(urls[2])
    for url in fakulty["fvl"]:
        katurl = await get_urls(browser, url)
        #fvl["katedry"].append(katurl)
        for url in katurl:
            RightList = await get_RightList(browser, url)
            fvl["katedry"].append(RightList[1])
    

    for url in fakulty["fvt"]:
        katurl = await get_urls(browser, url)
        #fvt["katedry"].append(katurl)
        for url in katurl:
            RightList = await get_RightList(browser, url)
            fvt["katedry"].append(RightList[1])
    
    for url in fakulty["fvz"]:
        katurl = await get_urls(browser, url)
        #fvz["katedry"].append(katurl)
        for url in katurl:
            RightList = await get_RightList(browser, url)
            fvz["katedry"].append(RightList[1])
    

    
    with open("outputs/fvl.json", "w", encoding = "utf8") as f:
        json.dump(fvl, f, indent=2)
    with open("outputs/fvt.json", "w", encoding = "utf8") as f:
        json.dump(fvt, f, indent=2)
    with open("outputs/fvz.json", "w", encoding = "utf8") as f:
        json.dump(fvz, f, indent=2)
    """
    for url in urls:
        result["FacURL"].append(url)
    
    for url in urls:
        katurl = await get_urls(browser, url)
        result["KatURL"].append(katurl)
        for url in katurl:
            RightList = await get_RightList(browser, url)
            result["RightListURL"].append(RightList)
    
    with open("outputs/RightList.json", "r") as f:
        content = json.load(f)
    
    for index in content:
        lideURL = index[1]
        result["LideURL"].append(lideURL)

    with open("outputs/lide.json", "r") as f:
        names = json.load(f)
    for url in names:
        NameURL = await get_Lide(browser, url)
        result["NamesURL"].append(NameURL)
    
    with open("outputs/Names.json", "r") as f:
        jmena = json.load(f)
    for url in jmena:
        info = await get_data(browser, url)
        result["info"].append(info)
        print(info)

    with open("outputs/katedry.json", "w", encoding = "utf8") as f:
        json.dump(result["KatURL"], f, indent=2)   
    with open("outputs/RightList.json", "w", encoding = "utf8") as f:
        json.dump(result["RightListURL"], f, indent=2)
    with open("outputs/lide.json", "w", encoding = "utf8") as f:
        json.dump(result["LideURL"], f, indent=2)
    with open("outputs/Names.json", "w", encoding = "utf8") as f:
        json.dump(result["NamesURL"], f, indent=2)
    with open("outputs/info.json", "w", encoding = "utf8") as f:
        json.dump(result["info"], f, indent=2)
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
