define([
    'common',
    '/static/feti/js/scripts/views/searchbar.js'
], function(Common, SearchbarView){
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
            Common.Dispatcher.on('map:addLayer', this.addLayer, this);
            Common.Dispatcher.on('map:removeLayer', this.removeLayer, this);
            this.animationSpeed = 400;

            this.mapContainerWidth = 0;
            this.mapContainerHeight = 0;

            this.render();
            new SearchbarView();
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
            Common.Router.navigate('map/fullscreen', true);
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

                this.$navbar.hide();
                this.$header.slideUp(_speed);
                this.$aboutSection.slideUp(_speed);
                this.$partnerSection.hide();
                this.$footerSection.hide();

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
                    Common.Dispatcher.trigger('map:resize', true);
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
                    Common.Dispatcher.trigger('map:resize', false);
                });

                // edit url
                Backbone.history.navigate('/');
            }
        }
    });

    return MapView;
});