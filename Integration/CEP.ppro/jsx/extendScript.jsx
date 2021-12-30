function execute(req){
	alert(req);
	try {  
	   ans = eval(req);
	}  
	catch (e) {  
	  ans = e.message;
	}  
	return (ans) 
}
