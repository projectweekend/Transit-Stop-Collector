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
    systemId: String,
    systemCode: String
} );


TransitStopSchema.index( { route: 1, direction: 1, systemCode: 1, systemId: 1 } );


TransitStopSchema.statics.removeAll = function ( done ) {

    this.remove( {}, done );

};


TransitStopSchema.statics.removeBusChicagoCTA = function ( done ) {

    this.remove( { type: "bus", systemCode: "chicago-cta" }, done );

};


TransitStopSchema.statics.insertBulk = function ( documents, done ) {

    this.collection.insert( documents, done );

};


exports.TransitStop = mongoose.model( "TransitStop", TransitStopSchema );
