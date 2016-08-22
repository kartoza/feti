var MapView = Backbone.View.extend({
    template: _.template($('#map-template').html()),
    events: {
        'click #feti-map': 'clickMap',
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
        dispatcher.on('map:addLayer', this.addLayer, this);
        dispatcher.on('map:removeLayer', this.removeLayer, this);
        this.animationSpeed = 400;

        this.mapContainerWidth = 0;
        this.mapContainerHeight = 0;
        this.render();
    },
    render: function () {
        this.$el.html(this.template());
        $('#map-section').append(this.$el);
        this.map = L.map(this.$('#feti-map')[0]).setView([-29, 20], 6);
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this.map);

        this.$('#feti-map').parent().css('height', '100%');
    },
    addLayer: function (layer) {
        this.map.addLayer(layer);
    },
    removeLayer: function (layer) {
        this.map.removeLayer(layer);
    },
    maximise: function() {
        alert('maximising');
    },
    clickMap: function (e) {
        this.fullScreenMap(e);
    },
    fullScreenMap: function (e) {
        var d = {};
        var _map = this.map;
        var that = this;

        if (!this.isFullScreen) {
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

            $('.search-category').css({
                'border-top-left-radius': '0',
                'border-top-right-radius': '0'
            });

            this.mapContainerWidth = this.$mapContainer.width();
            this.mapContainerHeight = 600;

            this.$mapContainer.animate(d, this.animationSpeed, function () {
                _map._onResize();
                that.isFullScreen = true;
                dispatcher.trigger('map:resize', true);
            });
        }
    },
    exitFullScreen: function (e) {
        var d = {};
        var _map = this.map;
        var that = this;

        if (this.isFullScreen) {
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

            $('.search-category').css({
                'border-top-left-radius': '8px',
                'border-top-right-radius': '8px'
            });

            this.$mapContainer.animate(d, this.animationSpeed, function () {
                _map._onResize();
                that.isFullScreen = false;
                dispatcher.trigger('map:resize', false);
            });
        }
    }
});

var mapView = new MapView();
mapView.render();
mapView.map.invalidateSize();


var SearchBarView = Backbone.View.extend({
    tagName: 'div',
    container: '#map-search',
    template: _.template('\
        <form action="map" method="POST">\
            <div class="search-category">\
                <span id="back-home">Home</span>\
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
               <i id="carousel-toogle" class="carousel-toogle fa fa-caret-left" aria-hidden="true"></i>\
            </div>\
        </form>'),
    events: {
        'click #where-to-study': 'categoryClicked',
        'click #what-to-study': 'categoryClicked',
        'click #choose-occupation': 'categoryClicked',
        'click #back-home': 'exitFullScreen',
        'click #carousel-toogle': 'carouselToogling'
    },
    categoryClicked: function (event) {
        this.changeCategory(event.target);
        mapView.fullScreenMap();
    },
    exitFullScreen: function () {
        this.toogleProviderWithMap();
    },
    carouselToogling: function (event) {
        if ($(event.target).hasClass('fa-caret-left')) {
            $(event.target).removeClass('fa-caret-left');
            $(event.target).addClass('fa-caret-right');
            if (!$('#providers').is(":visible")) {
                $('#providers').show("slide", {direction: "right"}, 500);
            }
        } else {
            $(event.target).removeClass('fa-caret-right');
            $(event.target).addClass('fa-caret-left');
            if ($('#providers').is(":visible")) {
                $('#providers').hide("slide", {direction: "right"}, 500);
            }
        }
    },
    initialize: function () {
        this.render();
        dispatcher.on('map:resize', this.mapResize, this);
        this.$search_bar = $(".search-bar");
        this.search_bar_hidden = true;
    },
    render: function () {
        this.$el.empty();
        this.$el.html(this.template());
        $(this.container).append(this.$el);
    },
    categorySelected: function () {
        var button = this.$el.find('.search-category').find('.m-button.active');
        if (button[0]) {
            return $(button[0]).html();
        } else {
            return null;
        }
    },
    changeCategory: function (button) {
        this.$el.find('.search-category').find('.m-button').removeClass('active');
        $(button).addClass('active');
        if (mapView.isFullScreen) {
            this.showSearchBar();
        }
    },
    mapResize: function (is_resizing) {
        if (is_resizing) {
            this.$('#back-home').show();
            this.showSearchBar();
        } else {
            this.$('#back-home').hide();

        }
    },
    showSearchBar: function () {
        if (this.search_bar_hidden && this.categorySelected()) {
            this.$search_bar.slideToggle(500);
            // zoom control animation
            var $zoom_control = $('.leaflet-control-zoom');
            $zoom_control.animate({
                marginTop: '+=55px'
            }, 500);
            var $result = $('#providers');
            $result.animate({
                paddingTop: '+=55px'
            }, 500);

            // now it is shown
            this.search_bar_hidden = false;
        }
    },
    hideSearchBarWithMap: function () {
        if (!this.search_bar_hidden) {
            this.$search_bar.slideToggle(500, function () {
                mapView.exitFullScreen();
            });
            // zoom control animation
            var $zoom_control = $('.leaflet-control-zoom');
            $zoom_control.animate({
                marginTop: '-=55px'
            }, 500);

            // now it is shown
            this.search_bar_hidden = true;
        } else {
            mapView.exitFullScreen();
        }
    },
    toogleProviderWithMap: function () {
        var that = this;
        if ($('#providers').is(":visible")) {
            $('#carousel-toogle').removeClass('fa-caret-right');
            $('#carousel-toogle').addClass('fa-caret-left');
            $('#providers').hide("slide", {direction: "right"}, 500, function () {
                that.hideSearchBarWithMap();
            });
        } else {
            that.hideSearchBarWithMap();
        }
    }
});

new SearchBarView();

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
        this.model.renderMarker();
    },
    initialize: function () {
        this.render();
    }
});