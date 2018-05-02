var window, document;

function isBlank(inputField){
    return (inputField.value=="");
}

function isValidEmail_reg(email){
	var re = /^[2-9]$/;
	return re.test(email);
}

function makeRed(inputDiv){
	inputDiv.style.backgroundColor="#AA0000";
	inputDiv.parentNode.style.backgroundColor="#AA0000";
	inputDiv.parentNode.style.color="#FFFFFF";		
}
function makeClean(inputDiv){
	inputDiv.parentNode.style.backgroundColor="#FFFFFF";
	inputDiv.parentNode.style.color="#000000";		
}
window.onload = function(){
	var mainForm = document.getElementById("mainForm");
    var requiredInputs = document.querySelectorAll(".required");
	requiredInputs.forEach(function(input){
		input.onfocus = function(){
			this.style.backgroundColor = "#EEEE00";
		}
		input.onblur = function(){
			this.style.backgroundColor = "#FFFFFF";
		}
	});
	/*
    for (var i=0; i < requiredInputs.length; i++){
		requiredInputs[i].onfocus = function(){
			this.style.backgroundColor = "#EEEE00";
		}
    }
	*/
    mainForm.onsubmit = function(e){
		var requiredInputs = document.querySelectorAll(".required");
		requiredInputs.forEach(function(input) {
			if( isBlank(input) ){
				e.preventDefault();
				makeRed(input);
			}
			else{
				makeClean(input);
			}	
		});
		/*
		for (var i=0; i < requiredInputs.length; i++){
			if( isBlank(requiredInputs[i]) ){
				e.preventDefault();
				makeRed(requiredInputs[i]);
			}
			else{
				makeClean(requiredInputs[i]);
			}
		}
		*/
		var email = document.getElementById("email");
		if(!isValidEmail_reg(email.value)){
			e.preventDefault();
			makeRed(email);
		}
		else{
			makeClean(email);
            document.getElementById("email").get
            document.getElementById("movingDiv1").style.display="block";
		}

    }
}
