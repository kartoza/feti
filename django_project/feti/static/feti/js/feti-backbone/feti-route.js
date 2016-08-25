/**
 * Created by Christian Christelis <christian@kartoza.com> on 18/08/16.
 */

var mapView = mapView || {};
var loginModalView = loginModalView || {};
var searchBarView = searchBarView || {};
var is_logged_in = is_logged_in || false;

var AppRouter = Backbone.Router.extend({
    page_history: [],
    routes: {
        "": "landing_page",
        "login": "login_page",
        "map": "show_map",
        "map/:mode": "show_map",
        "map/:mode(/:results)": "show_map_results"
    },
    landing_page: function () {
        if (this.page_history.length > 0 && this.page_history[this.page_history.length - 1].match(/map.*/)) {
            searchBarView.exitFullScreen();
        } else if (this.page_history.length > 0 && this.page_history[this.page_history.length - 1].match(/login/)) {
            loginModalView.hide();
        }
        this.page_history.push(Backbone.history.getFragment());
    },
    show_map: function (mode) {
        loginModalView.hide();
        if (this.page_history.length == 0) {
            mapView.fullScreenMap(0);
        } else {
            mapView.fullScreenMap();
        }
        if (mode) {
            searchBarView.changeCategoryButton(mode);
        } else {
            searchBarView.changeCategoryButton("");
        }
        this.page_history.push(Backbone.history.getFragment());
    },
    login_page: function () {
        if (!is_logged_in) {
            loginModalView.show();
        }
        this.page_history.push(Backbone.history.getFragment());
    },
    back: function (own_route) {
        if (this.page_history.length > 0) {
            if (own_route == this.page_history[this.page_history.length - 1]) {
                this.navigate(this.page_history[this.page_history.length - 2], true);
            } else {
                this.navigate(this.page_history[this.page_history.length - 1], true);
            }
        } else {
            this.navigate('', true);
        }
    }
});

var app_router = new AppRouter;
// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();
