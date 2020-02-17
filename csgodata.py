import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

ABS_PATH = '/home/emmanuel/Desktop/csgo-data/'

#-------------------------------------------------#
# Save to CSV ------------------------------------#
#-------------------------------------------------#
def createMasterDataFrames( year ):

    year_vec = [ year ]
    dic1, dic2 = createMasterDictionary( year_vec )

    # With Map Results
    df1 = pd.DataFrame.from_dict( dic1['team1'], orient='index' )
    df2 = pd.DataFrame.from_dict( dic1['team2'], orient='index' )

    df = df1.append(df2, ignore_index=True)

    # With Player statistics
    df2 = pd.DataFrame()
    
    for count in range(5):
        
        df_a = pd.DataFrame.from_dict( dic2['team1'][str(count)], orient='index' )
        df_b = pd.DataFrame.from_dict( dic2['team2'][str(count)], orient='index' )

        df2 = df2.append( df_a, ignore_index=True, sort=False )
        df2 = df2.append( df_b, ignore_index=True, sort=False )


    print( 'Saving Data Frames to csv files ')
    df.to_csv(ABS_PATH+'data/csv/'+year+'-team-lvl.csv', index=False )
    df2.to_csv(ABS_PATH+'data/csv/'+year+'-player-lvl.csv', index=False )
            
    return

#-------------------------------------------------#
# Scrape individual map data ---------------------#
#-------------------------------------------------#
def createMasterDictionary( year_vec ):

    # Empty structures

    # Match data
    master_dict_1 = {}
    master_dict_1['team1'] = {}
    master_dict_1['team2'] = {}

    # Player stats
    master_dict_2 = {}
    master_dict_2['team1'] = {}
    master_dict_2['team2'] = {}

    for count in range(5):
        master_dict_2['team1'][str(count)] = {}
        master_dict_2['team2'][str(count)] = {}
    
    # Iterate troughout all the years
    for year in year_vec:
    
        path = ABS_PATH+'data/matches-'+year+'/maps/'

        # Scan all files
        for fileobj in os.listdir(path):
        
            file = os.fsdecode(fileobj);

            map_id = file.strip('hltv_map_')
            map_id = map_id.strip('.json')

            # print( map_id )

            # Load in JSON file
            with open(path + file) as f:
                try:
                    data = json.load(f)
                except:
                    print('aha')
                    continue

            # Collect appropriate data
            try:
                match_map = data['map']
            except:
                # print( 'Map set to null'  )
                match_map = 'null'
            
                
            match_date  = data['date']
            event_id    = data['event']['id']
            event_name  = data['event']['name']

            tmp     = int( match_date ) / 1000
            date_hr = datetime.utcfromtimestamp(tmp).strftime('%Y-%m-%d %H:%M:%S') 
            
            '''TEAM LEVEL DATAFRAME'''
            team1_id = data['team1']['id']
            team1_name = data['team1']['name']
            team1_score = data['team1']['score']

            try:
                team1_kills = data['performanceOverview']['team1']['kills']
                team1_deaths = data['performanceOverview']['team1']['deaths']
                team1_assists = data['performanceOverview']['team1']['assists']
            except:
                team1_kills = np.nan
                team1_deaths = np.nan
                team1_assists = np.nan

            
    
            team2_id = data['team2']['id']
            team2_name = data['team2']['name']
            team2_score = data['team2']['score']

            try:
                team2_kills = data['performanceOverview']['team2']['kills']
                team2_deaths = data['performanceOverview']['team2']['deaths']
                team2_assists = data['performanceOverview']['team2']['assists']
            except:
                team2_kills = np.nan
                team2_deaths = np.nan
                team2_assists = np.nan


            master_dict_1['team1'][map_id] = {}
            master_dict_1['team2'][map_id] = {}
            
            master_dict_1['team1'][map_id]['map_id']       = map_id
            master_dict_1['team1'][map_id]['map']          = match_map
            master_dict_1['team1'][map_id]['date_unix']    = match_date

            master_dict_1['team1'][map_id]['date_human_utc'] = date_hr

            master_dict_1['team1'][map_id]['event_id']     = event_id
            master_dict_1['team1'][map_id]['event_name']   = event_name
            
            master_dict_1['team1'][map_id]['team_id']      = team1_id
            master_dict_1['team1'][map_id]['team_name']    = team1_name
            master_dict_1['team1'][map_id]['team_score']   = team1_score
            master_dict_1['team1'][map_id]['team_kills']   = team1_kills
            master_dict_1['team1'][map_id]['team_deaths']  = team1_deaths
            master_dict_1['team1'][map_id]['team_assists'] = team1_assists
            

            master_dict_1['team2'][map_id]['map_id']       = map_id
            master_dict_1['team2'][map_id]['map']          = match_map

            master_dict_1['team2'][map_id]['date_unix']    = match_date

            master_dict_1['team2'][map_id]['date_human_utc'] = date_hr

            master_dict_1['team2'][map_id]['event_id']     = event_id
            master_dict_1['team2'][map_id]['event_name']   = event_name
                                           
            master_dict_1['team2'][map_id]['team_id']      = team2_id
            master_dict_1['team2'][map_id]['team_name']    = team2_name
            master_dict_1['team2'][map_id]['team_score']   = team2_score
            master_dict_1['team2'][map_id]['team_kills']   = team2_kills
            master_dict_1['team2'][map_id]['team_deaths']  = team2_deaths
            master_dict_1['team2'][map_id]['team_assists'] = team2_assists

            '''PLAYER LEVEL DATAFRAME'''
            # Get data for each player for a match
            count = 0
            for player in data['playerStats']['team1']:

                master_dict_2['team1'][str(count)][map_id] = {}
                
                master_dict_2['team1'][str(count)][map_id]['map_id']       = map_id
                master_dict_2['team1'][str(count)][map_id]['map']          = match_map
                master_dict_2['team1'][str(count)][map_id]['date']         = match_date
                master_dict_2['team1'][str(count)][map_id]['team_id']      = team1_id
                master_dict_2['team1'][str(count)][map_id]['team_name']    = team1_name
                
                master_dict_2['team1'][str(count)][map_id]['player_id']        = player['id']
                master_dict_2['team1'][str(count)][map_id]['player_name']      = player['name']
                master_dict_2['team1'][str(count)][map_id]['kills']            = player['kills']
                master_dict_2['team1'][str(count)][map_id]['hs_kills']         = player['hsKills']
                master_dict_2['team1'][str(count)][map_id]['assists']          = player['assists']
                master_dict_2['team1'][str(count)][map_id]['flash_assists']    = player['flashAssists']
                master_dict_2['team1'][str(count)][map_id]['deaths']           = player['deaths']
                master_dict_2['team1'][str(count)][map_id]['KAST']             = player['KAST']
                master_dict_2['team1'][str(count)][map_id]['kill_death_diff']  = player['killDeathsDifference']
                master_dict_2['team1'][str(count)][map_id]['ADR']              = player['ADR']
                master_dict_2['team1'][str(count)][map_id]['first_kills_diff'] = player['firstKillsDifference']
                master_dict_2['team1'][str(count)][map_id]['rating']           = player['rating']
                                    
                # Some entries that not all have
                try:
                    master_dict_2['team1'][str(count)][map_id]['kills_per_round']  = player['killsPerRound']
                except:
                    master_dict_2['team1'][str(count)][map_id]['kills_per_round']  = np.nan

                try:
                    master_dict_2['team1'][str(count)][map_id]['deaths_per_round'] = player['deathsPerRound']
                except:
                    master_dict_2['team1'][str(count)][map_id]['deaths_per_round'] = np.nan

                try:
                    master_dict_2['team1'][str(count)][map_id]['impact'] = player['impact']
                except:
                    master_dict_2['team1'][str(count)][map_id]['impact'] = np.nan
                    
                count = count + 1

                # To avoid the very rare cases where there's more than 5 players
                if count == 5:
                    break
                
                
                
            # Team 2
            count = 0
            for player in data['playerStats']['team2']:

                # print( count )
                # print( map_id )
                # tmp = match_date/1000
                # print( datetime.utcfromtimestamp(tmp).strftime('%Y-%m-%d %H:%M:%S') )
                
                master_dict_2['team2'][str(count)][map_id] = {}
                
                master_dict_2['team2'][str(count)][map_id]['map_id']       = map_id
                master_dict_2['team2'][str(count)][map_id]['map']          = match_map
                master_dict_2['team2'][str(count)][map_id]['date']         = match_date
                master_dict_2['team2'][str(count)][map_id]['team_id']      = team2_id
                master_dict_2['team2'][str(count)][map_id]['team_name']    = team2_name
                
                master_dict_2['team2'][str(count)][map_id]['player_id']        = player['id']
                master_dict_2['team2'][str(count)][map_id]['player_name']      = player['name']
                master_dict_2['team2'][str(count)][map_id]['kills']            = player['kills']
                master_dict_2['team2'][str(count)][map_id]['hs_kills']         = player['hsKills']
                master_dict_2['team2'][str(count)][map_id]['assists']          = player['assists']
                master_dict_2['team2'][str(count)][map_id]['flash_assists']    = player['flashAssists']
                master_dict_2['team2'][str(count)][map_id]['deaths']           = player['deaths']
                master_dict_2['team2'][str(count)][map_id]['KAST']             = player['KAST']
                master_dict_2['team2'][str(count)][map_id]['kill_death_diff']  = player['killDeathsDifference']
                master_dict_2['team2'][str(count)][map_id]['ADR']              = player['ADR']
                master_dict_2['team2'][str(count)][map_id]['first_kills_diff'] = player['firstKillsDifference']
                master_dict_2['team2'][str(count)][map_id]['rating']           = player['rating']

                # Some entries that not all have
                try:
                    master_dict_2['team2'][str(count)][map_id]['kills_per_round']  = player['killsPerRound']
                except:
                    master_dict_2['team2'][str(count)][map_id]['kills_per_round']  = np.nan

                try:
                    master_dict_2['team2'][str(count)][map_id]['deaths_per_round'] = player['deathsPerRound']
                except:
                    master_dict_2['team2'][str(count)][map_id]['deaths_per_round'] = np.nan

                try:
                    master_dict_2['team2'][str(count)][map_id]['impact'] = player['impact']
                except:
                    master_dict_2['team2'][str(count)][map_id]['impact'] = np.nan
                    
                count = count + 1

                # To avoid the very rare cases where there's more than 5 players
                if count == 5:
                    break
       
    return master_dict_1, master_dict_2

