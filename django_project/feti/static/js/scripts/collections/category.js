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
        empty_data: {
            models: [],
            last_page: 1,
            finished: false
        },
        url: function () {
            return this.url;
        },
        reset: function () {
            if (this.search_changed) {
                _.each(this.results, function (view) {
                    view.destroy();
                });
                this.results = [];
            }
        },
        isAllowEmptySearch: function () {
            return $.inArray(this.mode, Common.AllowPagingRequest) !== -1;
        },
        changeEmptyDataState: function (allow_to_empty_search, is_empty_search) {
            var that = this;
            // check load more enabled
            that.load_more_enabled = false;
            if (is_empty_search) {
                if (that.models.length % Common.limit_per_page == 0) {
                    that.load_more_enabled = true;
                } else {
                    that.empty_data['finished'] = true;
                }
                that.current_page = Math.floor(
                    that.empty_data['models'].length / Common.limit_per_page
                );
                that.empty_data['last_page'] = that.current_page + 1;
            }

        },
        search: function (q, drawnLayers) {
            var that = this;
            var allow_to_empty_search = false;
            var is_empty_search = false;

            if (that.search_changed) {
                that.current_page = 1;
            }

            // change if empty search
            if (this.isAllowEmptySearch()) {
                allow_to_empty_search = true;
                if (q == "") {
                    is_empty_search = true;
                    that.current_page = that.empty_data['last_page'];
                }
            }

            var parameters = {
                q: '',
                coord: '',
                page: that.current_page
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

            this.last_url = this.url;

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
            if (allow_to_empty_search && !is_empty_search && this.last_url == this.url) {
                return;
            }
            that.last_query = q;
            Common.FetchXHR = this.fetch({
                success: function (collection, response) {
                    // if change to empty search
                    // get old data
                    if (that.search_changed && is_empty_search) {
                        if (that.empty_data['finished']) {
                            that.models = [];
                        }
                        that.models = $.merge(that.models, that.empty_data['models']);
                        that.empty_data['models'] = [];
                    }

                    Common.FetchXHR = null;
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false, that.mode, 0);
                    } else {
                        _.each(that.models, function (model) {
                            var data = {
                                model: model,
                                id: "search_" + model.get('id'),
                                empty_search: false
                            };
                            data['empty_search'] = is_empty_search;
                            that.results.push(new that.view(data));
                            if (is_empty_search) {
                                that.empty_data['models'].push(model);
                            }
                        });
                        Common.Dispatcher.trigger('search:finish', true, that.mode, that.results.length);
                    }
                    that.changeEmptyDataState(allow_to_empty_search, is_empty_search)

                    // get campus count
                    var campus_count = that.results.length;
                    if (campus_count >= Common.limit_per_page && that.results[0].model.get('max')) {
                        campus_count = that.results.length + ' / ' + that.results[0].model.get('max');
                    }
                    Common.Dispatcher.trigger('sidebar:update_title', campus_count, that.mode, parameters['coord']);
                    Common.Router.is_initiated = true;
                    that.enableLoadMore();
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
                    Common.Dispatcher.trigger('search:loadMore');
                }, 1000);
            }
        },
        getRegex: function (character) {
            return new RegExp(character, 'gi');
        }
    });
});
