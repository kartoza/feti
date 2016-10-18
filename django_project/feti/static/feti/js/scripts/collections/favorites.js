/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/favorites-view.js',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/collections/category.js'
], function (Common, FavoritesView, Provider, Category) {

    var FavoritesCollection = Category.extend({
        model: Provider,
        provider_url_template: _.template("/api/saved-campus/"),
        initialize: function() {
            this.url_template = this.provider_url_template;
            this.view = FavoritesView;
            this.mode = 'favorites';
        }
    });

    return new FavoritesCollection();
});
