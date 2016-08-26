/*global define */
define([
	'/static/feti/js/scripts/models/course.js'
], function (Course) {

    var CourseCollection = Backbone.Collection.extend({
        model: Course,
        course_views: [],
        url_template: _.template("/api/courses/<%- id %>"),
        initialize: function (options) {
            this.id = options.id;
        },
        url: function () {
            return this.url_template({id: this.id});
        }
    });

	return new CourseCollection();
});
