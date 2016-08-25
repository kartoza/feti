define([
    '/static/feti/js/scripts/collections/courses.js'
], function (CourseCollection) {
    var CourseView = Backbone.View.extend({
        tagName: 'li',
        template: _.template('<%- _long_description %>'),
        container: "",
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
        },
        initialize: function () {
            this.render();
        }
    });

    return CourseView;
});
