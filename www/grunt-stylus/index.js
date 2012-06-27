/*
 * stylus task for grunt
 * Copyright (c) 2012 Greg Smith
 * This work is public domain.
 */

module.exports = function(grunt) {

  var stylus = require("stylus");

  grunt.registerMultiTask("stylus", "Compile Stylus files.", function() {
    var dest = this.file.dest;
    var files = grunt.file.expandFiles(this.file.src);
    files.forEach(function(fileName) {
      var str = grunt.file.read(fileName);
      var newFileName = fileName.match(/(\w+)\.styl/)[1] + ".css";
      var newFilePath = dest + "/" + newFileName;
      stylus(str)
        .include(dest)
        .set("filename", newFileName)
        .render(function(err, css){
          if (err) {
            grunt.warn(err.message);
          }
          else {
            grunt.file.write(newFilePath, css);
            grunt.log.writeln("File \"" + newFilePath + "\" created.");
          }
        }
      );
    });
  });

};