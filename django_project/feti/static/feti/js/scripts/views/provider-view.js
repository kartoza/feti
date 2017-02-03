define([
    'common',
    '/static/feti/js/scripts/models/provider.js',
    '/static/feti/js/scripts/views/provider-course-view.js',
    '/static/feti/js/scripts/models/course.js',
    'text!/static/feti/js/scripts/templates/provider-detail.html'
], function (Common, Provider, ProviderCourseView, Course, providerTemplate) {
    var ProviderView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-title',
        template: _.template(providerTemplate),
        courses_template: _.template('<div id="<%- id %>-courses" class="collapse"></div>'),
        container: '#result-container-provider',
        model: Provider,
        events: {
            'click': 'clicked',
            'click .favorites': 'addToFavorites',
            'click .gotomap': 'gotoMap'
        },
        clicked: function () {
            this.model.clicked();
        },
        addToFavorites: function (e) {
            if (!Common.IsLoggedIn) {
                alert('You need to log in first');
                return false;
            }
            // get id
            var id = this.model.attributes.id;
            var course_id = [];

            // get all courses id
            _.each(this.model.attributes.courses, function (course) {
                course_id.push(course.id);
            });

            if ($(e.target).hasClass('fa-star-o')) {
                // Add to favorites
                $.ajax({
                    url: 'profile/add-campus/',
                    type: 'POST',
                    data: JSON.stringify({
                        'campus': id,
                        'courses_id': course_id
                    }),
                    success: function (response) {
                        if (response == 'added') {
                            alert('Campus added to favorites');
                            Common.Dispatcher.trigger('favorites:added', 'provider');
                            $(e.target).removeClass('fa-star-o');
                            $(e.target).addClass('fa-star filled');

                            for (var i = 0; i < course_id.length; i++) {
                                $('#' + id + '-courses #favorite-course-' + course_id[i]).children().removeClass('fa-star-o');
                                $('#' + id + '-courses #favorite-course-' + course_id[i]).children().addClass('fa-star filled');
                            }
                        }
                    },
                    error: function (response) {
                        alert('Adding campus to favorites failed');
                    },
                    complete: function () {
                    }
                });

            } else if ($(e.target).hasClass('fa-star filled')) {
                // $(e.target).removeClass('fa-star filled');
                // $(e.target).addClass('fa-star-o');
                // Remove from favorites
            }

            return false;
        },
        gotoMap: function (event) {
            $('#toogle-button').click();
            this.clicked()
            event.stopPropagation();
            return false;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
            $(this.container).append(this.courses_template(this.model.attributes));
            this.$elCourses = $("#" + this.model.attributes.id + "-courses");
            // toogling
            this.$el.attr("href", "#" + this.model.attributes.id + "-courses");
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
                    campus_id: that.model.attributes.id,
                    container: "#" + that.model.attributes.id + "-courses"
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
