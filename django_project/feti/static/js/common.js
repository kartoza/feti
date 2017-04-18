/*global define*/
'use strict';

define(['backbone', 'underscore'], function (Backbone, _) {
    return {
        IsLoggedIn: is_logged_in || false,
        IsLoginError: is_login_error || false,
        UserLocation: user_location || 'None',
        AllowPagingRequest: ['provider'],
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {},
        CurrentSearchMode: 'provider',
        FetchXHR: null,
        Favorites: favorites || null,
        EmbedVersion: typeof is_embed !== "undefined",
        DebugMode: is_debug_mode || false,
        limit_per_page: limit_per_page || 99999
    };
});
