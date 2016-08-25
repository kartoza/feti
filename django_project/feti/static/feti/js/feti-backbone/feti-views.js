var app_router = app_router || {};

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
        dispatcher.on('map:pan', this.pan, this);
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
    pan: function (latLng) {
        this.map.panTo(latLng);
    },
    addLayer: function (layer) {
        this.map.addLayer(layer);
    },
    removeLayer: function (layer) {
        this.map.removeLayer(layer);
    },
    clickMap: function (e) {
        if (!this.isFullScreen) {
            app_router.navigate('map', true);
        }
    },
    fullScreenMap: function (speed) {
        var d = {};
        var _map = this.map;
        var that = this;
        var _speed = this.animationSpeed;

        if (!this.isFullScreen) {

            if (typeof speed != 'undefined') {
                _speed = speed;
            }

            this.$header.slideUp(_speed);
            this.$aboutSection.slideUp(_speed);
            this.$partnerSection.hide();
            this.$footerSection.hide();

            var nav_bar_height = $('#navigation_bar').height();
            this.$mapContainer.css('padding-top', nav_bar_height);
            this.$mapContainer.css('padding-right', 0);
            this.$mapContainer.css('padding-left', 0);

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

            this.$mapContainer.animate(d, _speed, function () {
                _map._onResize();
                that.isFullScreen = true;
                dispatcher.trigger('map:resize', true, speed);
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

            // edit url
            Backbone.history.navigate('/');
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
        <form id="search-form" action="" method="POST">\
            <div class="search-category">\
                <span id="back-home">Home</span>\
                <span class="map-question"">\
                    What are you looking for?\
                </span>\
                <span class="m-button map-option" id="where-to-study" mode="provider">\
                    Where to study\
                </span>\
                <span class="m-button map-option" id="what-to-study" mode="course">\
                    What to study\
                </span>\
                <span class="m-button map-option" id="choose-occupation" mode="occupation">\
                    Choose occupation\
                </span>\
            </div>\
            <div class="search-bar">\
                <span id="search-bar" class="right-inner-addon">\
                   <i class="icon-search fa fa-search"></i>\
                   <input id="search-bar-input" type="search"\
                           class="form-control" name="q"\
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
               <i id="result-toogle" class="result-toogle fa fa-caret-left" aria-hidden="true"></i>\
            </div>\
        </form>'),
    events: {
        'click #where-to-study': 'categoryClicked',
        'click #what-to-study': 'categoryClicked',
        'click #choose-occupation': 'categoryClicked',
        'click #back-home': 'exitFullScreen',
        'click #result-toogle': 'resultToogling'
    },
    initialize: function () {
        this.render();
        this.$search_bar = $(".search-bar");
        this.$search_bar_input = $("#search-bar-input");
        this.$provider_button = $("#where-to-study");
        this.$course_button = $("#what-to-study");
        this.$occupation_button = $("#choose-occupation");
        this.search_bar_hidden = true;
        dispatcher.on('map:resize', this.mapResize, this);
    },
    render: function () {
        this.$el.empty();
        this.$el.html(this.template());
        $(this.container).append(this.$el);
        // form submit
        var that = this;
        $("#search-form").submit(function (e) {
            var mode = that.categorySelected();
            if (mode == 'provider') {
                search_collection.getProvider(that.$search_bar_input.val());
            }

            e.preventDefault(); // avoid to execute the actual submit of the form.
        });
    },
    categoryClicked: function (event) {
        this.changeCategory(event.target);
        mapView.fullScreenMap();
    },
    exitFullScreen: function (e) {
        this.toogleProviderWithMap(e);
        this.changeCategoryButton("");
    },
    categorySelected: function () {
        var button = this.$el.find('.search-category').find('.m-button.active');
        if (button[0]) {
            return $(button[0]).attr("mode");
        } else {
            return "";
        }
    },
    showResult: function () {
        var $toogle = $('#result-toogle');
        if ($toogle.hasClass('fa-caret-left')) {
            $toogle.removeClass('fa-caret-left');
            $toogle.addClass('fa-caret-right');
            if (!$('#providers').is(":visible")) {
                $('#providers').show("slide", {direction: "right"}, 500);
            }
        }
    },
    resultToogling: function (event) {
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
    changeCategoryButton: function (mode) {
        this.$el.find('.search-category').find('.m-button').removeClass('active');
        var $button = null;
        var highlight = "Choose what are you looking for";
        if (mode == "provider") {
            $button = this.$provider_button;
            highlight = 'Search for provider';
        } else if (mode == "course") {
            $button = this.$course_button;
            highlight = 'Search for courses';
        } else if (mode == "occupation") {
            $button = this.$occupation_button;
            highlight = 'Search for occuption';
        }

        // change placeholder of input
        this.$search_bar_input.attr("placeholder", highlight);
        if ($button) {
            $button.addClass('active');
            if (mapView.isFullScreen) {
                this.showSearchBar();
            }
        }
    },
    changeCategory: function (button) {
        var mode = $(button).attr("mode");
        Backbone.history.navigate('map/' + mode, true);
    },
    mapResize: function (is_resizing, speed) {
        if (is_resizing) {
            this.$('#back-home').show();
            this.showSearchBar(speed);
        } else {
            this.$('#back-home').hide();

        }
    },
    showSearchBar: function (speed) {
        if (this.search_bar_hidden) {
            this.$search_bar.slideToggle(speed);
            // zoom control animation
            var $zoom_control = $('.leaflet-control-zoom');
            $zoom_control.animate({
                marginTop: '+=55px'
            }, speed);
            var $result = $('#providers');
            $result.animate({
                paddingTop: '+=55px'
            }, speed);

            // now it is shown
            this.search_bar_hidden = false;
        }
    },
    hideSearchBarWithMap: function (e) {
        if (!this.search_bar_hidden) {
            this.$search_bar.slideToggle(500, function () {
                mapView.exitFullScreen(e);
            });
            // zoom control animation
            var $zoom_control = $('.leaflet-control-zoom');
            $zoom_control.animate({
                marginTop: '-=55px'
            }, 500);

            // now it is shown
            this.search_bar_hidden = true;
        } else {
            mapView.exitFullScreen(e);
        }
    },
    toogleProviderWithMap: function (e) {
        var that = this;
        if ($('#providers').is(":visible")) {
            $('#result-toogle').removeClass('fa-caret-right');
            $('#result-toogle').addClass('fa-caret-left');
            $('#providers').hide("slide", {direction: "right"}, 500, function () {
                that.hideSearchBarWithMap(e);
            });
        } else {
            that.hideSearchBarWithMap(e);
        }
    }
});

var SearchResultView = Backbone.View.extend({
    tagName: 'div',
    className: 'result-row',
    template: _.template('<%- provider %>'),
    container: '#providers',
    model: SearchResult,
    events: {
        'click': 'clicked'
    },
    clicked: function () {
        this.model.clicked();
        return false;
    },
    render: function () {
        this.$el.empty();
        this.$el.html(this.template(this.model.attributes));
        $(this.container).append(this.$el);
        this.model.renderMarker();
    },
    initialize: function () {
        this.render();
    },
    destroy: function () {
        this.model.destroy();
        this.$el.remove();
        return Backbone.View.prototype.remove.call(this);
    }
});

var LoginModalView = Backbone.View.extend({
    id: 'login-modal',
    className: 'modal fade',
    template: _.template($('#login-modal-template').html()),
    events: {
        'hidden.bs.modal': 'teardown'
    },

    initialize: function () {
        _.bindAll(this, 'show', 'teardown', 'render', 'hide');
        this.render();
    },

    show: function () {
        this.$el.modal('show');
    },

    hide: function (s) {
        this.$el.modal('hide');
    },

    teardown: function () {
        app_router.back('login');
    },

    render: function () {
        this.$el.html(this.template());
        this.$el.modal({show: false});
        return this;
    }
});

searchBarView = new SearchBarView();
loginModalView = new LoginModalView();
