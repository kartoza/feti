/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/courses-view.js',
    '/static/feti/js/scripts/models/provider.js'
], function (Common, CourseView, Provider) {

    var CourseCollection = Backbone.Collection.extend({
        model: Provider,
        mode: 'course',
        courses: [],
        provider_url_template: _.template("/api/course?q=<%- q %>&<%- coord %>"),
        url: function () {
            return this.url;
        },
        count: function() {
            return this.courses.length;
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
            this.fetch({
                success: function (collection, response) {
                    if (that.models.length == 0) {
                        Common.Dispatcher.trigger('search:finish', false, that.mode, 0);
                    } else {
                        _.each(that.models, function (model) {
                            that.courses.push(new CourseView({
                                model: model,
                                id: "search_" + model.get('id')
                            }));
                        });
                        Common.Dispatcher.trigger('search:finish', true, that.mode, that.courses.length);
                    }
                    that.updateSearchTitle(that.models.length, that.mode, parameters['coord']);
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
            $result_title_mode.html(parseInt(number_result) > 1 ? '  campuses': ' campus');

            var $result_title_campus = $("<div>", {id: "result-title-" + mode});
            $result_title_campus.append($result_title_number);
            $result_title_campus.append($result_title_mode);

            $('#result-title').append($result_title_campus);
        }
    });

    return new CourseCollection();
});
