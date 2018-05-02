<?php
include "session.php";
$sess = new Session();
$q1 = $sess->getRandQ(1);
$q2 = $sess->getRandQ(2);
$q3 = $sess->getRandQ(3);
$q4 = $sess->getRandQArr(4,4);
$q5 = $sess->getRandQ(5);
$warned = false;
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Practical 3 - Quiz</title>
        <link rel="stylesheet" type="text/css" href="text.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
        <script type="text/javascript">
            window.jQuery ||
            document.write('<script src="/jquery-1.9.1.min.js"><\/script>');
        </script>
    </head>
    <body style="background-image: url(stream.jpg);">
        <div id="mainBlock" class="container">
          <div class="row">
            <div id="q1" class="col-md-6">
              <h2>Question 1:</h2>
            <?php echo $q1['question'];?>
            <div id="True/False">
                False   <input id="radioF" class="radio" type="radio" value="0" name="t/f" checked>
                True    <input id="radioT" class="radio" type="radio" value="1" name="t/f">
                <div id="q1Reason"></div>
            </div>
            </div>
            <div id="q2" class="col-md-6">
            <h2>Question 2:</h2>
            <?php echo $q2['question'];?>
            <div id="multipleRadio">
                <?php echo $q2['wrong1'];?> <input id="radio<?php echo $q2['wrong1'];?>" class="radio" type="radio" name="multi" checked>
                <?php echo $q2['answer'];?> <input id="radio<?php echo $q2['answer'];?>" class="radio" type="radio" name="multi">
                <?php echo $q2['wrong2'];?> <input id="radio<?php echo $q2['wrong2'];?>" class="radio" type="radio" name="multi">
                <div id="q2Reason"></div>
            </div>
            </div>
            <div id="q3" class="col-md-6">
            <h2>Question 3:</h2>
            <?php echo $q3['question'];?>
            <div id="multipleCheck">
                <?php echo $q3['wrong2'];?>  <input id="check<?php echo $q3['wrong2'];?>" class="check" type="checkbox">
                <?php echo $q3['wrong1'];?>  <input id="check<?php echo $q3['wrong1'];?>" class="check" type="checkbox">
                <?php echo $q3['answer'];?>  <input id="check<?php echo $q3['answer'];?>" class="check" type="checkbox">
                <div id="q3Reason"></div>
            </div>
            </div>
            <div id="q4" class="col-md-6">
            <h2>Question 4:</h2>
            Match the irrational number to the symbol:
            <table id="matching" style="text-align: left">
                <tbody><tr>
                    <th><?php echo $q4[0]['question'];?></th>
                    <th><input id="num0" class="number" type="number" min="1" max="4" style="color:black"><br></th>
                    <th>1)<?php echo $q4[2]['answer'];?></th>
                    <th id="q4.1Reason"></th>
                </tr>
                <tr>
                    <th><?php echo $q4[1]['question'];?></th>
                    <th><input id="num1" class="number" type="number" min="1" max="4" style="color:black"><br></th>
                    <th>2)<?php echo $q4[3]['answer'];?></th>
                    <th id="q4.2Reason"></th>
                </tr>
                <tr>
                    <th><?php echo $q4[2]['question'];?></th>
                    <th><input id="num2" class="number" type="number" min="1" max="4" style="color:black"><br></th>
                    <th>3)<?php echo $q4[0]['answer'];?></th>
                    <th id="q4.3Reason"></th>
                </tr>
                <tr>
                    <th><?php echo $q4[3]['question'];?></th>
                    <th><input id="num3" class="number" type="number" min="1" max="4" style="color:black"><br></th>
                    <th>4)<?php echo $q4[1]['answer'];?></th>
                    <th id="q4.4Reason"></th>
                </tr>
            </tbody></table>
            </div>
            <div id="q5" class="col-md-6">
            <h2>Question 5:</h2>
            <?php echo $q5['question'];?>   <input id="short" class="text" type="text" style="color:black">
            <div id="q5Reason"></div><br>
            </div>
          </div>
            <input type="submit" class="short" onclick="mark()">
          <div id="user"></div>
          </div>
        </div>
        <script>
            var emptyFields = false;
            function mark(){
                       var emptyFields = false;
                for(var i=0; i<4; i++){
                    var match = document.getElementById("num"+i).value;
                    var box = document.getElementById("num"+i);
                    if (match>4 || match<1){
                        emptyFields = true;
                        box.style.backgroundColor = "yellow";
                        alert('Box '+(i+1)+' is empty');
                    }else{
                        box.style.backgroundColor = "white";
                    }
                }
                var short = document.getElementById("short").value;
                var box = document.getElementById("short");
                if (!short){
                    emptyFields = true;
                    alert("Question 5 is empty");
                    $warned = true;
                    box.style.backgroundColor = "yellow";
                }else{
                    box.style.backgroundColor = "white";
                }
                if(!emptyFields){
                    var score = 0;
                    var radioTrue = document.getElementById("radioT").checked;
                    if(radioTrue==<?php echo $q1['answer'];?>){
                       score++;
                    }else{
                       document.getElementById("q1Reason").innerHTML="Correct: <?php echo $q1['answer'];?>. Reason: <?php echo $q1['reason'];?>";
                    }
                    var radioMulti = document.getElementById("radio<?php echo $q2['answer'];?>");
                    if (radioMulti.checked){
                        score++;
                    }else{
                        document.getElementById("q2Reason").innerHTML="Correct: <?php echo $q2['answer'];?>. Reason: <?php echo $q2['reason'];?>";
                    }
                    var multi1 = document.getElementById("check<?php echo $q3['wrong2'];?>");
                    var multi2 = document.getElementById("check<?php echo $q3['wrong1'];?>");
                    var multi3 = document.getElementById("check<?php echo $q3['answer'];?>");
                    if (!multi1.checked && !multi2.checked && multi3.checked){
                        score++;
                    }else{
                        document.getElementById("q3Reason").innerHTML="Correct: <?php echo $q3['answer'];?>. Reason: <?php echo $q3['reason'];?>";
                    }
                    var lostAny = false;
                    var match1 = document.getElementById("num0").value;
                    var match2 = document.getElementById("num1").value;
                    var match3 = document.getElementById("num2").value;
                    var match4 = document.getElementById("num3").value;
                    if(match1!=3){
                        lostAny = true;   
                        document.getElementById("q4.1Reason").innerHTML="Correct: <?php echo $q4[0]['answer'];?>. Reason: <?php echo $q4[0]['reason'];?>";
                    }
                    if(match2!=4){
                        lostAny = true;   
                        document.getElementById("q4.2Reason").innerHTML="Correct: <?php echo $q4[1]['answer'];?>. Reason: <?php echo $q4[1]['reason'];?>";
                    }
                    if(match3!=1){
                        lostAny = true;   
                        document.getElementById("q4.3Reason").innerHTML="Correct: <?php echo $q4[2]['answer'];?>. Reason: <?php echo $q4[2]['reason'];?>";
                    }
                    if(match4!=2){
                        lostAny = true;   
                        document.getElementById("q4.4Reason").innerHTML="Correct: <?php echo $q4[3]['answer'];?>. Reason: <?php echo $q4[3]['reason'];?>";
                    }
                    if (!lostAny){
                        score++;
                    }
                    if(short.toLowerCase().trim() == "<?php echo $q5['answer'];?>"){
                        score++;
                    }else{
                        document.getElementById("q5Reason").innerHTML="Correct: <?php echo $q5['answer'];?>. Reason: <?php echo $q5['reason'];?>";
                    }
                    document.getElementById("user").innerHTML='<input type="button" value="Continue" onclick=\'window.location.href=\"enter.php\"\' />';
                    alert('score is '+score);
                }
            }
        </script>
    </body>
</html>