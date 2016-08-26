define([
    '/static/feti/js/scripts/collections/campuses.js',
    '/static/feti/js/scripts/collections/courses.js',
    '/static/feti/js/scripts/models/campus.js',
    '/static/feti/js/scripts/views/course.js'
], function (CampuseCollection, CourseCollection, Campus, CourseView) {
    var CampusView = Backbone.View.extend({
        tagName: 'li',
        template: _.template('<%- provider %><br><ul id="campus_course_<%- id %>" ></ul>'),
        container: '#providers',
        model: Campus,
        events: {
            'click': 'clicked'
        },
        clicked: function () {
            return false;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
            var that = this;
            this.course_collection = new CourseCollection({id: this.model.attributes.id});
            this.course_collection.fetch({
                success: function () {
                    _.each(that.course_collection.models, function (model) {
                        that.course_collection.course_views.push(new CourseView({
                            model: model,
                            id: "campus_" + that.model.attributes.id + "_course_" + model.get('id'),
                        }, "#campus_course_" + that.model.attributes.id));
                    });
                }
            });
            this.model.renderMarker();
        },
        initialize: function () {
            this.render();
        }
    });

    return CampusView;
});
