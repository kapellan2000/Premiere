//Open socket
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

//Generate UI
function generateButtons(){
	const object = {'File Save...': 'SaveVersion', 'File Save comment...': 'SaveComment', 'Prism settings' : 'Settings', 'Project Browser' : 'ProjectBrowser', 'Export' : 'Export'};
	var buttonHolder = document.getElementById("buttonHolder");
	var thisButton;
	var thisName;
	for (const [key, value] of Object.entries(object)){
		thisName = key
		thisButton = document.createElement("BUTTON");
		thisButton.innerHTML = thisName;
		thisButton.setAttribute("class", "scriptButton");
		//thisButton.setAttribute("id", 1);
		thisButton.setAttribute("path", "aaaa");
		thisButton.setAttribute("onclick", "buttonClick( '" + value + "' )");
		buttonHolder.appendChild(thisButton);
	}
}

// On click function
function buttonClick(argumentValue){
	var pythonExePath = "C:/Program Files/Prism2/Python39/python.exe";
	var scriptPath = "c:/ProgramData/Prism2/plugins/Premiere/Scripts/Prism_Premiere_MenuTools.py";
	var command = '"' + pythonExePath + '" "' + scriptPath + '" "' + argumentValue + '"';
	var exec = require('child_process').exec;
	exec(command)

		
}




