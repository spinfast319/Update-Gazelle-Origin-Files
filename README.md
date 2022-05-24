# Update-Gazelle-Origin-Files
### A python script that allows you to batch update your origin files with additional metadata, using an albums exisiting yaml origin file.

This project has a dependency on the gazelle-origin project created by x1ppy. gazelle-origin scrapes gazelle based sites and stores the related music metadata in a yaml file in the music albums folder. It is located here: https://github.com/x1ppy/gazelle-origin

For this script to work you need to use a fork that has additional metadata.  The fork that has the most additional metadata right now is:
https://github.com/spinfast319/gazelle-origin

This script allows you to batch update all of your origin files with new ones that have additional metadata.  It cycles through all the folders in a directory loads the yaml origin files inside them and reads url of the album. It then uses the url to run origin query and saves the new origin file a work directory. Then it deletes the original origin file and moves the new one to the album's folder. As it loops through the folders it caputres and logs any errors it encounters.

It can handle albums with artwork folders or multiple disc folders in them. It can also handle special characters and skips and logs any albums that have characters that makes windows fail. It has been tested and works in both Ubuntu Linux and Windows 10.

## Update gazelle-origin to grab additional metadata

First you need to uninstall gazelle origin.
```
pip uninstall gazelle-origin
```

Then you need to install a fork or branch with additional metadata.
```
pip install git+https://github.com/spinfast319/gazelle-origin
```

## Install and set up the script
Clone this script and test-config.py file where you want to run it.

### 1) Edit test-config.py
Set up or specify the three directories you will be using:
Go to *# Set your directories here*
1. The directory of the albums you want to update the origin files for
2. A directory to store the log files the script creates
3. An empty directory the script will use to temporarily hold and rename files before it moves them to the final location

Set the album_depth variable to specify whether you are using nested folders or have all albums in one directory:
Go to *# Set whether you are using nested folders or have all albums in one directory here*
- If you have all your ablums in one music directory, ie. Music/Album then set this value to 1
- If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2

The default is 1 (Music/Album)

Set your gazelle site information:
Go to *# Set your site and API information here*
1. Your gazelle site identity three letter code
2. Your gazelle site's ajax page
3. Your API key to the gazelle site

### 2) Rename test-config.py to config.py
### 3) Run the script from the command line.  


