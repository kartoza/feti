/*global define */
define([
    'common',
    'scripts/views/favorites-view',
    'scripts/models/provider',
    'scripts/collections/category'
], function (Common, FavoritesView, Provider, Category) {

    var FavoritesCollection = Category.extend({
        model: Provider,
        provider_url_template: _.template("/api/saved-campus/?<%- coord %>"),
        initialize: function() {
            this.url_template = this.provider_url_template;
            this.view = FavoritesView;
            this.mode = 'favorites';
        }
    });

    return new FavoritesCollection();
});
