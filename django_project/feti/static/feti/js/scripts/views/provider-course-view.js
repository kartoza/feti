define([
    'common',
    '/static/feti/js/scripts/models/course.js',
    'text!static/feti/js/scripts/templates/course-view.html'
], function (Common, Course, courseTemplate) {
    var CourseView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-row',
        template: _.template(courseTemplate),
        model: Course,
        events: {
            'click': 'clicked',
            'click .favorites': 'addToFavorites'
        },
        clicked: function () {
            this.model.clicked();
            return false;
        },
        addToFavorites: function (e) {
            if (!Common.IsLoggedIn) {
                alert('You need to log in first');
                return false;
            }

            var that = this;

            if($(e.target).hasClass('fa-star-o')) {
                // Add to favorites
                $.ajax({
                    url:'profile/add-campus/',
                    type:'POST',
                    data: JSON.stringify({
                        'campus': that.campus_id,
                        'courses_id': [that.model.id]
                    }),
                    success: function(response) {
                        if(response=='added') {
                            alert('Course and campus added to favorites');
                            Common.Dispatcher.trigger('favorites:added', 'provider');

                            $(e.target).removeClass('fa-star-o');
                            $(e.target).addClass('fa-star filled');

                            $('#search_'+that.campus_id+' #favorite-'+that.campus_id).children().removeClass('fa-star-o');
                            $('#search_'+that.campus_id+' #favorite-'+that.campus_id).children().addClass('fa-star filled');
                        }
                    },
                    error: function(response) {
                        alert('Adding course to favorites failed');
                    },
                    complete: function() {
                    }
                });

            } else if ($(e.target).hasClass('fa-star filled')) {
            }

            return false;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
        },
        initialize: function (options) {
            this.container = options.container;
            this.campus_id = options.campus_id;
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
