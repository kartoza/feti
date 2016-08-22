var MapView = Backbone.View.extend({
    template: _.template($('#map-template').html()),
    events: {
        'click #feti-map': 'clickMap',
        'click #back-home': 'exitFullScreen'
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
        this.animationSpeed = 400;

        this.mapContainerWidth = 0;
        this.mapContainerHeight = 0;

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
        var _map = this.map;

        if(!this.isFullScreen) {
            this.$mapContainer.css('padding-right', 0);
            this.$mapContainer.css('padding-left', 0);

            this.$navbar.hide();
            this.$header.slideUp(this.animationSpeed);
            this.$aboutSection.slideUp(this.animationSpeed);
            this.$partnerSection.hide();
            this.$footerSection.hide();

            this.$bodyContent.css('margin-top', '0');
            this.$bodyContent.css('height', '100%');

            this.$mapSection.css({
                'padding-top': '0',
                'padding-bottom': '0',
                'height': '100%'
            });

            d.width = '100%';
            d.height = '100%';

            this.$('.map-category').css({
                'border-top-left-radius': '0',
                'border-top-right-radius': '0'
            });

            this.mapContainerWidth = this.$mapContainer.width();
            this.mapContainerHeight = 600;

            this.$('#back-home').show();

            this.isFullScreen = true;

            this.$mapContainer.animate(d, this.animationSpeed, function() {
                _map._onResize();
            });
        }
    },
    exitFullScreen: function(e) {
        var d = {};
        var _map = this.map;

        console.log(this.isFullScreen);

        if(this.isFullScreen) {
            this.$mapContainer.css({
                'padding-right': '15px',
                'padding-left': '15px'
            });

            this.$navbar.show();
            this.$header.slideDown(this.animationSpeed);
            this.$aboutSection.slideDown(this.animationSpeed);
            this.$partnerSection.show();
            this.$footerSection.show();

            d.width = this.mapContainerWidth;
            d.height = this.mapContainerHeight;

            this.$mapSection.css({
                'padding-top': '50px',
                'padding-bottom': '50px',
                'height': this.mapContainerHeight + 100
            });

            this.$('.map-category').css({
                'border-top-left-radius': '8px',
                'border-top-right-radius': '8px'
            });

            this.$('#back-home').hide();

            this.isFullScreen = false;

            this.$mapContainer.animate(d, this.animationSpeed, function() {
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
