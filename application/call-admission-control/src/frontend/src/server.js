var express = require('express');
var path = require('path');
let app = express();

app.set('view engine', 'html');
app.set('views', 'src');

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
  });

app.use('/', express.static('GuiTopology', { index: false }));

app.get('*', (req, res, next) => {
    res.sendFile(path.join(__dirname, '/index.html'));
});
app.listen(3000, () => {
    console.log("listening on localhost:3000 (non-universal)");
});
