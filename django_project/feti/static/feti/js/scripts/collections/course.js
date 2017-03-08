/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/courses-view.js',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/collections/category.js'
], function (Common, CourseView, Provider, Category) {
    var CourseCollection = Category.extend({
        model: Provider,
        provider_url_template: _.template("/api/course?q=<%- q %>&<%- coord %>"),
        initialize: function () {
            this.url_template = this.provider_url_template;
            this.view = CourseView;
            this.mode = 'course';
        },
        parse: function (response) {
            return this.campusCourseParser(response, "course");
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

            /**
             * Parse each row
             */
            _.each(response, function (row) {
                var id = row['campus_id'];
                var campus_is_favorite = id in Common.Favorites;
                if (typeof row['campus_popup'] == 'undefined') {
                    return true;
                }
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
                        "courses": [],
                        "model": model,
                        "_campus_popup": row["campus_popup"],
                        "saved": campus_is_favorite
                    };
                    if (row["campus_icon"] != "") {
                        campus["icon"] = 'media/' + row["campus_icon"];
                    }
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
                        that.getRegex(that.last_query), function (str) {
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
    return new CourseCollection();
});
