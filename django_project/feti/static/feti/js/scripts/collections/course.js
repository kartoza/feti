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
        }
    });
    return new CourseCollection();
});
