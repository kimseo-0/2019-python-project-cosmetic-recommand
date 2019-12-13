const fileread = (file) => {
    var fs = require('fs');
    fs.readFile(file, 'utf8', function(err, data){
        console.log(data)
    });
  }

  fileread('test.txt')