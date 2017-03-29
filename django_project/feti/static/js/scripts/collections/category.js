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
                q: '',
                coord: ''
            };

            if (q && q.length > 0) {
                parameters.q = q;
            }

            if (drawnLayers && drawnLayers.length > 0) {
                parameters.coord = drawnLayers;
            }

            if (Common.CurrentSearchMode == 'favorites') {
                if (q && q.length > 0)
                    parameters.coord = q;
            }

            this.url = this.url_template(parameters);
            this.url = this.url.replace(/&quot;/g, '"');

            if (parameters.q == "" && parameters.coord == "") {
                // check if last string is question mark
                if (this.url.slice('-1') == '?') {
                    this.url = this.url.replace('?', '/')
                }
            }

            this.reset();
            if (Common.FetchXHR != null) {
                Common.FetchXHR.abort();
            }

            that.last_query = q;
            Common.FetchXHR = this.fetch({
                success: function (collection, response) {
                    Common.FetchXHR = null;
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
                    Common.FetchXHR = null;
                    Common.Dispatcher.trigger('search:finish', false, that.mode, 0);
                    Common.Dispatcher.trigger('sidebar:update_title', 0, that.mode, parameters['coord']);
                }
            });
        },
        getRegex: function (character) {
            return new RegExp(character, 'gi');
        }
    });
});
