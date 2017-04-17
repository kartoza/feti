// Require.js allows us to configure shortcut alias
require.config({
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
        }
    }
});

require([
    'routers/router',
    'common',
    'backbone',
    'jquery',
    'underscore'
], function (Workspace, Common, Backbone, $, _) {
    Common.Router = new Workspace();

    var $carousel = $('.carousel');
    $carousel.carousel({
        interval: 1000 * 5
    });

    var favorites = Common.Favorites;

    if(favorites) {
        favorites = favorites.replaceAll("&quot;", "\"");
        favorites = JSON.parse(favorites);
        var parsed_favorites = {};
        _.each(favorites, function (row) {
            parsed_favorites[row["campus"]] = row["courses"];
        });
        Common.Favorites = parsed_favorites;
    }

    Backbone.history.start();

    $(document).ready(function () {
        if (Common.EmbedVersion) {
            // for embed version
            var $toogleButton = $('#toogle-button');
            $toogleButton.click(function (event) {
                var $faButton = $toogleButton.find('.fa');
                Common.Dispatcher.trigger('toogle:result', event);
                if ($faButton.hasClass('fa-caret-left')) {
                    $faButton.removeClass('fa-caret-left');
                    $faButton.addClass('fa-caret-right');
                    $faButton.html("<span> Show Map</span>");
                    $toogleButton.attr('title', 'Hide side panel');
                } else {
                    $faButton.removeClass('fa-caret-right');
                    $faButton.addClass('fa-caret-left');
                    $faButton.html("<span> List Result</span>");
                    $toogleButton.attr('title', 'Show side panel');
                }
                $toogleButton.tooltip();
            });
        }

    });

});
