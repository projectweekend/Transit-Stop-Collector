var async = require( "async" );
var cta = require( "./chicago-cta" );

var main = function() {

    var tasks = [ cta.bus.getRoutes, cta.bus.getDirections, cta.bus.getStops ];

    async.waterfall( tasks, function ( err, result ) {

        // TODO: send this to mongo
        console.log( result );

    } );

};


if ( require.main === module ) {

    main();

}
