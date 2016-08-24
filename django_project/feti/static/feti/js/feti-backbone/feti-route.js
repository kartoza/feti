/**
 * Created by Christian Christelis <christian@kartoza.com> on 18/08/16.
 */

var AppRouter = Backbone.Router.extend({
    routes: {
        "": "landing_page",
        "map/:mode": "show_map",
        "login": "login_page",
        "/map/:mode(/:results)": "show_map_results"
    }
});

var app_router = new AppRouter;

var mapView = mapView || {};
var loginModalView = loginModalView || {};
var is_logged_in = is_logged_in || false;

var page_history = [];

app_router.on('route:landing_page', function(){
    if(page_history.length > 0 && page_history[page_history.length-1].match(/map.*/)) {
        mapView.exitFullScreen();
    }
    page_history.push(Backbone.history.getFragment());
});

app_router.on('route:show_map', function (mode) {
    if(mode=='fullscreen') {
        if(page_history.length==0) {
            mapView.fullScreenMap(0);
        } else {
            mapView.fullScreenMap();
        }
    } else {
        mapView.exitFullScreen();
    }
    page_history.push(Backbone.history.getFragment());
});

app_router.on('route:login_page', function() {
    if(!is_logged_in) {
        loginModalView.show();
    }
    page_history.push(Backbone.history.getFragment());
});

// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();
