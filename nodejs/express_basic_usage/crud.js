const express = require("express");
const server = express();

// Makes the server able to handle json requests
server.use(express.json());

let customers = [
    { id: 1, name: "Jason", site: "http:/friday13th.com"},
    { id: 2, name: "Freddy", site: "http:/elmerstreetnightmare.com"},
    { id: 3, name: "UOL", site: "http:/uol.com.br"},
];

server.get("/customers", (req, res) => {
    return res.json(customers);
});

server.get("/customers/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const customer = customers.find(item => item.id === id);
    const status = customer ? 200 : 404;
    return res.status(status).json(customer);
});

server.post("/customers", (req, res) => {
    const { name, site } = req.body;
    const id = customers[customers.length - 1].id + 1;

    const newCustomer = { id, name, site };
    customers.push(newCustomer);
    return res.status(201).json(newCustomer);
});

server.put("/customers/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const { name, site } = req.body;

    const index = customers.findIndex(item => item.id === id);
    const status = index >= 0 ? 200 : 404;

    if (index >=0) {
        customers[index] = { id, name, site };
    }
    return res.status(status).json(customers[index]);
});

server.delete("/customers/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const index = customers.findIndex(item => item.id === id);
    const status = index >= 0 ? 200 : 404;

    if (index >=0) {
        customers.splice(index, 1);
    }
    return res.status(status).json();
});

server.listen(3000);