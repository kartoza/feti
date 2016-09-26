/*global define*/
define([
    '/static/feti/js/scripts/views/map.js',
    '/static/feti/js/scripts/views/login.js',
    'common'
], function (MapView, LoginView, Common) {

    var AppRouter = Backbone.Router.extend({
        routes: {
            "": "landing_page",
            "login": "login_page",
            "map": "show_map",
            "map/:mode": "show_map",
            "map/:mode/:query": "show_map",
            "map/:mode/:query/:filter": "show_map",
            "map/:mode/:query/:filter/:pathway": "show_map",
        },
        initialize: function () {
            this.loginView = new LoginView();
            this.loginView.render();

            this.mapView = new MapView();
            this.mapView.render();

            this.pageHistory = [];
        },
        landing_page: function () {
            if (this.is_previous_route_match(/map.*/)) {
                this.mapView.exitAllFullScreen();
            } else if (this.is_previous_route_match(/login/)) {
                this.loginView.hide();
            }
            // Set 'where to study' clicked on landing page
            this.mapView.changeCategory(Common.CurrentSearchMode);

            this.pageHistory.push(Backbone.history.getFragment());
        },
        login_page: function () {
            if (!Common.IsLoggedIn) {
                this.loginView.show();
            }
            this.pageHistory.push(Backbone.history.getFragment());
        },
        is_previous_route_match: function (regex) {
            return this.pageHistory.length > 0 && this.pageHistory[this.pageHistory.length - 1].match(regex)
        },
        show_map: function (mode, query, filter, selected) {
            if (this.pageHistory.length == 0) {
                this.mapView.fullScreenMap(0);
            } else {
                this.mapView.fullScreenMap();
            }
            if (mode) {
                this.mapView.changeCategory(mode);
            } else {
                this.mapView.changeCategory(Common.CurrentSearchMode);
                mode = Common.CurrentSearchMode;
            }

            var selected_occupation = null;
            if (mode == 'occupation' && $.isNumeric(filter)) {
                selected_occupation = filter;
            }
            this.selected_occupation = selected_occupation;

            if (query) {
                this.mapView.search(mode, query, filter);
            } else {
                this.mapView.search(mode, '', '');
            }

            this.pageHistory.push(Backbone.history.getFragment());
        },
        show_map_without_filter: function (mode, query, selected, pathway) {
            console.log(selected);
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
