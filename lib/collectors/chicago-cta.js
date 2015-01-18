var fs = require( "fs" );
var _ = require( "lodash" );
var async = require( "async" );
var csv = require( "fast-csv" );

var TRAIN = "train";
var BUS = "bus";
var SYSTEM = "chicago-cta";
var STOPS = {};
var ROUTES = {};
var TRIPS = {};
var DOCUMENTS = [];

var FILE_OPTIONS = {
    encoding: "utf8"
};

var CSV_OPTIONS = {
    headers: true,
    quote: '"'
};


var onError = function ( done ) {

    return function ( err ) {

        done( err );

    };

};


var onSuccess = function ( done ) {

    return function () {
        done( null );
    };

};


var populateStops = function ( gtfsRoot ) {

    return function ( done ) {

        var parseStopInfo = function ( line ) {

            var directionMatch = line.stop_desc.match( /Northbound|Eastbound|Southbound|Westbound/ );

            var stop = {
                id: line.stop_id,
                name: line.stop_name,
                latitude: line.stop_lat,
                longitude: line.stop_lon,
                direction: directionMatch !== null ? directionMatch[ 0 ] : ""
            };

            STOPS[ line.stop_id ] = stop;

        };

        var csvStream = csv( CSV_OPTIONS );
        csvStream.on( "data", parseStopInfo );
        csvStream.on( "error", onError( done ) );
        csvStream.on( "end", onSuccess( done ) );

        var fileStream = fs.createReadStream( gtfsRoot + "/stops.txt", FILE_OPTIONS );
        fileStream.pipe( csvStream );

    };

};


var populateRoutes = function ( gtfsRoot ) {

    return function ( done ) {

        var routeTypes = {
            "1": TRAIN,
            "3": BUS
        };

        var parseRouteInfo = function ( line ) {

            var routeType = routeTypes[ line.route_type ];

            var route = {
                id: line.route_id,
                name: routeType === TRAIN ? line.route_long_name : line.route_short_name,
                type: routeType,
                stopIds: []
            };

            ROUTES[ line.route_id ] = route;

        };

        var csvStream = csv( CSV_OPTIONS );
        csvStream.on( "data", parseRouteInfo );
        csvStream.on( "error", onError( done ) );
        csvStream.on( "end", onSuccess( done ) );

        var fileStream = fs.createReadStream( gtfsRoot + "/routes.txt", FILE_OPTIONS );
        fileStream.pipe( csvStream );

    };

};


var populateTrips = function ( gtfsRoot ) {

    return function ( done ) {

        var parseTripInfo = function ( line ) {

            var trip = {
                routeId: line.route_id
            };

            TRIPS[ line.trip_id ] = trip;

        };

        var csvStream = csv( CSV_OPTIONS );
        csvStream.on( "data", parseTripInfo );
        csvStream.on( "error", onError( done ) );
        csvStream.on( "end", onSuccess( done ) );

        var fileStream = fs.createReadStream( gtfsRoot + "/trips.txt", FILE_OPTIONS );
        fileStream.pipe( csvStream );

    };

};


var addStopIdsToRoutes = function ( gtfsRoot ) {

    return function ( done ) {

        var parseStopTimeInfo = function ( line ) {

            var routeId = TRIPS[ line.trip_id ].routeId;

            if ( typeof ROUTES[ routeId ] === "undefined" ) {
                return;
            }

            ROUTES[ routeId ].stopIds.push( line.stop_id );

        };

        var csvStream = csv( CSV_OPTIONS );
        csvStream.on( "data", parseStopTimeInfo );
        csvStream.on( "error", onError( done ) );
        csvStream.on( "end", onSuccess( done ) );

        var fileStream = fs.createReadStream( gtfsRoot + "/stop_times.txt", FILE_OPTIONS );
        fileStream.pipe( csvStream );

    };

};


var buildStopDocuments = function ( done ) {

    var processRoute = function ( route ) {

        var addStopDocument = function ( stopId ) {
            DOCUMENTS.push( {
                type: route.type,
                route: route.name,
                direction: STOPS[ stopId ].direction,
                name: STOPS[ stopId ].name,
                latitude: STOPS[ stopId ].latitude,
                longitude: STOPS[ stopId ].longitude,
                system: SYSTEM
            } );
        };

        _.forEach( _.uniq( route.stopIds ), addStopDocument );

    };

    try {

        _.forEach( ROUTES, processRoute );

    } catch ( err ) {

        done( err );

    }

    done( null );

};


exports.run = function ( gtfsRoot, cb ) {

    var tasks = [
        populateStops( gtfsRoot ),
        populateRoutes( gtfsRoot ),
        populateTrips( gtfsRoot ),
        addStopIdsToRoutes( gtfsRoot ),
        buildStopDocuments
    ];

    async.series( tasks, function ( err ) {

        if ( err ) {
            return cb( err );
        }

        return cb( null );

    } );

};
