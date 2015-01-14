var fs = require( "fs" );


exports.writeJSONFile = function ( path, data, done ) {

    return fs.writeFile( path, JSON.stringify( data ), done );

};
