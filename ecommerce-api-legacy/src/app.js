const express = require('express');
const config = require('./config/settings');
const routes = require('./routes/index');
const errorHandler = require('./middlewares/errorHandler');
const { getDb } = require('./models/database');

const app = express();
app.use(express.json());

// Initialize database
getDb();

// Register routes
app.use(routes);

// Centralized error handling
app.use(errorHandler);

app.listen(config.port, () => {
    console.log(`LMS API running on port ${config.port}`);
});

module.exports = app;
