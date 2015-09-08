module.exports = {
  concat: {
    src: [
      '<%= bower_dir %>/font-awesome/css/font-awesome.css',
      '<%= temp_dir %>/css/app.css'
    ],
    dest: '<%= temp_dir %>/css/app.css'
  },

  copy: {
    files: [{
      expand: true,
      cwd: '<%= bower_dir %>/font-awesome/fonts',
      src: ['**/*'],
      dest: '<%= release_dir %>/fonts'
    }]
  }
}
