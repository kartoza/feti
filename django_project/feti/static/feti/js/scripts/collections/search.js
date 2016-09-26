/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/provider-view.js',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/views/occupation-view.js',
    '/static/feti/js/scripts/models/occupation.js',
], function (Common, ProviderView, Provider, OccupationView, Occupation) {

    var SearchCollection = Backbone.Collection.extend({
        model: Provider,
        views: [],
        provider_url_template: _.template("/api/campus?q=<%- q %>&<%- coord %>"),
        course_url_template: _.template("/api/course?q=<%- q %>&<%- coord %>"),
        occupation_url_template: _.template("/api/occupation?q=<%- q %>&<%- coord %>"),
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.views, function (view) {
                view.destroy();
            });
            $('#result-container').html("");
            this.views = [];
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

            this.model = Provider;
            if (mode == 'provider') {
                this.url = this.provider_url_template(parameters);
            } else if (mode == 'course') {
                this.url = this.course_url_template(parameters);
            } else if (mode == 'occupation') {
                this.model = Occupation;
                this.url = this.occupation_url_template(parameters);
            }

            this.url = this.url.replace(/&quot;/g, '"');

            this.reset();
            this.updateSearchTitle('0', mode, '');
            this.fetch({
                success: function (collection, response) {
                    if (mode == 'occupation') {
                        that.showing_map_cover(true);
                    } else {
                        that.showing_map_cover(false);
                    }
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false);
                    } else {
                        _.each(that.models, function (model) {
                            if (model.attributes.model == 'occupation') {
                                that.views.push(new OccupationView({
                                    model: model,
                                    id: "search_" + model.get('id'),
                                }));
                            } else {
                                that.views.push(new ProviderView({
                                    model: model,
                                    id: "search_" + model.get('id'),
                                }));

                            }
                        });
                        Common.Dispatcher.trigger('search:finish', true);
                    }
                    that.updateSearchTitle(that.models.length, mode, parameters['coord']);
                },
                error: function () {
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        },
        updateSearchTitle: function (number_result, mode, query) {
            $("#result-title-number").html(number_result);
            $("#result-title-mode").html(mode);
            if (query.indexOf("administrative") >= 0) {
                query = query.split("=")[1];
                query = query.split();
                query.reverse();
                $("#result-title-place").html('in ' + query.join().replace(",", ", "));
            } else if (query.indexOf("circle") >= 0) {
                var coordinates_index = query.indexOf("coordinate=") + "coordinate=".length;
                var radius_index = query.indexOf("&radius=");
                var coordinates = query.substring(coordinates_index, radius_index);
                radius_index = query.indexOf("&radius=") + "&radius=".length;
                var radius = parseInt(query.substring(radius_index, query.length));
                var coordinate = JSON.parse(coordinates);
                if (radius % 1000 > 1) {
                    radius = (radius % 1000) + " km"
                } else {
                    radius = radius + " meters"
                }
                $("#result-title-place").html('in radius ' + radius + ' from [' + coordinate['lat'].toFixed(3) + " , " + coordinate['lng'].toFixed(3) + "]");
            }
            else {
                $("#result-title-place").html('');
            }

        },
        showing_map_cover: function (showing) {
            var $cover = $('#shadow-map');
            if (showing) {
                if (!$cover.is(":visible")) {
                    $cover.fadeIn(200);
                }
            } else {
                if ($cover.is(":visible")) {
                    $cover.fadeOut(200);
                    $('#result-detail').hide("slide", {direction: "right"}, 500);
                }
            }
        }
    });

    return new SearchCollection();
});
