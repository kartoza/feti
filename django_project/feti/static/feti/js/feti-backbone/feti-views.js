var MapView = Backbone.View.extend({
    template: _.template($('#map-template').html()),
    events: {
        'click #feti-map': 'clickMap'
    },
    initialize: function() {
        this.$mapContainer = $('#map-container');
        this.$header = $('.intro-header');
        this.$aboutSection = $('.about-section');
        this.$partnerSection = $('.partner-section');
        this.$footerSection = $('footer');
        this.$mapSection = $('.map-section');
        this.$navbar = $('.navbar');
        this.$bodyContent = $("#content");
        this.isFullScreen = false;
        this.render();
    },
    render: function () {
        this.$el.html(this.template());
        this.map = L.map(this.$('#feti-map')[0]).setView([-29, 20], 6);
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this.map);

        this.$('#feti-map').parent().css('height', '100%');
    },
    add_layer: function (layer) {
        this.map.addLayer(layer);
    },
    remove_layer: function (layer) {
        this.map.removeLayer(layer);
    },
    clickMap: function (e) {
        this.fullScreenMap(e);
    },
    fullScreenMap: function(e) {
        var d = {};
        var speed = 400;
        var _map = this.map;

        if(!this.isFullScreen) {
            this.$mapContainer.css('padding-right', 0);
            this.$mapContainer.css('padding-left', 0);

            this.$navbar.hide();
            this.$header.slideUp(speed);
            this.$aboutSection.slideUp(speed);
            this.$partnerSection.hide();
            this.$footerSection.hide();

            this.$bodyContent.css('margin-top', '0');
            this.$bodyContent.css('height', '100%');

            this.$mapSection.css('padding-top', '0');
            this.$mapSection.css('padding-bottom', '0');
            this.$mapSection.css('height', '100%');

            d.width = '100%';
            d.height = '100%';

            this.isFullScreen = true;

            this.$mapContainer.animate(d, speed, function() {
                _map._onResize();
            });
        }
    }
});

var mapView = new MapView();
$('#map-container').append(mapView.el);
mapView.render();
mapView.map.invalidateSize();

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
    }
});
