const {
  HLTV
} = require('hltv')

// Establish connection to HLTV API
const myHLTV = HLTV.createInstance( {
  hltvUrl: 'my-proxy-server',
} )

// File object instantiation
const fs = require('fs');

var abs_path = '/home/emmanuel/Desktop/csgo-data/'
var year_col = '2019'
// var year_folder = 'data/matches-'+year_col+'/'
var year_folder = abs_path+'data/matches-'+year_col+'/'


// console.log( 'Testing get_matches inside Python (not collecting)' )

var start_date = fs.readFileSync( abs_path+'log/start_date.log' )
var end_date   = fs.readFileSync( abs_path+'log/end_date.log' )

console.log( 'Start date = ' + start_date )
console.log( 'End date   = ' + end_date )

HLTV.getMatchesStats({startDate: start_date, endDate: end_date}).then((res) => {

    console.log('Match overview results successfully collected for given dates');

    // Convert dictionary to JSON object
    let data = JSON.stringify(res);

    // Write data to directory
    fs.writeFileSync( year_folder + 'hltv_matches_tmp.json', data);

    console.log( '-> Wrote matches' );
    
} ).catch( (err) => {

    console.log( '** Error Collecting Matches' )

} ); 
