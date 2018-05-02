<?php
class Session{
    private $db_host;
    private $db_name;
    private $db_user;
    private $db_pass; 
    private $db;
    
    function __construct(){
        $this->db_host = 'localhost';
        $this->db_name = 'prac3';
        $this->db_user = 'root';
        $this->db_pass = '';
        session_start();
        
        try{
            $this->db = new PDO("mysql:host=$this->db_host;dbname=$this->db_name",$this->db_user,$this->db_pass);
        }catch(PDOException $e){
            echo "Error: ".$e->getMessage();
            die();
        }
    }
    
    function getStatus(){
        return $this->db_user;
    }
    
    function getAll(){
        $sql = "SELECT * FROM `q_and_a`";
        $result = $this->db->query($sql);
        while ($row = $result->fetch()){
            echo $row['qID']." - ".$row['question']."<br>";
        }
    }
  
    function getLeaderB(){
      $sql = "SELECT * FROM `users` ORDER BY `score` DESC LIMIT 5";
      $result = $this->db->query($sql);
      while ($row = $result->fetch()){
            echo $row['username']." - ".$row['score']."<br>";
      }
    }
    
    function getRandQ($type){
        $sql = "SELECT * FROM `q_and_a` \n"
             . "WHERE type=".$type."\n"
             . "ORDER BY RAND()\n"
             . "LIMIT 1";
        $result = $this->db->query($sql);
        $row = $result->fetch();
        return $row;
    }
    
    function getRandQArr($type,$num){
        $sql = "SELECT * FROM `q_and_a` \n"
             . "WHERE type=".$type."\n"
             . "ORDER BY RAND()\n"
             . "LIMIT ".$num;
        $result = $this->db->query($sql);
        $qArr = array();
        while ($row = $result->fetch()){
            $qArr[] = $row;
        }
        return $qArr;
    }
}
?>