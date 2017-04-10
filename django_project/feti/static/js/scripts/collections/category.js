define([
    'common'
], function (Common) {
    return CategoryCollection = Backbone.Collection.extend({
        subviews: {},
        results: [],
        $result_title: $('#result-title'),
        url_template: '',
        search_changed: true,
        current_page: 1,
        load_more_enabled: false,
        mode: '',
        view: {},
        url: function () {
            return this.url;
        },
        reset: function () {
            if (this.search_changed) {
                _.each(this.results, function (view) {
                    view.destroy();
                });
                $('#result-container').html("");
                this.results = [];
            }
            this.search_changed = true;
        },
        search: function (q, drawnLayers) {
            var that = this;
            if (that.search_changed) {
                that.current_page = 1;
            }
            var parameters = {
                q: '',
                coord: '',
                page: that.current_page
            };
            if (q == Common.EmptyString) {
                q = '';
            }

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
            console.log(this.url);
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
                    var campus_count = that.results.length;
                    if (campus_count > 0) {
                        if (that.results[0].model.get('max')) {
                            campus_count = that.results.length + ' / ' + that.results[0].model.get('max');
                        }
                    }
                    Common.Dispatcher.trigger('sidebar:update_title', campus_count, that.mode, parameters['coord']);

                    that.load_more_enabled = false;
                    if ($.inArray(Common.CurrentSearchMode, Common.AllowPagingRequest) !== -1) {
                        if (that.models.length >= Common.limit_per_page) {
                            that.load_more_enabled = true;
                        }
                    }
                    that.enableLoadMore();
                    if (!that.load_more_enabled) {
                        Common.Router.is_initiated = true;
                    }
                },
                error: function () {
                    Common.FetchXHR = null;
                    Common.Dispatcher.trigger('search:finish', false, that.mode, 0);
                    Common.Dispatcher.trigger('sidebar:update_title', 0, that.mode, parameters['coord']);
                }
            });
        },
        enableLoadMore: function () {
            var that = this;
            if (that.load_more_enabled) {
                setTimeout(function () {
                    that.current_page += 1;
                    Common.Dispatcher.trigger('search:loadMore');
                }, 1000);
            }
        },
        getRegex: function (character) {
            return new RegExp(character, 'gi');
        }
    });
});
