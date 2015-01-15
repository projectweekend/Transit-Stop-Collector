var async = require( "async" );
var mongoose = require( "mongoose" );
var cta = require( "./api" );
var utils = require( "../../utils" );
var TransitStop = require( "../../models" ).TransitStop;


mongoose.connect( process.env.MONGO_URL );


var rebuildData = function ( transitStops, done ) {

    var removeOldTransitStops = function ( seriesDone ) {

        TransitStop.removeBusChicagoCTA( function ( err ) {

            if ( err ) {
                return seriesDone( err );
            }

            return seriesDone( null );

        } );

    };

    var addNewTransitStops = function ( seriesDone ) {

        TransitStop.insertBulk( transitStops, function ( err ) {

            if ( err ) {
                return seriesDone( err );
            }

            return seriesDone( null );

        } );

    };

    var tasks = [ removeOldTransitStops, addNewTransitStops ];

    async.series( tasks, function ( err, results ) {

        if ( err ) {
            return done( err );
        }

        return done( null );

    } );

};


module.exports = {

    collectBusData: function( done ) {

        var tasks = [
            cta.bus.getRoutes,
            cta.bus.getDirections,
            cta.bus.getStops
        ];

        var tasksCompleted = function ( err, result ) {

            rebuildData( result, function ( err ) {

                if ( err ) {
                    return done( err );
                }

                return done( null );

            } );

        };

        async.waterfall( tasks, tasksCompleted );

    }

};
