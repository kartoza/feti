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
                    that.updateSearchTitle(that.models.length, that.mode, parameters['coord']);
                },
                error: function () {
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        },
        updateSearchTitle: function (number_result, mode, query) {
            this.$result_title.find('#result-title-'+mode).remove();

            var $result_title_number = $("<span>", {class: "result-title-number"});
            $result_title_number.html(number_result);

            var $result_title_mode = $("<span>", {class: "result-title-mode"});
            if(mode == 'occupation') {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  occupations': ' occupation');
            } else {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  campuses': ' campus');
            }

            var $result_title_campus = $("<div>", {id: "result-title-" + mode});
            $result_title_campus.append($result_title_number);
            $result_title_campus.append($result_title_mode);

            var $result_title_place = $("<span>", {class: "result-title-place"});

            if (query.indexOf("administrative") >= 0) {
                query = query.split("=")[1];
                query = query.split();
                query.reverse();
                $result_title_place.html(' in ' + query.join().replace(",", ", "));
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
                $result_title_place.html(' in radius ' + radius + ' from [' + coordinate['lat'].toFixed(3) + " , " + coordinate['lng'].toFixed(3) + "]");
            }
            else {
                $result_title_place.html('');
            }
            $result_title_campus.append($result_title_place);

            this.$result_title.append($result_title_campus);
        }
    });
});
