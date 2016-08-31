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
        course_url_template: _.template("/api/course?q=<%- q %>"),
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.SearchResultViews, function (view) {
                view.destroy();
            });
            this.SearchResultViews = [];
        },
        search: function (mode, q) {
            var that = this;
            if (mode == 'provider') {
                this.url = this.provider_url_template({q: q});
            } else if (mode == 'course') {
                this.url = this.course_url_template({q: q});
            }
            this.reset();
            this.fetch({
                success: function (collection, response) {
                    Common.Dispatcher.trigger('search:finish');
                    _.each(that.models, function (model) {
                        that.SearchResultViews.push(new SearchResultView({
                            model: model,
                            id: "search_" + model.get('id'),
                        }));
                    });
                },
                error: function () {
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        }
    });

    return new SearchCollection();
});
