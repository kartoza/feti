/**
 * Created by meomancer on 08/08/16.
 */
var MapView = Backbone.View.extend({
    el: 'map',
    initialize: function () {
        this.render();
        this.listenTo(dispatcher, 'map:add_layer', this.add_layer);
        this.listenTo(dispatcher, 'map:remove_layer', this.remove_layer);
    },
    render: function () {
        this.map = L.map('feti-map').setView([-29, 20], 6);
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this.map);
    },
    add_layer: function (layer) {
        this.map.addLayer(layer);
    },
    remove_layer: function (layer) {
        this.map.removeLayer(layer);
    },
});
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
    initialize: function (self, container) {
        this.container = container;
        this.render();
    }
});

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
        this.model.render_marker();
    },
    initialize: function () {
        this.render();
    }
});
