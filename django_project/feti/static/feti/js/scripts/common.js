/*global define*/
'use strict';

define([], function () {
    return {
        IsLoggedIn: is_logged_in || false,
        UserLocation: user_location || 'None',
        Dispatcher: _.extend({}, Backbone.Events),
        Router: {},
        CurrentSearchMode: 'provider',
        AllowPagingRequest: ['provider'],
        FetchXHR: null,
        Favorites: new_favorite,
        EmbedVersion: typeof is_embed !== "undefined",
        EmptyString: '<empty>',
        limit_per_page: limit_per_page || 99999
    };
});
