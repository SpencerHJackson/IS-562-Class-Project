var mysql = require('mysql');

var con = mysql.createConnection({
  host: "rds-terraform.ccme3kf5lctp.us-east-2.rds.amazonaws.com",
  user: "admin",
  password: "is562section2classproject"
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

con.query("select * from student_employee", function (err, result) {
    if (err) throw err;
    console.log("Result: " + result);
  });