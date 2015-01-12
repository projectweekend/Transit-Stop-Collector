var async = require( "async" );
var _ = require( "lodash" );
var cta = require( "cta-bus-tracker" );


var busTracker = cta( process.env.CHICAGO_CTA_BUS_API_KEY );


var getRoutesTask = function ( done ) {

    busTracker.routes( done );

};


var getDirectionsTask = function ( routes, done ) {

    var directionsForRoute = function ( route ) {

        return function ( parallelDone ) {

            var output = {
                route: route.rt
            };

            busTracker.routeDirections( route.rt, function ( err, data ) {

                if ( err ) {
                    return parallelDone( err );
                }

                output.directions = typeof data === "string" ? [ data ] : data;
                return parallelDone( null, output );

            } );

        };

    };

    var tasks = routes.map( directionsForRoute );

    async.parallelLimit( tasks, 5, function ( err, result ) {

        if ( err ) {
            return done( err );
        }

        return done( null, result );

    } );

};


var getStopsTask = function ( routes, done ) {

    var stopsForRouteDirection = function ( route ) {

        return function ( parallelDone ) {



        };

    };

    // Change this
    return done( null, routes );

};


var main = function() {

    var tasks = [ getRoutesTask, getDirectionsTask, getStopsTask ];

    async.waterfall( tasks, function ( err, result ) {

        console.log( result );

    } );

};

if ( require.main === module ) {

    main();

}
