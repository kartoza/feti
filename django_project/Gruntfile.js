module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        requirejs: {
            compile: {
                options: {
                    baseUrl: 'feti/static/js',
                    mainConfigFile: 'feti/static/js/main.js',
                    name: 'libs/almond/almond',
                    include: ['main.js'],
                    out: 'feti/static/js/optimized.js'
                }
            }
        }

    });

    // Load plugins here.
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-requirejs');

    // Register tasks here.
    grunt.registerTask('default', ['requirejs']);
};
