/*global define*/
'use strict';

define(['backbone', 'underscore'], function (Backbone, _) {
    return {
        IsLoggedIn: is_logged_in || false,
        IsLoginError: is_login_error || false,
        UserLocation: user_location || 'None',
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {},
        CurrentSearchMode: 'provider',
        FetchXHR: null,
        Favorites: favorites || null,
        EmbedVersion: typeof is_embed !== "undefined"
    };
});
