/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/search.js',
    '/static/feti/js/scripts/models/search.js'
], function (Common, SearchResultView, SearchResult) {

    var SearchCollection = Backbone.Collection.extend({
        model: SearchResult,
        SearchResultViews: [],
        provider_url_template: _.template("/api/campus?q=<%- q %>"),
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.SearchResultViews, function (view) {
                view.destroy();
            });
            this.SearchResultViews = [];
            Common.Dispatcher.trigger('result:show');
        },
        getProvider: function (q) {
            var that = this;
            this.url = this.provider_url_template({q: q});
            this.fetch({
                success: function (collection, response) {
                    that.reset();
                    _.each(that.models, function (model) {
                        that.SearchResultViews.push(new SearchResultView({
                            model: model,
                            id: "search_" + model.get('id'),
                        }));
                    });
                },
                error: function () {
                    that.trigger('errorOnFetch');
                }
            });
        }
    });

    return new SearchCollection();
});
