import subprocess
import ConfigParser
import logging
import os.path
import requests
import time
import helpers
from datetime import date, datetime

if __name__ == "__main__":
    
    if not helpers.package_exists("streamlink"):
        print "Error: Streamlink is not installed"
        exit(1)

    # Load configuration file
    config = ConfigParser.RawConfigParser()
    try:
        config.readfp(open('config'))
    except IOError:
        print "Error: No configuration file 'config' found"
        exit(1)
    try:
        download_dir  = config.get('General', 'download-dir')
        quality       = config.get('General', 'quality')
        log_file_path = config.get('Logging', 'file-path')
        log_file_size = config.get('Logging', 'max-size')
    except ConfigParser.NoOptionError, e:
        print "Error:", e
        exit(1)

    helpers.setup_logging(log_file_path, log_file_size)
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    classes = [
        {"name": "Intro to DSA - Why Learning DSA is Important", "videoId": "YEOuqKT-svE", "day": datetime.strptime("19/11/20", '%d/%m/%y').date()},
        {"name": "Basic Maths + Practise Questions + Q/A", "videoId": "POehjAlYqNw", "day": datetime.strptime("25/11/20", '%d/%m/%y').date()},
        {"name": "Introduction to Arrays and Operations", "videoId": "uFdm_kXGJkU", "day": datetime.strptime("26/11/20", '%d/%m/%y').date()}]
    
    while True:
        today = date.today()
        thereIsAClassToday = False
        
        for aClass in classes:
            if aClass['day'] == today:
                thereIsAClassToday = True
            elif aClass['day'] < today:
                classes.pop()

        if not thereIsAClassToday:
            logging.info("No class today. Sleeping for 1 day")
            time.sleep(60*60*24)
            
        video_url = "https://www.youtube.com/watch?v="+classes[0]['videoId']
        
        today = time.strftime("%Y-%m-%d")
        
        # If more than 1 video saved today, concatenate a count
        i = 1
        while (os.path.isfile(os.path.join(download_dir, today+'-'+str(i)+'.mp4'))):
            i += 1
            
        output_fname = today+'-'+str(i)+'.mp4'

        logging.info("Downloading stream @ %s", video_url)
        
        # Invoke streamlink process to download the live video
        proc = subprocess.Popen(["streamlink", "-o", os.path.join(download_dir, classes[0]["name"] + ".mp4"), video_url, quality])
        exit_code = proc.wait()
        print(exit_code)
        if exit_code != 0:
            logging.info("Video is not live %s. Will wait for 5 minutes and retry.", video_url)
            time.sleep(300)