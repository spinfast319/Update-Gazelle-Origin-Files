# Update Gazelle-Origin Files
# author: hypermodified
# This script uses an exisiting yaml origin file for an album to update the file with additional metadata.
# You need a fork of gazelle-origin with the extra metatdata installled for it to work.
# It takes the folder and opens the yaml to get the url. It then uses the url to run origin query and saves the new origin file a work directory.
# It then deletes the original origin file and moves the new one to the albums folder.
# It can handle albums with artwork folders or multiple disc folders in them. 
# It can also handle specials characters and skips and logs any characters that makes windows fail.
# It has been tested and works in both Ubuntu Linux and Windows 10.


# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import yaml  # Imports yaml
import shutil # Imports functionality that lets you copy files and directory
import datetime # Imports functionality that lets you make timestamps
import subprocess  # Imports functionality that let's you run command line commands in a script
import requests # Imports the ability to make web or api requests
import re # Imports regex


# Set your directories here
album_directory = "M:\Python Test Environment\Albums" # Which directory has the albums you want to update the origin files for?
log_directory = "M:\Python Test Environment\Logs" # Which directory do you want the log albums that have missing origin files in?
work_directory = "M:\Python Test Environment\Work"  # Create directory for downloading the origin file to before you move it to the final directory.


'''#  Set your linux directories here
album_directory = "/mnt/m/Python Test Environment/Albums" # Which directory has the albums you want to update the origin files for
log_directory = "/mnt/m/Python Test Environment/Logs" # Which directory do you want the log albums that have missing origin files in?
work_directory = "/mnt/m/Python Test Environment/Work"  # Create directory for downloading the origin file to before you move it to the final directory.
'''

# Set your site and API information here
site_ident = "" # set your gazelle site here
site_ajax_page = "" # set the gazelle ajax page here
api_key = "" # set your api key here
headers = {"Authorization": api_key}

# Set up the counters for completed albums and missing origin files
count = 0
good_missing = 0
bad_missing = 0
bad_folder_name = 0
album_missing = 0
link_missing = 0
error_message = 0

#intro text
print("")
print("Engage!")

# A function to log events
def log_outcomes(d,p,m):
    global log_directory
    script_name = "Update-Origin Script"
    today = datetime.datetime.now()
    log_name = p
    directory = d
    message = m
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    log_path = log_directory + os.sep + log_name + ".txt"
    with open(log_path, 'a',encoding='utf-8') as log_name:
        log_name.write("--{:%b, %d %Y}".format(today)+ " at " +"{:%H:%M:%S}".format(today)+ " from the " + script_name + ".\n")
        log_name.write("The album " + album_name + " " + message + ".\n")
        log_name.write("Album location: " + directory + "\n")
        log_name.write(" \n")     

#  A function that gets the url of the album, downloads a new origin script and replaces the old one
def update_origin(directory):
        global count
        global good_missing
        global bad_missing
        global bad_folder_name
        global album_missing
        global link_missing
        global headers
        global site_ajax_page
        print ("\n")
        #check to see if folder has bad characters and skip if it does
        #get album name from directory
        re1 = re.compile(r"[\\/:*\"<>|?]");
        name_to_check = directory.split(os.sep)
        name_to_check = name_to_check[-1]
        if re1.search(name_to_check):
            print ("Illegal windows character detected.")
            print("--Logged album skipped due to illegal characters.")
            log_name = "illegal-characters"
            log_message = "was skipped due to illegal characters"
            log_outcomes(directory,log_name,log_message)
            bad_folder_name +=1 # variable will increment every loop iteration
            
        else:
            print("Getting new origin file for " + directory)
            #check to see if there is an origin file
            file_exists = os.path.exists('origin.yaml')
            #if origin file exists, load it, get url, run gazelle-origin, download new one, replace old one
            if file_exists == True:
                #open the yaml and turn the data into variables
                with open(directory + os.sep + 'origin.yaml',encoding='utf-8') as f:
                  data = yaml.load(f, Loader=yaml.FullLoader)
                album_url = data['Permalink']
                clean_directory = data['Directory']   
                                            
                # check to see if there is a gazelle link that exists and works
                if album_url != None:
                    
                    # check to see if the url in origin file goes to a real album
                    # get the torrent id from the permalink
                    torrent_id = album_url.split("=")
                    torrent_id = torrent_id[-1]
                    # create the ajax page
                    ajax_page = site_ajax_page
                    ajax_page = ajax_page + torrent_id          
                    # do an api request to get back a success or failure
                    r = requests.get(ajax_page, headers=headers)
                    status = r.json()
                    if status['status'] == "success":
                        print ("--The album was located.")            
                        #print("--The album is at " + album_url)
                        the_command = "gazelle-origin -t " + site_ident + " --api-key " + api_key + " " + album_url + " -o \"" + work_directory + os.sep + "origin.yaml\"" 
                        print("--Downloading new origin file as origin.yaml in work directory")
                        subprocess.run (the_command, shell=True) # Executes the gazzelle origin command on the directory you are in
                
                        #delete the origin file
                        print ("--Removed old origin file.")
                        os.remove(directory + os.sep + "origin.yaml")              
                        
                        #move origin.yaml file from work to directory
                        print("--Moved new origin.yaml from work directory to " + clean_directory)
                        os.rename(work_directory + os.sep + "origin.yaml", directory + os.sep + "origin.yaml")
                
                        count +=1 # variable will increment every loop iteration
                    else:
                        print("--The album is no longer on the site.")
                        print("--Logged missing album.")
                        log_name = "no-album"
                        log_message = "is no longer on the site"
                        log_outcomes(directory,log_name,log_message)
                        album_missing +=1 # variable will increment every loop iteration
                else:
                    print("--The is origin file is missing a link to the album.")
                    print("--Logged missing link.")
                    log_name = "no-link"
                    log_message = "origin file is missing a link to the album"
                    log_outcomes(directory,log_name,log_message)
                    link_missing +=1 # variable will increment every loop iteration
                    
            #otherwise log that the origin file is missing
            else:
                #split the directory to make sure that it distinguishes between folders that should and shouldn't have origin files
                path_segments = directory.split(os.sep)
                #create different log files depending on whether the origin file is missing somewhere it shouldn't be
                if len(path_segments) == 5:
                    #log the missing origin file folders that are likely supposed to be missing
                    print ("--An origin file is missing from a folder that should not have one.")
                    print("--Logged missing origin file.")
                    log_name = "good-missing-origin"
                    log_message = "origin file is missing from a folder that should not have one. You can double check"
                    log_outcomes(directory,log_name,log_message)
                    good_missing +=1 # variable will increment every loop iteration
                else:    
                    #log the missing origin file folders that are not likely supposed to be missing
                    print ("--An origin file is missing from a folder that should have one.")
                    print("--Logged missing origin file.")
                    log_name = "bad-missing-origin"
                    log_message = "origin file is missing from a folder that should have one"
                    log_outcomes(directory,log_name,log_message)
                    bad_missing +=1 # variable will increment every loop iteration
        
# Get all the subdirectories of album_directory recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
directories.remove(os.path.abspath(album_directory)) # If you don't want your main directory included

# Run a loop that goes into each directory identified and updates the origin file
for i in directories:
      os.chdir(i)         # Change working Directory
      update_origin(i)      # Run your function

# Summary text
print("")
print("Aye Aye Captain. This script updated " + str(count) + " origin files.")
if bad_folder_name >= 1:
    print("--There were " + str(bad_folder_name) + " folders with illegal characters.")
    error_message +=1 # variable will increment if statement is true
if album_missing >= 1:
    print("--There were " + str(album_missing) + " albums no longer on the site.")
    error_message +=1 # variable will increment if statement is true
if link_missing >= 1:
    print("--There were " + str(link_missing) + " origin files with a missing link to the album.")
    error_message +=1 # variable will increment if statement is true
if bad_missing >= 1:
    print("--There were " + str(bad_missing) + " folders missing an origin files that should have had them.")
    error_message +=1 # variable will increment if statement is true
if good_missing >= 1:
    print("--There were " + str(good_missing) + " folders missing origin files that should not have had them. Double check if you want.")
    error_message +=1 # variable will increment if statement is true
if error_message >= 1:
    print("Check the logs to see which folders had errors and what they were.")
else:
    print("There were no errors.")    

