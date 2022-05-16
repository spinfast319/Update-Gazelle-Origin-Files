# Update Gazelle-Origin Files
# author: hypermodified
# version: 1.0
# This script is meant to use the exisitng yaml origin files and update them with the more complete origin+ files
# It takes the folder and opens the yaml to get the url. It then uses the url to run origin query and names the file something differnt.
# It then deletes the original origin and renames the new one to origin.
# It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters and removes any characters that makes windows fail.
# You need gazelle-origin installled for it to work.

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import yaml  # Imports yaml
import shutil # Imports functionality that lets you copy files and directory
import datetime # Imports functionality that lets you make timestamps
import subprocess  # Imports functionality that let's you run command line commands in a script
import requests # Imports the ability to make web or api requests
import re # Imports regex


#  Set your directories here
directory_to_update = "M:\Python Test Environment\Albums\\" # Which directory has the albums you want to update the origin files for?
completed_directory =  "M:\Python Test Environment\Done\\" # Which directory has the albums you want to update the origin files for?
log_directory = "M:\Python Test Environment\Logs\\" # Which directory do you want the log albums that have missing origin files in?
work_directory = "M:\Python Test Environment\Work\\"  # Create directory for downloading the origin file to before you move it to the final directory.

# Set your site and API information here
# for linux you can just have this be in your ~/.bashrc file
site_ident = "" # set your gazelle site here
site_ajax_page = ""
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
print("")

# A function to log events
def log_outcomes(d,p,m):
    global log_directory
    script_name = "Update-Origin Script"
    today = datetime.datetime.now()
    log_name = p
    directory = d
    message = m
    album_name = directory.split("\\")
    album_name = album_name[-1]
    log_path = log_directory + log_name + ".txt"
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
        name_to_check = directory.split("\\")
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
                with open(directory + '\origin.yaml',encoding='utf-8') as f:
                  data = yaml.load(f, Loader=yaml.FullLoader)
                album_url = data['Permalink']
                clean_directory = data['Directory']   
                print (directory)
                #directory = directory_to_update + clean_directory
                #print (directory)
                            
                # check to see if there is a gazelle link that exists and works
                if album_url != None:
                    
                    # check to see if the url in origin fils goes to a real album
                    # get the torrent id from the permalink
                    torrent_id = album_url.split("=")
                    torrent_id = torrent_id[-1]
                    # create the ajax page
                    ajax_page = site_ajax_page
                    ajax_page = ajax_page + torrent_id   
                    print(ajax_page)        
                    # do an api request to get back a success or failure
                    r = requests.get(ajax_page, headers=headers)
                    status = r.json()
                    if status['status'] == "success":
                        print ("--The album was located.")            
                        print("--The album is at " + album_url)
                        the_command = "gazelle-origin -t " + site_ident + " --api-key " + api_key + " " + album_url + " -o \"" + work_directory + "origin.yaml\"" #windows
                        print("--Downloading origin file as neworigin.yaml")
                        subprocess.run (the_command) # Executes the gazzelle origin command on the directory you are in
                
                        #delete the origin file
                        print ("--Removed old origin file.")
                        os.remove(directory + "\\origin.yaml")
                
                        #rename neworigin to origin
                        #print("--Renamed neworigin.yaml to origin.yaml")
                        #os.rename(directory + "\\neworigin.yaml", directory + "\\origin.yaml")
                        
                        #move origin.yaml file from work to directory
                        print("--Moved origin.yaml from work directory to " + clean_directory)
                        os.rename(work_directory + "origin.yaml", directory + "\\origin.yaml")
                
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
                #split the director to make sure that it distinguishes between foldrs that should and shouldn't have origin files
                path_segments = directory.split("\\")
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
        
# Get all the subdirectories of directory_to_update recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_update)]
directories.remove(os.path.abspath(directory_to_update)) # If you don't want your main directory included

#  Run a loop that goes into each directory identified and updates the origin file
for i in directories:
      os.chdir(i)         # Change working Directory
      update_origin(i)      # Run your function

#summary text
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

# ToDo
# figure out global ajax
# test in linux
# --see if i can move the trailing slashes to the directory variable

