/*global define */
define([
    'common',
    'scripts/views/occupation-view',
    'scripts/models/occupation',
    'scripts/collections/category'
], function (Common, OccupationView, Occupation, Category) {
    var OccupationCollection = Category.extend({
        model: Occupation,
        provider_url_template: _.template("/api/occupation?q=<%- q %>"),
        initialize: function() {
            this.url_template = this.provider_url_template;
            this.view = OccupationView;
            this.mode = 'occupation';
        },
        parse: function (response, model) {
            return response['data'];
        }
    });

    return new OccupationCollection();
});
