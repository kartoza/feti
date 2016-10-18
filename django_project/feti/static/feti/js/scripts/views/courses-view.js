define([
    'common',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/views/provider-course-view.js',
    '/static/feti/js/scripts/models/course.js'
], function (Common, Provider, ProviderCourseView, Course) {
    var ProviderView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-title',
        template: _.template('<img src="/static/feti/images/default-logo.png" width="54" height="54"/><div class="details"><h3><%- title %></h3><p class="courses"><%- counts %> courses <i class="fa fa-angle-down" aria-hidden="true"></i></p></div>'),
        courses_template: _.template('<div id="<%- id %>-courses-course" class="collapse"></div>'),
        container: '#result-container-course',
        model: Provider,
        events: {
            'click': 'clicked'
        },
        clicked: function () {
            this.model.clicked();
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
            $(this.container).append(this.courses_template(this.model.attributes));
            this.$elCourses = $("#" + this.model.attributes.id + "-courses-course");
            // toogling
            this.$el.attr("href", "#" + this.model.attributes.id + "-courses-course");
            this.$el.attr("data-toggle", "collapse");
            this.model.renderMarker();
            this.renderCourses();
        },
        renderCourses: function () {
            var that = this;
            var marker = that.model.get('marker');
            _.each(this.model.attributes.courses, function (course) {
                course.marker = marker;
                var model = new Course(course);
                that.courses.push(new ProviderCourseView({
                    model: model,
                    container: "#" + that.model.attributes.id + "-courses-course"
                }));
            });
        },
        initialize: function () {
            this.courses = [];
            this.render();
        },
        destroy: function () {
            this.model.destroy();
            this.model = null;
            // delete courses
            _.each(this.courses, function (course) {
                course.destroy();
            });
            this.courses = [];
            this.$el.remove();
            this.$elCourses.remove();
            return Backbone.View.prototype.remove.call(this);
        }
    });

    return ProviderView;
});
