/*global define*/
'use strict';

define([], function () {
	return {
        IsLoggedIn: is_logged_in || false,
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {}
	};
});
