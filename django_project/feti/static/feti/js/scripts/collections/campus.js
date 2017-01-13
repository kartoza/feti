/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/provider-view.js',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/collections/category.js'
], function (Common, ProviderView, Provider, Category) {

    var CampusCollection = Category.extend({
        model: Provider,
        provider_url_template: _.template("/api/campus?q=<%- q %>&<%- coord %>"),
        initialize: function () {
            this.url_template = this.provider_url_template;
            this.view = ProviderView;
            this.mode = 'provider';
        },
        parse: function (response) {
            return this.campusCourseParser(response, "campus");
        }
    });

    return new CampusCollection();
});
