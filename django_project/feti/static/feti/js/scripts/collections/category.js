define([
    'common'
], function (Common) {
    return CategoryCollection = Backbone.Collection.extend({
        subviews: {},
        results: [],
        $result_title: $('#result-title'),
        url_all_template: _.template('/api/get-all-campus/?page=<%- page %>'),
        view: {},
        search_changed: true,
        currentPage: 0,
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
        getRegex: function (character) {
            return new RegExp(character, 'gi');
        },
        search: function (q, drawnLayers) {
            var that = this;
            var parameters = {
                q: '',
                coord: ''
            };

            var url_template = this.url_template;
            if (q && q.length > 0) {
                this.currentPage = 0;
                parameters.q = q;
            } else {
                url_template = this.url_all_template;
                parameters.page = this.currentPage + 1;
            }

            if (drawnLayers && drawnLayers.length > 0) {
                parameters.coord = drawnLayers;
            }

            if (Common.CurrentSearchMode == 'favorites') {
                if (q && q.length > 0)
                    parameters.coord = q;
            }

            this.url = url_template(parameters);
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
                    Common.Dispatcher.trigger('sidebar:update_title', that.results.length, that.mode, parameters['coord']);

                    //bind onscroll event
                    $(".result-container").unbind('scroll');
                    if (!q || q == "") {
                        $(".result-container").bind("scroll", function () {
                            if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
                                Common.Dispatcher.trigger('search:start');
                            }
                        })
                    }
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
            var currentIndex = 0;
            var indexes = {};
            var output = [];
            // check if it is pagination
            var is_pagination = false;
            if (response.constructor == Object && response['current_page']) {
                that.currentPage = parseInt(response['current_page']);
                response = response["campuses"];
                is_pagination = true;
            }

            /**
             * Parse each row
             */
            _.each(response, function (row) {
                var id = row['campus_id'];
                if (!(id in indexes)) {
                    var campusIsMarked = (model == "campus" && that.last_query != "");
                    var campus = that.campusParser(row, campusIsMarked, is_pagination);
                    if (campus) {
                        // put campus is success
                        indexes[id] = currentIndex;
                        currentIndex += 1;
                        output.push(campus);
                    }
                }

                /**
                 * Push course to campus course list
                 */
                var campusIndex = indexes[id];
                if (campusIndex != undefined) {
                    var courseIsMarked = (model == "course" && that.last_query != "");
                    that.courseParser(row, courseIsMarked, output[campusIndex]["courses"], is_pagination);
                }
            });
            return output;
        },
        campusParser: function (row, isMarked, isPagination) {
            /**
             * Create campus row if it is not presented
             */
            // parse campus location
            var id = row['campus_id'];
            var campus_is_favorite = id in Common.Favorites;
            var latlng = {};
            if (row["campus_location"]) {
                var location = row["campus_location"].split(",");
                latlng = {
                    "lat": parseFloat(location[0]),
                    "lng": parseFloat(location[1])
                };
                var campusTitle = row["campus_provider"];
                if (campusTitle && isMarked) {
                    campusTitle = campusTitle.replace(
                        this.getRegex(this.last_query), function (str) {
                            return '<mark>'
                            courseParser + str + '</mark>'
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
                    "model": 'campus',
                    "_campus_popup": row["campus_popup"],
                    "saved": campus_is_favorite
                };
                return campus;
            }
            return null;
        },
        courseParser: function (row, isMarked, campusOfCourse, isPagination) {
            /**
             * Create course if it is presented
             */
            var id = row['campus_id'];
            var campus_is_favorite = id in Common.Favorites;
            if (!isPagination) {
                var courseNldr = "";
                if (row["course_nlrd"]) {
                    courseNldr = "[" + row["course_nlrd"] + "] ";
                }
                var courseTitle = courseNldr + row["course_course_description"];
                if (isMarked) {
                    courseTitle = courseTitle.replace(
                        this.getRegex(this.last_query), function (str) {
                            return '<mark>' + str + '</mark>'
                        }
                    );
                }
                var saved = false;
                if (campus_is_favorite) {
                    saved = Common.Favorites[id].indexOf(row["course_id"]) >= 0;
                }
                var course = {
                    "id": row["course_id"],
                    "title": courseTitle,
                    "model": "course",
                    "saved": saved
                };
                campusOfCourse.push(course);
            } else {
                var cleanCourses = row["courses"].replace(this.getRegex("'"), "\"");
                cleanCourses = cleanCourses.replace(this.getRegex("'"), "\"");
                cleanCourses = cleanCourses.replace(this.getRegex(/\\/g), "");
                var courses = JSON.parse(cleanCourses);
                var coursesOutput = [];
                _.each(courses, function (course) {
                    var saved = false;
                    var attributes = course.split(";;");
                    if (campus_is_favorite) {
                        saved = Common.Favorites[id].indexOf(row["course_id"]) >= 0;
                    }
                    var courseOutput = {
                        "id": attributes[0].trim(),
                        "title": attributes[1].trim(),
                        "model": "course",
                        "saved": saved
                    };
                    campusOfCourse.push(courseOutput);
                });
            }
        }
    });
});
