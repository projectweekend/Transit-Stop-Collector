exports.asyncError = function ( done ) {

    return function ( err ) {

        done( err );

    };

};


exports.asyncSuccess = function ( done ) {

    return function () {

        done( null );

    };

};
