define([
    'common'
], function (Common) {
    return CategoryCollection = Backbone.Collection.extend({
        subviews: {},
        results: [],
        $result_title: $('#result-title'),
        url_template: '',
        mode: '',
        view: {},
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.results, function (view) {
                view.destroy();
            });
            $('#result-container').html("");
            this.results = [];
        },
        search: function (q, drawnLayers) {
            var that = this;
            var parameters = {
                q: q,
                coord: ''
            };

            if (drawnLayers && drawnLayers.length > 0) {
                parameters.coord = drawnLayers;
            }

            this.url = this.url_template(parameters);
            this.url = this.url.replace(/&quot;/g, '"');

            this.reset();
            this.fetch({
                success: function (collection, response) {
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false, that.mode, 0);
                    } else {
                        _.each(that.models, function (model) {
                            that.results.push(new that.view({
                                model: model,
                                id: "search_" + model.get('id')
                            }));
                        });
                        Common.Dispatcher.trigger('search:finish', true, that.mode, that.results.length);
                    }
                    Common.Dispatcher.trigger('sidebar:update_title', that.models.length, that.mode, parameters['coord']);
                },
                error: function () {
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        }
    });
});
