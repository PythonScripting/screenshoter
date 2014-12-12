var system = require('system');
var args = system.args;

if (args.length < 3) {
    console.error('Url or filename missing');
    phantom.exit(1);
}

var url = args[1];
var path = args[2];

console.log('Saving', url, 'to', path);

var page = require('webpage').create();

page.viewportSize = {
  width: 1024,
  height: 768
};

page.open(url, function() {
    page.render(path, { format: 'jpeg', quality: '30' });
    phantom.exit();
});

var killAfter = 60 * 1000;

setTimeout(function() {
    phantom.exit(1);
}, killAfter);
