var MapView = Backbone.View.extend({
    template: _.template($('#map-template').html()),
    events: {
        'click #feti-map': 'clickMap'
    },
    initialize: function () {
        this.$mapContainer = $('#map-container');
        this.$header = $('.intro-header');
        this.$aboutSection = $('.about-section');
        this.$partnerSection = $('.partner-section');
        this.$footerSection = $('footer');
        this.$mapSection = $('.map-section');
        this.$navbar = $('.navbar');
        this.$bodyContent = $("#content");
        this.isFullScreen = false;
        dispatcher.on('map:add_layer', this.add_layer, this);
        dispatcher.on('map:remove_layer', this.remove_layer, this);
        this.render();
    },
    render: function () {
        this.$el.html(this.template());
        $('#map-container').append(this.$el);
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
    fullScreenMap: function (e) {
        var d = {};
        var speed = 400;
        var _map = this.map;
        var that = this;

        if (!this.isFullScreen) {
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

            this.$mapContainer.animate(d, speed, function () {
                _map._onResize();
                that.isFullScreen = true;
                dispatcher.trigger('map:resize', true);
            });
        }
    }
});

var mapView = new MapView();
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


var SearchBarView = Backbone.View.extend({
    tagName: 'div',
    container: '#map-search',
    template: _.template('\
        <form action="map" method="POST">\
            <div class="search-category">\
                <span class="map-question"">\
                    What are you looking for?\
                </span>\
                <span class="m-button map-option" id="where-to-study">\
                    Where to study\
                </span>\
                <span class="m-button map-option" id="what-to-study">\
                    What to study\
                </span>\
                <span class="m-button map-option" id="choose-occupation">\
                    Choose occupation\
                </span>\
            </div>\
            <div class="search-bar">\
                <span id="search-bar" class="right-inner-addon">\
                   <i class="icon-search fa fa-search"></i>\
                   <input type="search"\
                           class="form-control"\
                           placeholder="Search" />\
                </span>\
                <span class="m-button map-option" id="where-to-study">\
                    Location\
                </span>\
                <span class="m-button map-option" id="what-to-study">\
                    Draw a shape\
                </span>\
                <span class="m-button map-option" id="choose-occupation">\
                    Travel line\
                </span>\
            </div>\
        </form>'),
    events: {
        'click #where-to-study': 'category_clicked',
        'click #what-to-study': 'category_clicked',
        'click #choose-occupation': 'category_clicked'
    },
    category_clicked: function (event) {
        this.change_category(event.target);
        mapView.fullScreenMap();
    },
    initialize: function () {
        this.render();
        dispatcher.on('map:resize', this.map_resize, this);
        this.$search_bar = $(".search-bar");
        this.search_bar_hidden = true;
    },
    render: function () {
        this.$el.empty();
        this.$el.html(this.template());
        $(this.container).append(this.$el);
    },
    category_selected: function () {
        var button = this.$el.find('.search-category').find('.m-button.active');
        if (button[0]) {
            return $(button[0]).html();
        } else {
            return null;
        }
    },
    change_category: function (button) {
        this.$el.find('.search-category').find('.m-button').removeClass('active');
        $(button).addClass('active');
        if (mapView.isFullScreen) {
            this.show_search_bar();
        }
    },
    map_resize: function (is_resizing) {
        if (is_resizing) {
            this.show_search_bar();
        }
    },
    show_search_bar: function () {
        if (this.search_bar_hidden && this.category_selected()) {
            this.$search_bar.slideToggle(500);
            // zoom control animation
            var $zoom_control = $('.leaflet-control-zoom');
            $zoom_control.animate({
                marginTop: '+=55px'
            }, 500);

            // now it is shown
            this.search_bar_hidden = false;
        }
    },
});

new SearchBarView();