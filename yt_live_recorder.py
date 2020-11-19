import ConfigParser
import logging
import os.path
import requests
import time
import helpers

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
    
    while True:
        video_id = 'YEOuqKT-svE'
            
        video_url = "https://www.youtube.com/watch?v="+video_id
        
        today = time.strftime("%Y-%m-%d")
        
        # If more than 1 video saved today, concatenate a count
        i = 1
        while (os.path.isfile(os.path.join(download_dir, today+'-'+str(i)+'.mp4'))):
            i += 1
            
        output_fname = today+'-'+str(i)+'.mp4'

        logging.info("Downloading stream @ %s", video_url)
        
        # Invoke streamlink process to download the live video
        proc = Popen(["streamlink", "-o", os.path.join(download_dir, output_fname), video_url, quality])
        exit_code = proc.wait()
