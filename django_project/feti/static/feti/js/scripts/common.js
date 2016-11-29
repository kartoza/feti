/*global define*/
'use strict';

define([], function () {
	return {
        IsLoggedIn: is_logged_in || false,
        UserLocation: user_location || 'None',
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {},
        CurrentSearchMode: 'provider',
        FetchXHR: null
	};
});
