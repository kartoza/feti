var allTestFiles = []
var TEST_REGEXP = /(spec|test)\.js$/i

// Get a list of all the test files to include
Object.keys(window.__karma__.files).forEach(function (file) {
  if (TEST_REGEXP.test(file)) {
    // Normalize paths to RequireJS module names.
    // If you require sub-dependencies of test files to be loaded as-is (requiring file extension)
    // then do not normalize the paths
    // var normalizedTestModule = "feti/static/"+file;
      console.log(file);

  }
  allTestFiles.push(file);
})

require.config({
  basePath: '/base/src',
  paths: {
        text: 'feti/static/js/libs/text',
        common: 'feti/static/js/common',
        bootstrap: 'feti/static/js/libs/bootstrap.min',
        moment: 'feti/static/js/libs/moment.min',
        leaflet: 'feti/static/js/libs/Leaflet/1.0.3/leaflet',
        leafletExtraMarkers: 'feti/static/js/libs/leaflet-extra-markers/leaflet.extra-markers',
        jquery: 'feti/static/js/libs/jquery-1.11.3.min',
        jqueryUi: 'feti/static/js/libs/jquery-ui-1.12.1.min',
        underscore: 'feti/static/js/libs/underscore-1.8.3.min',
        backbone: 'feti/static/js/libs/backbone-1.3.3.min',
        leafletDraw: 'feti/static/js/libs/leaflet.draw-0.4.9/leaflet.draw',
        easyButton: 'feti/static/js/libs/easy-button/easy-button',
        bootstrapSlider: 'feti/static/js/libs/bootstrap-slider-9.7.2/bootstrap-slider',
        chosen: 'feti/static/js/libs/chosen.jquery.min'
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
