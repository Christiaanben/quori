<?php 
include "session.php";
$sess = new Session();
if($_SERVER['REQUEST_METHOD']=="POST"){
  if(isset($_POST["score"])){
    alert($_POST["score"]);
  }
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
  <title>Practical 3 - UsernameStuffs</title>
  <link rel="stylesheet" type="text/css" href="text.css">
</head>

<body style="background-image: url(stream.jpg);">
  <div id="mainBlock">
    <form name="userForm" onsubmit="return validate()" action="" method="post">
      <h2>Username:</h2>
      <input id="user" class="text" type="text" name="username">
      <h2>Password:</h2>
      <input id="pass" class="text" type="text" name="password">
      <input type="submit">
    </form>
    <div id='leaderB'>
      <?php $sess->getLeaderB();?>
    </div>
  </div>
</body>
<script>
  var regUser = /^[A-Z]+[a-zA-Z0-9]{4,14}$/;
  var regPass = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[,.!?])[A-Za-z\d,.!?]{8,}/;

  function validate() {
    var user = document.getElementById("user").value;
    var pass = document.getElementById("pass").value;
    if (!regUser.test(user)) {
      alert("username not valid");
      return false;
    }
    if (!regPass.test(pass)) {
      alert("password not valid");
      return false;
    }
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
      if (this.readyState ==4 && this.status == 200){
        document.getElementById("leaderB").innerHTML="";
        document.getElementById("leaderB").innerHTML=this.responseText;
      }
    };
    
    var url= "session.php";
    xhttp.open("POST","session.php?score="+(-1),true);
    xhttp.send();
  }
  
  
  
  
</script>

</html>