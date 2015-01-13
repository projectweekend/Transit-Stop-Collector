var fs = require( "fs" );
var async = require( "async" );
var nomnom = require( "nomnom" );
var cta = require( "./chicago-cta" );


var writeJSONFile = function ( path, data, done ) {

    return fs.writeFile( path, JSON.stringify( data ), done );

};


var main = function() {

    var options = nomnom.option( "file", {
                abbr: "f",
                default: null,
                help: "Path to output file for JSON export"
            } )
            .parse();

    var tasks = [
        cta.bus.getRoutes,
        cta.bus.getDirections,
        cta.bus.getStops
    ];

    async.waterfall( tasks, function ( err, result ) {

        if ( options.file ) {
            writeJSONFile( options.file, result, function ( err ) {

                if ( err ) {
                    console.log( "Error generating JSON file" );
                } else {
                    console.log( "JSON file complete" );
                }

            } );
        } else {
            console.log( "TODO: send this to mongo" );
        }

    } );

};


if ( require.main === module ) {

    main();

}
