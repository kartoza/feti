define([
    'common',
    '/static/feti/js/scripts/models/course.js'
], function (Common, Course) {
    var CourseView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-row',
        template: _.template('<strong><%- national_learners_records_database %></strong> <%- _long_description %>'),
        model: Course,
        events: {
            'click': 'clicked'
        },
        clicked: function () {
            this.model.clicked();
            return false;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
        },
        initialize: function (options) {
            this.container = options.container;
            this.render();
        },
        destroy: function () {
            this.model.destroy();
            this.model = null;
            this.$el.remove();
            return Backbone.View.prototype.remove.call(this);
        }
    });

    return CourseView;
});
