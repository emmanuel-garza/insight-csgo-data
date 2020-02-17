const {
    HLTV
} = require('hltv')

// Establish connection to HLTV API
const myHLTV = HLTV.createInstance({
    hltvUrl: 'my-proxy-server',
})

// File object instantiation
const fs = require('fs');

// var eventid_str = '4273'
// var eventid_int = parseInt(eventid_str)


// Read individual map stats and save them
var str_vec = fs.readFileSync( 'event_ids.txt', 'utf-8').toString().split("\n")


function getEventDetails( event_id, filename ) {

    HLTV.getEvent({ id: event_id }).then(res => {

        console.log('Event overview successfully collected');

        // Convert dictionary to JSON object
        let data = JSON.stringify(res);

        // Write data to directory
        fs.writeFileSync( filename, data);

        console.log('-> Wrote Event');

        // var date = new Date();
        // var current_hour = date.getHours();
        // var current_min = date.getMinutes();
        // var current_sec = date.getSeconds();

        // console.log(current_hour + ':' + current_min + ':' + current_sec)

    }).catch((err) => {

        console.log('** Error Collecting Event')

    }); 

}



// Make sure to wait
var i = 0
function f() {
    
    console.log('At step '+i.toString()+' out of '+str_vec.length)
    
    var eventid_int = parseInt(str_vec[i])
    var fileaux     = 'data/events/hltv_event_' + eventid_int.toString() + '.json'

    // For loging purposes
    var date = new Date();
    var current_hour = date.getHours();
    var current_min = date.getMinutes();
    var current_sec = date.getSeconds();


    console.log( fileaux )

    console.log('Current time = ' + current_hour + ':' + current_min + ':' + current_sec)

    // Here we always overite the map file
    // getEventDetails( eventid_int, fileaux )
    // i++
    // if (i < str_vec.length) {
    //     setTimeout(f, 5000) // 5 seconds
    // }

    console.log( ' ' )

    // Here we only save the ones that don't exist
    if (fs.existsSync(fileaux)) {
        // Do nothing other than moving over
        i++
        if (i < str_vec.length) {
            setTimeout(f, 100) // 100 ms
        }
    } else {
        getEventDetails( eventid_int, fileaux )
        i++
        if (i < str_vec.length) {
            setTimeout(f, 3000) // 3 seconds
        }
    }
}

f()