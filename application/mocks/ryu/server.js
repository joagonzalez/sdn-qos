const express = require('express')
const app = express()
const restRequestResponse = require('./rest-request-responses');

app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded());

app.post('/stats/flow/:flowid', (req, res) => {
  res.json(restRequestResponse.statsFlowById);
});

app.listen(8001, () => console.log('RyuMockServer::listen on port 8001'))
