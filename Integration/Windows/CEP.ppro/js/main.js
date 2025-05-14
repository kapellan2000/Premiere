(function () {
    'use strict';
    themeManager.init();

    const net = require('net');
    const csInterface = new CSInterface(); 
    const server = net.createServer((socket) => {
        socket.on('data', (data) => {
            var command = data.toString().trim(); 

            csInterface.evalScript(command, function(result) {
                socket.write("Result: " + result); 
            });
        });
    });

    server.maxConnections = 2;
    server.listen(9889);

    setTimeout(function(){
        generateButtons();
    }, 300);
}());

var debug = 1;

//Generate UI
function generateButtons(){
	//const object = {'File Save...': 'Save Version.cmd', 'File Save comment...': 'Save Extended.cmd', 'Prism settings' : 'Settings.cmd', 'Project Browser' : 'Project Browser.cmd', 'Export' : 'Export.cmd'};

	let object;
	if (debug === 1) {
		object = {
			'File Save...': 'Save Version.cmd',
			'File Save comment...': 'Save Extended.cmd',
			'Prism settings': 'Settings.cmd',
			'Project Browser': 'Project Browser.cmd',
			'Export': 'Export.cmd'
		};
	} else {
		object = {
			'File Save...': 'SaveVersion',
			'File Save comment...': 'SaveComment',
			'Prism settings': 'Settings',
			'Project Browser': 'ProjectBrowser',
			'Export': 'Export'
		};
	}


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


	if (debug === 1) {
		var root = 'C:\\ProgramData\\Prism2'
		var process = require('child_process');
		var exec = process.exec;
		var cmd = 'explorer '+root+'\\plugins\\Premiere\\Integration\\dev\\'+argumentValue;

		exec(cmd, function(err, stdout, stderr) {
		});

	
	} else {
		var pythonExePath = "C:/Program Files/Prism2/Python311/python.exe";
		var scriptPath = "c:/ProgramData/Prism2/plugins/Premiere/Scripts/Prism_Premiere_MenuTools.py";
		var command = '"' + pythonExePath + '" "' + scriptPath + '" "' + argumentValue + '"';
		var exec = require('child_process').exec;
		exec(command)
	}
}






