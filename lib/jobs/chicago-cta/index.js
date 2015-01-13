var async = require( "async" );
var cta = require( "cta-bus-tracker" );


var busTracker = cta( process.env.CHICAGO_CTA_BUS_API_KEY );


var makeArray = function ( data ) {

    return Array.isArray( data ) ? data : [ data ];

};


var buildBusDirectionsTask = function ( item ) {

    return function ( parallelDone ) {

        var routeWithDirection = function ( direction ) {

            return {
                route: item.rt,
                direction: direction
            };

        };

        busTracker.routeDirections( item.rt, function ( err, data ) {

            if ( err ) {
                return parallelDone( err );
            }

            return parallelDone( null, makeArray( data ).map( routeWithDirection ) );

        } );

    };
};


var buildBusStopsTask = function ( item ) {

    return function ( parallelDone ) {

        var makeStopObject = function ( stop ) {

            return {
                type: "bus",
                route: item.route,
                direction: item.direction,
                name: stop.stpnm,
                latitude: stop.lat,
                longitude: stop.lon,
                systemId: stop.stpid,
                systemCode: "chicago-cta"
            };

        };

        busTracker.stops( item.route, item.direction, function ( err, data ) {

            if ( err ) {
                return parallelDone( err );
            }

            return parallelDone( null, makeArray( data ).map( makeStopObject ) );

        } );

    };

};


module.exports = {

    bus: {
        getRoutes: function ( done ) {

            busTracker.routes( done );

        },
        getDirections: function ( routes, done ) {

            async.parallelLimit( routes.map( buildBusDirectionsTask ), 5, function ( err, result ) {

                if ( err ) {
                    return done( err );
                }

                return done( null, [].concat.apply( [], result ) );

            } );

        },
        getStops: function ( routes, done ) {

            async.parallelLimit( routes.map( buildBusStopsTask ), 5, function ( err, result ) {

                if ( err ) {
                    return done( err );
                }

                return done( null, [].concat.apply( [], result ) );

            } );

        }
    },
    train: {}

};
