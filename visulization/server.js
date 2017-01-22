

/**
 * @author Camaro
 */
var express = require('express');
var http = require("http");
var bodyParser = require('body-parser');
var path = require("path");

var app = express();
var router = express.Router();
var port = process.env.PORT || (process.argv[2] != "mock" && process.argv[2]) || 3000;
var address = process.env.ADDRESS || process.argv[3] || "localhost";
var mock = process.argv[2] == "mock" || process.argv[4] == "mock" || false;

app.set('port', port);
app.set('statics', __dirname+'/statics');
app.use('/api', router);
app.use(express.static('statics'));
app.use(bodyParser.json());
router.use(bodyParser.json());

const leftStart = 0;
const topStart = 0;
const leftEnd = 631;
const topEnd = 404;
const pointSize = 5;

var wolves = [
    {
        "id": 1,
        "x": 133,
        "y": 312,
        "type": "ALPHA"
    },
    {
        "id": 2,
        "x": 400,
        "y": 131,
        "type": "BETA"
    },
    {
        "id": 3,
        "x": 133,
        "y": 234,
        "type": "DELTA"
    },
];


var map = {};

function updatePositions(wolves) {
    return wolves.map(function(wolve) {
        wolve.x = ( wolve.x + 10 ) % leftEnd;
        wolve.y = ( wolve.y + 10 ) % topEnd;
        return wolve;
    });
}

router.post('/map', function(req, res) {

    console.log(req.body);
    map = req.body;
    console.log("new map = ", map);
    res.json({"status" : "ok"});
});

router.route("/wolf/:id")
    .post(function(req, res){
        console.log("POST WOLF(%s)", req.params.id);
        console.log(req.body);
        wolves[req.params.id] = req.body;
        res.json({"status" : "ok"}); })
    .get(function(req, res) {
        res.json(wolves[req.params.id]);
    });

router.post('/wolf', function(req, res) {
    console.log("POST WOLVES");
    wolves = req.body;
    res.json({"status": "ok"});
});

router.get('/map', function(req, res) {
    console.log("GET map");
    res.json(map);
});


router.get('/wolf', function(req, res) {
    if (mock) {
        console.log("mocking mode: updating positions");
        wolves = updatePositions(wolves);
    }
    res.json(wolves);
});



app.listen(port, address, function(){
    if (mock) {
        console.log("Running in mocking mode");
    }
    console.log("Listening on address %s on port %s", address, port);
});

