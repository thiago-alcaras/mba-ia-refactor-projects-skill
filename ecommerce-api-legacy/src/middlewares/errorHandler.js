function errorHandler(err, req, res, next) {
    console.error(`[ERROR] ${err.message}`, { stack: err.stack });

    const statusCode = err.statusCode || 500;
    const message = statusCode === 500 ? 'Internal Server Error' : err.message;

    res.status(statusCode).json({
        error: message,
        ...(process.env.NODE_ENV === 'development' && { details: err.message }),
    });
}

module.exports = errorHandler;
