const {
  HLTV
} = require('hltv')

// Establish connection to HLTV API
const myHLTV = HLTV.createInstance({
  hltvUrl: 'my-proxy-server',
})

// File object instantiation
const fs = require('fs');

var abs_path = '/home/emmanuel/Desktop/csgo-data/'
var year_col = '2019'
var year_folder = abs_path+'data/matches-'+year_col+'/'

console.log('Collecting data from HLTV.org')


// Read individual map stats and save them
var str_vec = fs.readFileSync( year_folder+'matches.txt', 'utf-8').toString().split("\n")


function getMapStats( map_id, filename ) {
    HLTV.getMatchMapStats({id: map_id}).then(res => {

    	// Convert dictionary to JSON object
    	let tmp = JSON.stringify(res);

    	// Write data to directory
	fs.writeFileSync( filename, tmp);

	console.log( '-> Wrote mapid: '+map_id.toString() );
	
    } ).catch( (err) => {

	console.log( '** Error on mapID = '+map_id.toString() )

    });
}


// Make sure to wait
var i = 0
function f() {
    console.log('At step '+i.toString()+' out of '+str_vec.length)
    var mapid = parseInt(str_vec[i])

    var fileaux = year_folder+'maps/hltv_map_' + mapid.toString() + '.json'

    // Here we always overite the map file
    getMapStats( mapid, fileaux )
    i++
    if (i < str_vec.length) {
	setTimeout(f, 5000) // 5 seconds
    }

    // Here we only save the ones that don't exist
    // if(	fs.existsSync(fileaux) ) {
    // 	// Do nothing other than moving over
    // 	i ++
    // 	if (i < str_vec.length) {
    // 	    setTimeout(f, 100) // 100 ms
    // 	}
    // } else {
    // 	getMapStats( mapid, fileaux )
    // 	i++
    // 	if (i < str_vec.length) {
    // 	    setTimeout(f, 5000) // 5 seconds
    // 	}
    // }
}

f()
