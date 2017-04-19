/*global define*/
'use strict';

define(['backbone', 'underscore'], function (Backbone, _) {
    return {
        IsLoggedIn: typeof is_logged_in !== 'undefined',
        IsLoginError: typeof is_login_error !== 'undefined',
        UserLocation: typeof user_location !== 'undefined' ? user_location : 'None',
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {},
        CurrentSearchMode: 'provider',
        FetchXHR: null,
        Favorites: typeof favorites !== 'undefined' ? favorites : null,
        EmbedVersion: typeof is_embed !== "undefined",
        DebugMode: typeof is_debug_mode !== 'undefined'
    };
});
