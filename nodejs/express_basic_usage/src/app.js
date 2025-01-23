const express = require("express");
const routes = require("./routes");

class App {
    constructor() {
        this.server = express();
        this.middlewares();
        this.routes();
    }

    middlewares() {
        this.server.use(express.json());
    }

    routes () {
        this.server.use(routes);
    }
}

// Export the server to be used by the other files
const app = new App();
module.exports = app.server;