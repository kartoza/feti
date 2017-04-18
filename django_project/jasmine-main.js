var allTestFiles = []
var TEST_REGEXP = /(spec|test)\.js$/i

// Get a list of all the test files to include
Object.keys(window.__karma__.files).forEach(function (file) {
  if (TEST_REGEXP.test(file)) {
    // Normalize paths to RequireJS module names.
    // If you require sub-dependencies of test files to be loaded as-is (requiring file extension)
    // then do not normalize the paths
    //var normalizedTestModule = file.replace(".js", '')
    allTestFiles.push(file)
  }
})

require.config({
  basePath: 'feti/static',
  paths: {
        text: 'libs/text',
        common: 'common',
        bootstrap: 'libs/bootstrap.min',
        moment: 'libs/moment.min',
        leaflet: 'libs/Leaflet/1.0.3/leaflet',
        leafletExtraMarkers: 'libs/leaflet-extra-markers/leaflet.extra-markers',
        jquery: 'libs/jquery-1.11.3.min',
        jqueryUi: 'libs/jquery-ui-1.12.1.min',
        underscore: 'libs/underscore-1.8.3.min',
        backbone: 'libs/backbone-1.3.3.min',
        leafletDraw: 'libs/leaflet.draw-0.4.9/leaflet.draw',
        easyButton: 'libs/easy-button/easy-button',
        bootstrapSlider: 'libs/bootstrap-slider-9.7.2/bootstrap-slider',
        chosen: 'libs/chosen.jquery.min'
    },
    shim: {
        leaflet: {
            exports: 'L'
        },
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        leafletExtraMarkers: {
            deps: [
                'leaflet'
            ]
        },
        leafletDraw: {
            deps: [
                'leaflet'
            ]
        },
        chosen: {
            deps: [
                'jquery'
            ]
        },
        easyButton: {
            deps: [
                'leaflet'
            ]
        }
    },
    deps : allTestFiles,

    // we have to kickoff jasmine, as it is asynchronous
    callback: window.__karma__.start
})
