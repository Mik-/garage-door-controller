module.exports = function(grunt) {

  require('load-grunt-config')(grunt, {
    data: {
      source_dir: 'app',
      release_dir: 'static',
      temp_dir: '.temp',
      bower_dir: 'app/bower_components',
    }
  });
};
