/**
 * Created by Dimas on 4/17/17.
 */
// Requirejs Configuration Options
require.config({
    // to set the default folder

    // paths: maps ids with paths (no extension)
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
        chosen: 'libs/chosen.jquery.min',
        jasmine: ['libs/jasmine-2.5.2/jasmine'],
        jasmineHtml: ['libs/jasmine-2.5.2/jasmine-html'],
        boot: ['libs/jasmine-2.5.2/boot']
    },
    // shim: makes external libraries compatible with requirejs (AMD)
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
            ],
            exports: 'LeafletExtraMarkers'
        },
        leafletDraw: {
            deps: [
                'leaflet'
            ],
            exports: 'L.Draw'
        },
        chosen: {
            deps: [
                'jquery'
            ],
            exports: 'Chosen'
        },
        easyButton: {
            deps: [
                'leaflet'
            ],
            exports: 'EasyButton'
        },
        jasmine: {
            exports: 'jasmine'
        },
        jasmineHtml: {
            deps : ['jasmine'],
            exports: 'jasmine'
        },
        boot: {
            deps : ['jasmine', 'jasmineHtml'],
            exports: 'jasmine'
        }
    }
});

var specs = [
    'spec/MapSpec',
    'spec/SearchSpec'
];

require([
    'routers/router',
    'common',
    'backbone',
    'jquery',
    'underscore',
    'boot'
], function (Workspace, Common, Backbone, $, _) {
    Common.Router = new Workspace();

    Backbone.history.start();

    require(specs, function(){
        // Initialize the HTML Reporter and execute the environment (setup by `boot.js`)
        Common.Router.navigate('', true);
    })

});
