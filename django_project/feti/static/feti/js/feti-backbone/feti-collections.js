/**
 * Created by meomancer on 08/08/16.
 */

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
var CampusCollection = Backbone.Collection.extend({
    model: Campus,
    campus_views: [],
    url: function () {
        return "/api/campuss/";
    }
});

