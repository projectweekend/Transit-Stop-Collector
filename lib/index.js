var async = require( "async" );
var chicagoCTA = require( "./collectors/chicago-cta" );


exports.run = function ( done ) {

    chicagoCTA.collectBusData( function ( err ) {

        if ( err ) {
            console.log( err );
        } else {
            console.log( "Done!" );
        }

    } );

};
