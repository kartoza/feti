/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/search.js',
    '/static/feti/js/scripts/models/search.js'
], function (Common, SearchResultView, SearchResult) {

    var SearchCollection = Backbone.Collection.extend({
        model: SearchResult,
        SearchResultViews: [],
        provider_url_template: _.template("/api/campus?q=<%- q %>&coord=<%- coord %>"),
        course_url_template: _.template("/api/course?q=<%- q %>&coord=<%- coord %>"),
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.SearchResultViews, function (view) {
                view.destroy();
            });
            this.SearchResultViews = [];
        },
        search: function (mode, q, drawnLayers) {
            var that = this;
            var parameters = {
                q: q,
                coord: ''
            };

            if(drawnLayers.length > 0) {
                var coordinate = drawnLayers[0].getLatLngs();
                parameters.coord = JSON.stringify(coordinate);
            }

            if (mode == 'provider') {
                this.url = this.provider_url_template(parameters);
            } else if (mode == 'course') {
                this.url = this.course_url_template(parameters);
            }

            this.url = this.url.replace(/&quot;/g, '"');

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
