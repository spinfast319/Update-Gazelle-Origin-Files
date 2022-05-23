# Update Gazelle-Origin Files Configuration File
# author: hypermodified
# Set your site flag, API key, ajaxpage and directorties here to use with Update Gazelle-Origin
# rename this file to config.py and keep it in the same directory as Update-Origin.py

# Set your directories here
c_album_directory = "" # Which directory has the albums you want to update the origin files for?
c_log_directory = "" # Which directory do you want the log albums that have missing origin files in?
c_work_directory = ""  # Create directory for downloading the origin file to before you move it to the final directory.

# Set whether you are using nested folders or have all albums in one directory
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
c_album_depth = 1

# Set your site and API information here
c_site_ident = "" # set your gazelle site here
c_site_ajax_page = "" # set the gazelle ajax page here
c_api_key = "" # set your api key here

#example configuration
'''
# Set your directories here
c_album_directory = "M:\Music\Albums" # Which directory has the albums you want to update the origin files for?
c_log_directory = "M:\Music\Logs" # Which directory do you want the log albums that have missing origin files in?
c_work_directory = "M:\Music\Work"  # Create directory for downloading the origin file to before you move it to the final directory.

# Set whether you are using nested folders or have all albums in one directory
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
c_album_depth = 1

# Set your site and API information here
c_site_ident = "red" # set your gazelle site here
c_site_ajax_page = "https://redacted.ch/ajax.php?action=torrent&id=" # set the gazelle ajax page here
c_api_key = "d64bq2l9.t236n539742x33120h5s5623h3615478" # set your api key here
'''