#!/bin/python3

# Modules
import subprocess
import json
import os.path
import csgodata
from datetime import datetime, timedelta

# Define important file locations
current_year = '2019'
myfolder = '/home/emmanuel/Desktop/csgo-data/'
path = myfolder+'data/matches-' + current_year + '/'


# jkl
#-------------------------------------------------#
# Set the current date for start and end search---#
#-------------------------------------------------#

# We scan minus three days to make sure we don't miss
end_date   = datetime.today() + timedelta(days=1)
start_date = datetime.today() - timedelta(days=3)

# # Set by hand
# end_date   = datetime(2019,6,30)
# start_date = datetime(2019,1,1)

output_file = open( myfolder+'log/start_date.log', 'w' )
output_file.write( start_date.strftime("%Y-%m-%d" ) )
output_file.close()

output_file = open( myfolder+'log/end_date.log', 'w' )
output_file.write( end_date.strftime("%Y-%m-%d" ) )
output_file.close()

#-------------------------------------------------#

#-------------------------------------------------#
# Scrape match data ------------------------------#
#-------------------------------------------------#

cmd     = '/snap/bin/node ' + myfolder + 'get_matches.js'
process = subprocess.Popen( cmd, shell=True )

# Wait for process to finish
process.wait()

if process.returncode != 0:
    # There was a problem collecting matches
    print( 'Error in get_matches.js' )
    quit()

# get_matches.js saves a tmp json, now we need to
# merge the master and tmp json, then delete the
# tmp one
tmp_json_fname    = path + 'hltv_matches_tmp.json'
master_json_fname = path + 'hltv_matches.json'

with open( tmp_json_fname ) as f:
    tmp_data = json.load(f)

with open( master_json_fname ) as f:
    data = json.load(f)

# Append and Trim possible repeated entries
# -> Note that here the order here is important since if there's
#    overlap, we want to take the one in tmp_data
data = tmp_data + data

result  = []
matches = []

# Since the master_json might have some incomplete data, we append to
# tmp_data all the matches from the master_json that are not in
# tmp_data
for match in data:

    match_id = str(match['id'])

    if match_id not in matches:

        matches.append( match_id )
        result.append( match )

data = result

# Update matches json file
with open( master_json_fname, 'w' ) as f:
    json.dump( data, f )
    
#-------------------------------------------------#


#-------------------------------------------------#
# Find out which maps we need to download --------#
#-------------------------------------------------#

# Here we save al the map JSON's that are in tmp_data

#-> The problem is that some of the previous ones might be incomplete
# if they were saved in the middle of the match. To be safe, we
# re-write all the ones that correspond to these days.

# Extract the matches that haven't been saved
output_file = open( path + 'matches.txt', 'w' )

for match in tmp_data:

    match_id = str(match['id'])
    file = path + 'maps/hltv_map_' + match_id + '.json'

    output_file.write( match_id + '\n' )
    
    # if not( os.path.isfile( file ) ):
    #    output_file.write( match_id + '\n' )

output_file.close()
        
#-------------------------------------------------#


#-------------------------------------------------#
# Scrape individual map data ---------------------#
#-------------------------------------------------#

cmd     = '/snap/bin/node ' + myfolder + 'get_maps.js'
process = subprocess.Popen( cmd, shell=True )

# Wait for process to finish
process.wait()

if process.returncode != 0:
    # There was a problem collecting matches
    print( 'Error in get_maps.js' )
    quit()
    
#-------------------------------------------------#

# #jkl

#-------------------------------------------------#
# Update Master CSVs -----------------------------#
#-------------------------------------------------#

csgodata.createMasterDataFrames( current_year )

# Copy the CSVs to the shared folder
cmd = 'cp -f ' + myfolder + 'data/csv/'+current_year+'-*.csv ~/Dropbox/csgo-csv/.'

process = subprocess.Popen( cmd, shell=True )

# Wait for process to finish
process.wait()

if process.returncode != 0:
    print( 'Error copying file' )
    quit()


# Compress the json files from the current year
zipfile   = myfolder + current_year+'-json.zip'
folderloc = myfolder + 'data/matches-' + current_year
cmd = 'zip -rq ' + zipfile + ' ' + folderloc

process = subprocess.Popen( cmd, shell=True )

# Wait for process to finish
process.wait()

if process.returncode != 0:
    print( 'Error compression' )
    quit()

# Move the compressed file
cmd = 'mv -f ' + zipfile + ' ~/Dropbox/csgo-csv/.'

process = subprocess.Popen( cmd, shell=True )

# Wait for process to finish
process.wait()

if process.returncode != 0:
    print( 'Error compression' )
    quit()

#-------------------------------------------------#


# Save log files and update dates ----------------#

output_file = open( myfolder + 'log/last_run.log', 'w' )
output_file.write( 'Succesfully finished running scraper for:\n' )
output_file.write( '-> Start date: ' + start_date.strftime("%Y-%m-%d" ) + '\n' )
output_file.write( '-> End date:   ' + end_date.strftime("%Y-%m-%d" ) + '\n \n' )

now = datetime.now()

output_file.write( 'Execution finished at: ' + now.strftime("%Y-%m-%d %H:%M") )

output_file.close()


print( 'Succesfully finished running scraper for:\n' )
print( '-> Start date: ' + start_date.strftime("%Y-%m-%d" ) + '\n' )
print( '-> End date:   ' + end_date.strftime("%Y-%m-%d" ) + '\n \n' )

print( 'Execution finished at: ' + now.strftime("%Y-%m-%d %H:%M") + '\n \n' )

# Copy the log file to the shared folder
cmd = 'cp ' + myfolder + 'log/last_run.log ~/Dropbox/csgo-csv/.'

process = subprocess.Popen( cmd, shell=True )

# Wait for process to finish
process.wait()

if process.returncode != 0:
    print( 'Error compression' )
    quit()

#-------------------------------------------------#




