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

# Set your site and API information here
# for linux you can just have this be in your bashenv
site_ident = "red" # set your gazelle site here
api_key = "" # set your api key here
headers = {"Authorization": api_key}

# Set up the counters for completed albums and missing origin files
count = 0
missing = 0
bad_folder_name = 0
album_missing = 0
link_missing = 0

#intro text
print("")
print("Engage!")
print("")




#  A function that gets the url of the album, downloads a new origin script and replaces the old one
def update_origin(directory):
        global count
        global missing
        global bad_folder_name
        global album_missing
        global link_missing
        global headers
        print ("\n")
        #check to see if folder has bad characters and skip if it does
        #get album name from directory
        re1 = re.compile(r"[\\/∕:*\"<>|?]");
        name_to_check = directory.split("\\")
        name_to_check = name_to_check[-1]
        if re1.search(name_to_check):
            print ("Illegal windows character detected.")
            bad_folder_name +=1 # variable will increment every loop iteration
        else:
            print ("No illegal windows character detected.")
        
            print("Getting new origin file for " + directory)
            #check to see if there is an origin file
            file_exists = os.path.exists('origin.yaml')
            #if origin file exists, load it, get url, run gazelle-origin, download new one, replace old one
            if file_exists == True:
                #open the yaml and turn the data into variables
                with open(directory + '\origin.yaml',encoding='utf-8') as f:
                  data = yaml.load(f, Loader=yaml.FullLoader)
                album_url = data['Permalink']    
                            
                # check to see if there is a gazelle link that exists and works
                if album_url != None:
                    
                    # check to see if the url in origin fils goes to a real album
                    # get the torrent id from the permalink
                    torrent_id = album_url.split("=")
                    torrent_id = torrent_id[-1]
                    # create the ajax page
                    ajax_page = "https://redacted.ch/ajax.php?action=torrent&id="
                    ajax_page = ajax_page + torrent_id           
                    # do an api request to get back a success or failure
                    r = requests.get(ajax_page, headers=headers)
                    status = r.json()
                    if status['status'] == "success":
                        print ("--The album was located.")            
                        print("--The album is at " + album_url)
                        
                        # run gazelle origin on the url and write the new origin file to the directory
                        the_command = "gazelle-origin -t " + site_ident + " --api-key " + api_key + " " + album_url + " -o \"" + directory + "\\neworigin.yaml\"" #windows
                        print("--Downloading origin file as neworigin.yaml")
                        subprocess.run (the_command) # Executes the gazzelle origin command on the directory you are in
                
                        #delete the origin file
                        #print (directory + "\\origin.yaml")
                        os.remove(directory + "\\origin.yaml")
                
                        #rename neworigin to origin
                        print("--Renamed neworigin.yaml to origin.yaml")
                        os.rename(directory + "\\neworigin.yaml", directory + "\\origin.yaml")
                
                        '''#copy to completed directory
                        print(directory)
                        album_folder = os.path.split(directory)
                        album_folder = album_folder[-1]
                        new_album_path = completed_directory + album_folder
                        shutil.copytree(directory, new_album_path)'''
              
                        count +=1 # variable will increment every loop iteration
                    else:
                        print("--The album is no longer on the site.")
                        album_missing +=1 # variable will increment every loop iteration
                else:
                    print("--The is origin file is missing a link to the album.")
                    link_missing +=1 # variable will increment every loop iteration
            #otherwise log that the origin file is missing
            else:
                missing +=1 # variable will increment every loop iteration
                today = datetime.datetime.now()
                #split the director to make sure that it distinguishes between foldrs that should and shouldn't have origin files
                path_segments = directory.split("\\")
                #create different log files depending on whether the origin file is missing somewhere it shouldn't be
                if len(path_segments) == 5:
                    #log the missing origin file folders that are likely supposed to be missing
                    print ("--Missing origin file logged.")
                    the_good_log = log_directory + "good-log.txt"
                    with open(the_good_log, 'a') as log_file1:
                        log_file1.write("{:%b, %d %Y}".format(today)+ " at " +"{:%H:%M:%S}".format(today)+ ".\n")
                        log_file1.write(directory + "\\ is missing an origin file.\n")
                else:    
                    #log the missing origin file folders that are not likely supposed to be missing
                    print ("--Missing origin file logged.")
                    the_bad_log = log_directory + "bad-log.txt"
                    with open(the_bad_log, 'a') as log_file2:
                        log_file2.write("{:%b, %d %Y}".format(today)+ " at " +"{:%H:%M:%S}".format(today)+ ".\n")
                        log_file2.write(directory + "\\ is missing an origin file.\n")
        
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
print("There were " + str(bad_folder_name) + " folders with illegal characters.")
print("There were " + str(album_missing) + " albums no longer on the site.")
print("There were " + str(link_missing) + " origin files with a missing link to the album.")
print("There were " + str(missing) + " folders with no origin files. Check the log to see what they were.")

# ToDo
# check to see if folder name has special characters, if  so log it 
# move the updated folders to a done folder...that way you will have a nice folder of the ones that need to be run manaully
# Add error handling for if the gazzele link is missing (write to log)
# test in linux
# see if i can move the trailing slashes to the directory variable

