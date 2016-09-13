/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/provider-view.js',
    '/static/feti/js/scripts/models/provider.js'
], function (Common, ProviderView, Provider) {

    var SearchCollection = Backbone.Collection.extend({
        model: Provider,
        ProviderViews: [],
        provider_url_template: _.template("/api/campus?q=<%- q %>&<%- coord %>"),
        course_url_template: _.template("/api/course?q=<%- q %>&<%- coord %>"),
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.ProviderViews, function (view) {
                view.destroy();
            });
            this.ProviderViews = [];
        },
        search: function (mode, q, drawnLayers) {
            var that = this;
            var parameters = {
                q: q,
                coord: ''
            };

            if (drawnLayers && drawnLayers.length > 0) {
                parameters.coord = drawnLayers;
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
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false);
                    } else {
                        Common.Dispatcher.trigger('search:finish', true);
                        _.each(that.models, function (model) {
                            that.ProviderViews.push(new ProviderView({
                                model: model,
                                id: "search_" + model.get('id'),
                            }));
                        });
                    }
                },
                error: function () {
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        }
    });

    return new SearchCollection();
});
