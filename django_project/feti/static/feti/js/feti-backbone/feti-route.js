/**
 * Created by Christian Christelis <christian@kartoza.com> on 18/08/16.
 */

var AppRouter = Backbone.Router.extend({
    routes: {
        "": "landing_page",
        "login": "login_page",
        "/map/:mode": "show_map",
        "/map/:mode(/:results)": "show_map_results"
    }
});


var app_router = new AppRouter;

var loginModalView = loginModalView || {};

app_router.on('route:show_map', function (mode) {
    $('#introduction_carousel').hide();
    $('#introduction_text').hide();
    alert('here');
    //mapView.maximise();
});

app_router.on('route:login_page', function() {
   loginModalView.show();
});

// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();