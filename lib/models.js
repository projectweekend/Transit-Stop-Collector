var mongoose = require( 'mongoose' );

var Schema = mongoose.Schema;
var ObjectId = Schema.ObjectId;


var TransitStopSchema = Schema ( {
    type: String,
    route: String,
    direction: String,
    name: String,
    latitude: Number,
    longitude: Number,
    system_id: String,
    system_code: String
} );


TransitStopSchema.index( { system_id: 1, system_code: 1 }, { unique: true } );
TransitStopSchema.index( { route: 1, direction: 1 } );


exports.TransitStop = mongoose.model( "TransitStop", TransitStopSchema );
