/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/courses-view.js',
    '/static/feti/js/scripts/models/provider.js'
], function (Common, CourseView, Provider) {

    var CourseCollection = Backbone.Collection.extend({
        model: Provider,
        courses: [],
        provider_url_template: _.template("/api/course?q=<%- q %>&<%- coord %>"),
        url: function () {
            return this.url;
        },
        reset: function () {
            _.each(this.courses, function (view) {
                view.destroy();
            });
            $('#result-container').html("");
            this.courses = [];
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

            this.model = Provider;
            this.url = this.provider_url_template(parameters);
            this.url = this.url.replace(/&quot;/g, '"');

            this.reset();
            this.updateSearchTitle('0', 'provider', '');
            this.fetch({
                success: function (collection, response) {
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false);
                    } else {
                        _.each(that.models, function (model) {
                            that.courses.push(new CourseView({
                                model: model,
                                id: "search_" + model.get('id')
                            }));
                        });
                        Common.Dispatcher.trigger('search:finish', true);
                    }
                    that.updateSearchTitle(that.models.length, 'provider', parameters['coord']);
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
        }
    });

    return new CourseCollection();
});
