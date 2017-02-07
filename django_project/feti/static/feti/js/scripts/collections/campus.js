/*global define */
define([
    'common',
    '/static/feti/js/scripts/views/provider-view.js',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/collections/category.js'
], function (Common, ProviderView, Provider, Category) {

    var CampusCollection = Category.extend({
        model: Provider,
        provider_url_template: _.template("/api/campus?page=<%- page %>&q=<%- q %>&<%- coord %>"),
        initialize: function () {
            this.url_template = this.provider_url_template;
            this.view = ProviderView;
            this.mode = 'provider';
        },
        parse: function (response) {
            return this.campusCourseParser(response, "campus");
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

            /**
             * Parse each row
             */
            _.each(response, function (row) {
                var id = row['campus_id'];
                if (!(id in indexes)) {
                    var campusIsMarked = (model == "campus" && that.last_query != "");
                    var campus = that.campusParser(row, campusIsMarked);
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
                    that.courseParser(row, courseIsMarked, output[campusIndex]["courses"]);
                }
            });
            return output;
        },
        campusParser: function (row, isMarked) {
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
                            return '<mark>' + str + '</mark>'
                        }
                    );
                }
                var campus = {
                    "id": row["campus_id"],
                    "campus": row["campus"],
                    "provider": row["campus_provider"],
                    "location": latlng,
                    "title": campusTitle,
                    "icon": row["campus_icon"],
                    "courses": [],
                    "model": 'campus',
                    "address": row["campus_address"],
                    "website": row["campus_website"],
                    "saved": campus_is_favorite,
                    "campus_phone": row["campus_phone"],
                };
                return campus;
            }
            return null;
        },
        courseParser: function (row, isMarked, campusOfCourse) {
            /**
             * Create course if it is presented
             */
            var id = row['campus_id'];
            var campus_is_favorite = id in Common.Favorites;
            var cleanCourses = row["courses"].replace(this.getRegex("'"), "\"");
            cleanCourses = cleanCourses.replace(this.getRegex("'"), "\"");
            cleanCourses = cleanCourses.replace(this.getRegex(/\\/g), "");
            var courses = JSON.parse(cleanCourses);
            _.each(courses, function (course) {
                var saved = false;
                var attributes = course.split(";;");
                var course_id = attributes[0].trim();
                if (campus_is_favorite) {
                    saved = Common.Favorites[id].indexOf(parseInt(course_id)) >= 0;
                }
                var courseOutput = {
                    "id": course_id,
                    "title": attributes[1].trim(),
                    "model": "course",
                    "saved": saved
                };
                campusOfCourse.push(courseOutput);
            });
        }
    });

    return new CampusCollection();
});
