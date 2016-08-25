/*global define*/
define([
    '/static/feti/js/scripts/views/map.js',
    '/static/feti/js/scripts/views/login.js',
    'common'
], function (MapView, LoginView, Common) {

    var AppRouter = Backbone.Router.extend({
        routes: {
            "": "landing_page",
            "map/:mode": "show_map",
            "login": "login_page",
            "map/:mode(/:results)": "show_map_results"
        },
        initialize: function() {
            this.loginView = new LoginView();
            this.loginView.render();

            this.mapView = new MapView();
            this.mapView.render();

            this.pageHistory = [];
        },
        landing_page: function() {
            this.pageHistory.push(Backbone.history.getFragment());
        },
        login_page: function() {
            if (!Common.IsLoggedIn) {
                this.loginView.show();
            }
            this.pageHistory.push(Backbone.history.getFragment());
        },
        show_map: function(mode) {
            if(mode=='fullscreen') {
                if(this.pageHistory.length==0) {
                    this.mapView.fullScreenMap(0);
                } else {
                    this.mapView.fullScreenMap();
                }
            } else {
                this.mapView.exitFullScreen();
            }
            this.pageHistory.push(Backbone.history.getFragment());
        }
    });

	return AppRouter;
});
