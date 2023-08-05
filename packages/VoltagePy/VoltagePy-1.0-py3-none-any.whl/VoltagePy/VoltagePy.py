#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

#webdriver
browser = None
driver_folder = None

#init webdriver, defining options and capabilities
#by default the methods will autoload browser if None
def start(drive = ""):
    #options and capabilities
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    capabilities = options.to_capabilities()

    #setup drive path
    if(drive is not ""): 
        global driver_folder
        driver_folder = drive
    else:
        print("Please setup a drive path ex. start('path/to/drive')")

    #init webdrive
    global browser
    browser = webdriver.Chrome(executable_path=driver_folder,desired_capabilities=capabilities)

#open the page ex. browser.get("https://www.duckduckgo.com"), if in headless, there's no window.
def open(url):
    if(browser is None): start()
    browser.get(url)

#copy the contet of a "opened page" and return it
def pageHtml(url = ""):
    html = "PAGE NOT LOADED"
    
    #open a page if a url is provided
    if(url != "") : open(url)
    
    #check if the page is loaded 
    if(browser.title != ""):
        #if the url is not null, open and copy     
        html = browser.page_source
    return html

#close the browser
def quit():
    browser.close()
    browser.quit()

#--exemple of commands and response--
#start()
#open("https://www.duckduckgo.com")
#print(copyContent())
#quit()