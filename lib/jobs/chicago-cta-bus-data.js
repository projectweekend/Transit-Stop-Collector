var async = require( "async" );
var _ = require( "lodash" );
var cta = require( "cta-bus-tracker" );


var busTracker = cta( process.env.CHICAGO_CTA_BUS_API_KEY );


var getRoutes = function ( done ) {

    busTracker.routes( done );
    // done( null, [ { rt: '8' } ] );

};


var getDirections = function ( routes, done ) {

    var makeDirectionsTask = function ( route ) {

        return function ( parallelDone ) {

            var routeWithDirection = function ( direction ) {

                return {
                    route: route.rt,
                    direction: direction
                };

            };

            busTracker.routeDirections( route.rt, function ( err, data ) {

                if ( err ) {
                    return parallelDone( err );
                }

                data = Array.isArray( data ) ? data : [ data ];
                return parallelDone( null, data.map( routeWithDirection ) );

            } );

        };

    };

    async.parallelLimit( routes.map( makeDirectionsTask ), 5, function ( err, result ) {

        if ( err ) {
            return done( err );
        }

        return done( null, [].concat.apply( [], result ) );

    } );

};


var getStops = function ( routes, done ) {

    var makeStopsTask = function ( route ) {

        return function ( parallelDone ) {

            var makeStopObject = function ( stop ) {

                return {
                    type: "bus",
                    route: route.route,
                    direction: route.direction,
                    name: stop.stpnm,
                    latitude: stop.lat,
                    longitude: stop.lon,
                    systemId: stop.stpid,
                    systemCode: "chicago-cta"
                };

            };

            busTracker.stops( route.route, route.direction, function ( err, data ) {

                if ( err ) {
                    return parallelDone( err );
                }

                data = Array.isArray( data ) ? data : [ data ];

                return parallelDone( null, data.map( makeStopObject ) );

            } );

        };

    };

    async.parallelLimit( routes.map( makeStopsTask ), 5, function ( err, result ) {

        if ( err ) {
            return done( err );
        }

        return done( null, [].concat.apply( [], result ) );

    } );

};


var main = function() {

    var tasks = [ getRoutes, getDirections, getStops ];

    async.waterfall( tasks, function ( err, result ) {

        // TODO: send this to mongo
        console.log( result );

    } );

};


if ( require.main === module ) {

    main();

}
