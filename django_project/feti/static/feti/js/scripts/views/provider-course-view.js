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
            'click .favorites': 'favoriteClicked'
        },
        clicked: function () {
            this.model.clicked();
            return false;
        },
        favoriteClicked: function (e) {
            if (!Common.IsLoggedIn) {
                alert('You need to log in first');
                return false;
            }

            var that = this;

            if($(e.target).hasClass('fa-star-o')) {
                this.addToFavorites(e, that.campus_id, [that.model.id]);
            } else if ($(e.target).hasClass('fa-star filled')) {
                this.removeFromFavorites(e, that.campus_id, [that.model.id]);
            }

            return false;
        },
        addToFavorites: function (e, campus_id, courses_id) {
            $.ajax({
                url:'profile/add-campus/',
                type:'POST',
                data: JSON.stringify({
                    'campus': campus_id,
                    'courses_id': courses_id
                }),
                success: function(response) {
                    if(response=='added') {
                        alert('Course and campus added to favorites');
                        Common.Dispatcher.trigger('favorites:added', Common.CurrentSearchMode);

                        $(e.target).removeClass('fa-star-o');
                        $(e.target).addClass('fa-star filled');

                        $('#search_'+campus_id+' #favorite-'+campus_id).children().removeClass('fa-star-o');
                        $('#search_'+campus_id+' #favorite-'+campus_id).children().addClass('fa-star filled');
                    }
                },
                error: function(response) {
                    alert('Adding course to favorites failed');
                },
                complete: function() {
                }
            });
        },
        removeFromFavorites: function (e, campus_id, courses_id) {
            var mode = Common.CurrentSearchMode;
            if (mode != 'favorites') {
                return false;
            }
            var deleteConfirmation = confirm("Delete this course?");
            if(deleteConfirmation) {
                // Remove from favorites
                $.ajax({
                    url:'profile/delete-campus/',
                    type:'POST',
                    data: JSON.stringify({
                        'campus': campus_id,
                        'courses_id': courses_id
                    }),
                    success: function(response) {
                        if(response=='deleted') {
                            Common.Dispatcher.trigger('favorites:deleted', Common.CurrentSearchMode);
                            if(Common.CurrentSearchMode != 'favorites') {
                                $(e.target).addClass('fa-star-o');
                                $(e.target).removeClass('fa-star filled');

                                var course_saved_remaining = $('#'+campus_id+'-courses-course').children().find('.fa-star').length;

                                if(course_saved_remaining == 0) {
                                    $('#favorite-'+campus_id).removeClass('fa-star filled');
                                    $('#favorite-'+campus_id).removeClass('fa-star-o');
                                }
                            }
                        }
                    },
                    error: function(response) {
                    },
                    complete: function() {
                    }
                });
            }
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
