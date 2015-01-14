var async = require( "async" );
var nomnom = require( "nomnom" );
var mongoose = require( "mongoose" );
var cta = require( "./chicago-cta" );
var utils = require( "../utils" );
var TransitStop = require( "../models" ).TransitStop;

var options = nomnom.option( "file", {
                    abbr: "f",
                    default: null,
                    help: "Path to output file for JSON export"
                } )
                .parse();

mongoose.connect( process.env.MONGO_URL );


var rebuildData = function ( transitStops, done ) {

    TransitStop.remove( {}, function ( err, result ) {

        if ( err ) {
            return done( err );
        }

        TransitStop.collection.insert( transitStops, function ( err, data ) {

            if ( err ) {
                return done( err );
            }

            return done( null, data );

        } );

    } );

};


var tasksCompleted = function ( err, result ) {

    if ( options.file ) {
        utils.writeJSONFile( options.file, result, function ( err ) {

            if ( err ) {
                console.log( "Error generating JSON file" );
                process.exit( 1 );
            }

            process.exit( 0 );

        } );
    }

    rebuildData( result, function ( err, data ) {

        if ( err ) {
            console.log( err );
            process.exit( 1 );
        }

        process.exit( 0 );

    } );

};


var main = function() {

    var tasks = [
        cta.bus.getRoutes,
        cta.bus.getDirections,
        cta.bus.getStops
    ];

    async.waterfall( tasks, tasksCompleted );

};


if ( require.main === module ) {

    main();

}
