var fs = require( "fs" );


var basePath = "./lib/jobs";


var removeHidden = function ( file ) {

    return file[ 0 ] !== ".";

};


var addPath = function ( file ) {

    return basePath + "/" + file;

};


exports.run = function () {

    fs.readdir( ".", function ( err, files ) {

        console.log( files.filter( removeHidden ).map( addPath ) );

    } );

};
