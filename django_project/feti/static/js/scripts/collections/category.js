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
            markers: L.featureGroup(),
            views: [],
            last_page: 1,
            finished: false,
            filtered: false
        },
        clearEmptyData: function () {
            this.empty_data = {
                markers: L.featureGroup(),
                views: [],
                last_page: 1,
                finished: false,
                filtered: false
            }
        },
        url: function () {
            return this.url;
        },
        reset: function () {
            if (this.search_changed) {
                var that = this;
                var filtered = that.empty_data['filtered'];

                if(filtered) {
                    this.clearEmptyData();
                }

                _.each(this.results, function (view) {
                    if(view.model) {
                        view.destroy();
                    }
                });

                Common.Dispatcher.trigger('map:removeLayer', this.empty_data['markers']);
                this.results = [];
                if (this.isAllowEmptySearch() && !filtered) {
                    if (this.last_query === "" && this.empty_data['views'].length > 0) {
                        _.each(this.empty_data['views'], function (view) {
                            that.results.push(view);
                        });
                        var layer = this.empty_data['markers'];
                        Common.Dispatcher.trigger('map:addLayer', layer);
                        Common.Dispatcher.trigger('map:repositionMapByLayer', layer);
                    } else if(this.empty_data['views'].length === 0) {
                        Common.Dispatcher.trigger('map:repositionMap', this.mode);
                    }
                }
            }
        },
        addMarkerOfEmptyData: function (marker) {
            this.empty_data['markers'].addLayer(marker);
        },
        isAllowEmptySearch: function () {
            return $.inArray(this.mode, Common.AllowPagingRequest) !== -1;
        },
        changeEmptyDataState: function (allow_to_empty_search, is_empty_search, increment_page) {
            // TODO : increment page in filter search
            var that = this;
            // check load more enabled
            that.load_more_enabled = false;
            if (is_empty_search && increment_page) {
                if (that.models.length >= Common.limit_per_page) {
                    that.load_more_enabled = true;
                } else {
                    that.empty_data['finished'] = true;
                }
                that.empty_data['last_page'] = that.current_page + 1;
            }

            if(!increment_page) {
                that.empty_data['last_page'] = 1;
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
                if (q === "") {
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

            if (Common.CurrentSearchMode === 'favorites') {
                if (q && q.length > 0)
                    parameters.coord = q;
            }

            if(parameters.coord) {
                parameters.page = 1;
                this.empty_data['filtered'] = true;
            } else {
                this.empty_data['filtered'] = false;
            }

            this.last_url = this.url;

            this.url = this.url_template(parameters);
            this.url = this.url.replace(/&quot;/g, '"');

            if (parameters.q === "" && parameters.coord === "") {
                // check if last string is question mark
                if (this.url.slice('-1') === '?') {
                    this.url = this.url.replace('?', '/')
                }
            }

            if (allow_to_empty_search && !is_empty_search && this.last_url === this.url) {
                return;
            }
            that.last_query = q;
            this.reset();
            if (Common.FetchXHR !== null) {
                Common.FetchXHR.abort();
            }

            if (this.last_query !== "") {
                $("#result-container-all-data").hide();
            }
            Common.FetchXHR = this.fetch({
                success: function (collection, response) {
                    // if change to empty search
                    // get old data
                    Common.FetchXHR = null;
                    var increment_page = true;
                    if (that.models.length === 0) {
                        Common.Dispatcher.trigger('search:finish', false, that.mode, 0);
                    } else {
                        _.each(that.models, function (model) {
                            var model_id;
                            if('id' in model) {
                                model_id = model.id;
                            } else {
                                model_id = model.get('id');
                            }
                            var data = {
                                model: model,
                                id: "search_" + model_id,
                                empty_search: false
                            };
                            data['empty_search'] = is_empty_search;
                            var view = new that.view(data);
                            that.results.push(view);
                            if (is_empty_search && !parameters['coord']) {
                                that.empty_data['views'].push(view);
                            }
                        });
                        Common.Dispatcher.trigger('search:finish', true, that.mode, that.results.length);
                        Common.Dispatcher.trigger('collections:finishCreate', that.results.length);
                    }
                    if(parameters['coord']) {
                        increment_page = false;
                    }
                    that.changeEmptyDataState(allow_to_empty_search, is_empty_search, increment_page);

                    // get campus count
                    var campus_count = that.results.length;
                    if (campus_count >= Common.limit_per_page && that.results[0].model.get('max')) {
                        campus_count = that.results.length + ' / ' + that.results[0].model.get('max');
                    }
                    Common.Dispatcher.trigger('sidebar:update_title', campus_count, that.mode, parameters['coord']);
                    if (!that.load_more_enabled) {
                        Common.Router.is_initiated = true;
                    }
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
            if (typeof character === 'string' || character instanceof String){
                return new RegExp(character, 'gi');
            }
            return new RegExp(character);
        }
    });
});
