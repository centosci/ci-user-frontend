var app = require('../server');
var ip = process.env.IP  || '0.0.0.0';
var port = process.env.PORT || 3001;

app.listen(port, ip, function() {
 console.log('running at ' + ip + ':' + port);
});