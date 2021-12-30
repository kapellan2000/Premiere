(function () {
	'use strict';
	themeManager.init();
	var cs = new CSInterface();
	const net = require('net');
	const server = net.createServer((socket) => {
	  socket.on('data', (data) => {
		cs.evalScript('execute("'+ String(data) +'")', (ans)=>{
			socket.write(ans);
		})
	  });
	});
	server.maxConnections = 2;
	server.listen(9889);
	setTimeout(function(){
		generateButtons();
	}, 300);
	
}());

function generateButtons(){
	const object = {'File Save...': 'Save Version.cmd', 'File Save comment...': 'Save Extended.cmd', 'Prism settings' : 'Settings.cmd', 'Project Browser' : 'Project Browser.cmd', 'State Manager' : 'Export.cmd'};
	var buttonHolder = document.getElementById("buttonHolder");
	var thisButton;
	var thisName;
	for (const [key, value] of Object.entries(object)){

		thisName = key
		thisButton = document.createElement("BUTTON");
		thisButton.innerHTML = thisName;
		thisButton.setAttribute("class", "scriptButton");
		//thisButton.setAttribute("id", 1);
		//thisButton.setAttribute("path", "aaaa");
		thisButton.setAttribute("onclick", "buttonClick( '" + value + "' )");
		buttonHolder.appendChild(thisButton);
	}
}

function buttonClick(buttonElement){
	
	var root = 'C:\\Prism\\'
	var process = require('child_process');
	var exec = process.exec;
	var cmd = 'explorer '+root+'Plugins\\Apps\\Premiere\\'+buttonElement;

	exec(cmd, function(err, stdout, stderr) {

	});

}






