/*global define*/
define([
    'scripts/views/map',
    'scripts/views/login',
    'common'
], function (MapView, LoginView, Common) {
    var history = [];
    var AppRouter = Backbone.Router.extend({
        parameters: {
            mode: 'provider',
            query: '',
            filter: '',
            pathway: ''
        },
        is_initiated: false,
        routes: {
            "": "landing_page",
            "login": "login_page",
            "map": "show_map",
            "map/": "show_map",
            "map/:mode/": "show_map",
            "map/:mode": "show_map",
            "map/:mode/:query": "show_map",
            "map/:mode/:query/:filter": "show_map",
            "map/:mode/:query/:filter/:pathway": "show_map",
            "map/:mode//:filter": "show_map_empty_query",
            "map/:mode//:filter/:pathway": "show_map_empty_query",
        },
        initialize: function () {
            this.loginView = new LoginView();
            this.loginView.render();

            this.mapView = new MapView();
            this.mapView.render();

            this.pageHistory = [];
            this.inOccupation = false;
        },
        landing_page: function () {
            if (this.is_previous_route_match(/map.*/)) {
                this.mapView.exitAllFullScreen();
            } else if (this.is_previous_route_match(/login/)) {
                this.loginView.hide();
            }
            // Set 'where to study' clicked on landing page
            this.mapView.changeCategory(Common.CurrentSearchMode);
            if (!this.is_initiated) {
                this.mapView.search(this.parameters.mode, this.parameters.query, this.parameters.filter);
            }

            this.pageHistory.push(Backbone.history.getFragment());

            // force to #map/provider/
            if (typeof is_embed !== "undefined") {
                this.navigate('map/provider/', true);
            }
        },
        login_page: function () {
            if (!Common.IsLoggedIn) {
                var last_route = this.pageHistory[this.pageHistory.length - 1];
                this.loginView.setLastRoute(last_route);
                this.loginView.show();
            }
            this.pageHistory.push(Backbone.history.getFragment());
        },
        get_latest_route: function () {
            if (this.pageHistory.length >= 2) {
                return this.pageHistory[this.pageHistory.length - 2]
            }
        },
        is_previous_route_match: function (regex) {
            return this.pageHistory.length > 0 && this.pageHistory[this.pageHistory.length - 1].match(regex)
        },
        show_map_empty_query: function (mode, filter, pathway) {
            this.show_map(mode, null, filter, pathway);
        },
        show_map: function (mode, query, filter, pathway) {
            if (!query) {
                query = "";
            }
            this.parameters = {
                mode: mode, query: query, filter: filter, pathway: pathway
            };

            if (this.pageHistory.length == 0) {
                this.mapView.fullScreenMap(0);
            } else {
                this.mapView.fullScreenMap();
            }
            Common.CurrentSearchMode = mode;
            if (mode) {
                if (mode == 'favorites' && !Common.IsLoggedIn) {
                    this.navigate('', true);
                } else {
                    this.mapView.changeCategory(mode);
                }
            } else {
                this.mapView.changeCategory(Common.CurrentSearchMode);
            }

            var selected_occupation = null;
            var selected_pathway = null;
            if (mode == 'occupation' && $.isNumeric(filter)) {
                selected_occupation = filter;
                if ($.isNumeric(pathway)) {
                    selected_pathway = pathway;
                }
            }
            this.selected_occupation = selected_occupation;
            this.selected_pathway = selected_pathway;

            if (this.selected_occupation && this.inOccupation) {
                Common.Dispatcher.trigger('search:finish', true);
            } else {
                this.mapView.search(mode, query, filter);
                this.inOccupation = false;
            }

            this.pageHistory.push(Backbone.history.getFragment());
        },
        show_map_without_filter: function (mode, query, selected, pathway) {
            this.show_map(mode, query, "", selected, pathway)
        },
        back: function (own_route) {
            if (this.pageHistory.length > 0) {
                if (own_route == this.pageHistory[this.pageHistory.length - 1]) {
                    this.navigate(this.pageHistory[this.pageHistory.length - 2], true);
                } else {
                    this.navigate(this.pageHistory[this.pageHistory.length - 1], true);
                }
            } else {
                this.navigate('', true);
            }
        }
    });

    return AppRouter;
});
