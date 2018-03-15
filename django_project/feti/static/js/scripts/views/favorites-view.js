define([
    'common',
    'scripts/models/provider',
    'scripts/views/provider-course-view',
    'scripts/models/course',
    'text!scripts/templates/provider-detail.html',
    'backbone',
    'underscore',
    'jquery'
], function (
    Common,
    Provider,
    ProviderCourseView,
    Course,
    providerTemplate,
    Backbone,
    _,
    $
) {
    var FavoritesView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-title',
        template: _.template(providerTemplate),
        courses_template: _.template('<div id="<%- id %>-courses-favorites" class="collapse"></div>'),
        container: '#result-container-favorites',
        model: Provider,
        events: {
            'click': 'clicked',
            'click .favorites': 'deleteFavorite'
        },
        clicked: function () {
            this.model.clicked();
        },
        deleteFavorite: function (e) {
            if ($(e.target).hasClass('fa-star filled')) {
                // get id
                var id = this.model.attributes.id;
                var course_id = [];

                // get all courses id
                _.each(this.model.attributes.courses, function (course) {
                    course_id.push(course.id);
                });

                // Remove from favorites
                $.ajax({
                    url:'profile/delete-campus/',
                    type:'POST',
                    data: JSON.stringify({
                        'campus': id,
                        'courses_id': course_id
                    }),
                    success: function(response) {
                        if(response) {
                             var favorites = JSON.parse(response);
                             var parsed_favorites = {};
                            _.each(favorites, function (row) {
                                parsed_favorites[row["campus"]] = row["courses"];
                            });
                            Common.Favorites = parsed_favorites;
                            Common.Dispatcher.trigger('favorites:deleted', 'favorites');
                        }
                    },
                    error: function(response) {
                    },
                    complete: function() {
                    }
                });
            }

            return false;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
            $(this.container).append(this.courses_template(this.model.attributes));
            this.$elCourses = $("#" + this.model.attributes.id + "-courses-favorites");
            // toggling
            this.$el.attr("href", "#" + this.model.attributes.id + "-courses-favorites");
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
                    container: "#" + that.model.attributes.id + "-courses-favorites",
                    campus_id: that.model.attributes.id
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

    return FavoritesView;
});
