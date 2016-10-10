/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/occupation-view.js',
    '/static/feti/js/scripts/models/occupation.js'
], function (Common, OccupationView, Occupation) {

    var OccupationCollection = Backbone.Collection.extend({
        model: Occupation,
        views: [],
        occupation_url_template: _.template("/api/occupation?q=<%- q %>"),
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
        search: function (q) {
            var that = this;
            var parameters = {
                q: q
            };

            this.url = this.occupation_url_template(parameters);
            this.url = this.url.replace(/&quot;/g, '"');

            this.reset();
            this.fetch({
                success: function (collection, response) {
                    that.showing_map_cover(true);
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false);
                    } else {
                        _.each(that.models, function (model) {
                            var view = new OccupationView({
                                model: model,
                                id: "search_" + model.get('id')
                            });
                            that.views.push(view);
                        });
                        Common.Dispatcher.trigger('search:finish', true);
                    }
                    that.updateSearchTitle(that.models.length, 'occupation', parameters['coord']);
                },
                error: function () {
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        },
        updateSearchTitle: function (number_result, mode, query) {
            $('#result-title').find('#result-title-'+mode).remove();

            var $result_title_number = $("<span>", {class: "result-title-number"});
            $result_title_number.html(number_result);

            var $result_title_mode = $("<span>", {class: "result-title-number"});
            $result_title_mode.html(parseInt(number_result) > 1 ? '  occupations': ' occupation');

            var $result_title_campus = $("<div>", {id: "result-title-" + mode});
            $result_title_campus.append($result_title_number);
            $result_title_campus.append($result_title_mode);

            $('#result-title').append($result_title_campus);
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

    return new OccupationCollection();
});
