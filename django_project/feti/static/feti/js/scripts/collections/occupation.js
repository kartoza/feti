/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/occupation-view.js',
    '/static/feti/js/scripts/models/occupation.js',
    '/static/feti/js/scripts/collections/category.js'
], function (Common, OccupationView, Occupation, Category) {
    var OccupationCollection = Category.extend({
        model: Occupation,
        provider_url_template: _.template("/api/occupation?q=<%- q %>"),
        initialize: function() {
            this.url_template = this.provider_url_template;
            this.view = OccupationView;
            this.mode = 'occupation';
        }
    });

    return new OccupationCollection();
});
