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

            that.current_q = q;
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
                    Common.Dispatcher.trigger('search:finish');
                }
            });
        },
        campusCourseParser: function (response, model) {
            /**
             * This will parse response from server to readable website for campus-course.
             * Response is the list of campus-course entry
             * We parse it to be like old way
             */
            var that = this;
            var indexes = {};
            var output = [];
            var currentIndex = 0;
            var regex = new RegExp(that.current_q, 'gi');

            /**
             * Parse each row
             */
            _.each(response, function (row) {
                var id = row['campus_id'];
                var campus_is_favorite = id in Common.Favorites;
                if (!(id in indexes)) {
                    /**
                     * Create campus row if it is not presented
                     */
                    indexes[id] = currentIndex;
                    currentIndex += 1;

                    // parse campus location
                    var latlng = {};
                    if (row["campus_location"]) {
                        var location = row["campus_location"].split(",");
                        latlng = {
                            "lat": parseFloat(location[0]),
                            "lng": parseFloat(location[1])
                        }
                    }
                    var campusTitle = row["campus_provider"];
                    if (model == "campus") {
                        campusTitle = campusTitle.replace(
                            regex, function (str) {
                                return '<mark>' + str + '</mark>'
                            }
                        );
                    }
                    var campus = {
                        "id": row["campus_id"],
                        "campus": row["campus_campus"],
                        "location": latlng,
                        "title": campusTitle,
                        "icon": row["campus_icon"],
                        "courses": [],
                        "model": model,
                        "_campus_popup": row["campus_popup"],
                        "saved": campus_is_favorite
                    };
                    output.push(campus);
                }

                /**
                 * Push course to campus course list
                 */
                var courseNldr = "";
                if (row["course_nlrd"]) {
                    courseNldr = "[" + row["course_nlrd"] + "] ";
                }
                var courseTitle = courseNldr + row["course_course_description"];
                if (model == "course") {
                    courseTitle = courseTitle.replace(
                        regex, function (str) {
                            return '<mark>' + str + '</mark>'
                        }
                    );
                }
                var checkedIndex = indexes[id];
                var saved = false;
                if (campus_is_favorite) {
                    saved = Common.Favorites[id].indexOf(row["course_id"]) >= 0;
                }
                var course = {
                    "id": row["course_id"],
                    "title": courseTitle,
                    "model": model,
                    "saved": saved
                };
                output[checkedIndex]["courses"].push(course);
            });
            return output;
        },
    });
});
