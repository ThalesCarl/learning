const express = require("express");

const server = express();

server.get("/white-rabbit", (req, res) => {
    return res.send("Wake up Neo");
});

server.get("/jason", (req, res) => {
    return res.json({'title': 'Friday, 13th'});
});

// Query params are optional parameters that must be provided using the
// following pattern: url.com/query-params?name=Jason&age=13
server.get("/query-params", (req, res) => {
    const name = req.query.name;
    const age = req.query.age;
    
    // Alternatively, we could do
    // const { name, age } = req.query;

    return res.json({
        title: 'booo',
        message: `Sup ${name}, what u doing? You're only ${age}.`
    });
});

// Route params are required params that must be provided using the
// following pattern: url.com/route-params/Jason
server.get("/route-params/:name", (req, res) => {
    const name = req.query.name;

    return res.json({'name': 'Jason'});
});
server.listen(3000);

