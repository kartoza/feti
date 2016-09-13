define([
    'common',
    '/static/feti/js/scripts/views/searchbar.js'
], function (Common, SearchbarView) {
    var MapView = Backbone.View.extend({
        template: _.template($('#map-template').html()),
        events: {
            'click #feti-map': 'clickMap'
        },
        layerOptions: function () {
            return {
                stroke: true,
                color: '#f06eaa',
                weight: 4,
                opacity: 0.5,
                fill: true,
                fillColor: null, //same as color by default
                fillOpacity: 0.2
            }
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

            this.animationSpeed = 400;

            this.mapContainerWidth = 0;
            this.mapContainerHeight = 0;

            // Leaflet draw
            this.drawnItems = new L.FeatureGroup();
            // Polygon draw handler
            this.polygonDrawer = null;
            this.polygonLayer = null;
            this.circleDrawer = null;
            this.circleLayer = null;

            this.render();
            this.searchBarView = new SearchbarView({parent: this});
            this.listenTo(this.searchBarView, 'backHome', this.backHome);
            this.listenTo(this.searchBarView, 'categoryClicked', this.fullScreenMap);

            // Common Dispatcher events
            Common.Dispatcher.on('map:pan', this.pan, this);
            Common.Dispatcher.on('map:addLayer', this.addLayer, this);
            Common.Dispatcher.on('map:removeLayer', this.removeLayer, this);
            Common.Dispatcher.on('map:exitFullScreen', this.exitFullScreen, this);
            Common.Dispatcher.on('map:toFullScreen', this.fullScreenMap, this);
        },
        backHome: function () {
            Common.Router.navigate('', true);
        },
        render: function () {
            this.$el.html(this.template());
            $('#map-section').append(this.$el);
            this.map = L.map(this.$('#feti-map')[0]).setView([-29, 20], 6);
            L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGltYXNjaXB1dCIsImEiOiJjaXNqczJmNW8wMmt4MnRvY25hNTlobnlyIn0.TAdOiFVlAdeKMi5TKzueoQ', {
                maxZoom: 20,
                attribution: "© <a href='https://www.mapbox.com/map-feedback/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
            }).addTo(this.map);
            this.$('#feti-map').parent().css('height', '100%');

            // Add drawable layer to map
            this.map.addLayer(this.drawnItems);

            this.polygonDrawer = new L.Draw.Polygon(this.map);

            this.circleDrawer = new L.Draw.Circle(this.map);

            // Initialise the draw control and pass it the FeatureGroup of editable layers
            var drawControl = new L.Control.Draw({
                draw: false,
                edit: {
                    featureGroup: this.drawnItems
                },
                remove: {
                    featureGroup: this.drawnItems
                }
            }, this);
            this.map.addControl(drawControl);

            // Draw events
            this.map.on('draw:created', this.drawCreated, this);
        },
        drawCreated: function (e) {
            var type = e.layerType,
                layer = e.layer;

            this.drawnItems.addLayer(layer);

            if (type === 'polygon') {
                this.polygonLayer = layer;
                this.searchBarView.onFinishedCreatedShape('polygon');
            } else if(type === 'circle') {
                this.circleLayer = layer;
                this.searchBarView.onFinishedCreatedShape('circle');
            }
        },
        enablePolygonDrawer: function () {
            this.clearAllDrawnLayer();
            if(this.polygonDrawer) {
                this.polygonDrawer.enable();
            }
        },
        disablePolygonDrawer: function () {
            this.polygonDrawer.disable();
        },
        enableCircleDrawer: function () {
            this.clearAllDrawnLayer();
            if(this.circleDrawer) {
                this.circleDrawer.enable();
            }
        },
        disableCircleDrawer: function () {
            this.circleDrawer.disable();
        },
        clearAllDrawnLayer: function () {
            this.drawnItems.eachLayer(function (layer) {
                this.drawnItems.removeLayer(layer);
            }, this);
        },
        getCoordinatesQuery: function() {
            var drawnLayers = this.drawnItems.getLayers();
            if (drawnLayers.length > 0) {
                var _layer = drawnLayers[0];
                var query = '';
                // check if layer is polygon or circle
                if(_layer instanceof L.Polygon) {
                    var coordinates = _layer.getLatLngs();
                    var coordinates_string = JSON.stringify(coordinates);
                    query = 'shape=polygon&coordinates='+coordinates_string;
                } else if(_layer instanceof L.Circle) {
                    var circleCoordinate = _layer.getLatLng();
                    var circleRadius = _layer.getRadius();
                    query = 'shape=circle&coordinate='+JSON.stringify(circleCoordinate)+'&radius='+circleRadius;
                }
                return query;
            }
        },
        addLayer: function (layer) {
            this.map.addLayer(layer);
        },
        removeLayer: function (layer) {
            this.map.removeLayer(layer);
        },
        maximise: function () {
            alert('maximising');
        },
        clickMap: function (e) {
            if (!this.isFullScreen) {
                Common.Router.navigate('map/' + Common.CurrentSearchMode, true);
            }
        },
        pan: function (latLng) {
            this.map.panTo(latLng);
        },
        changeCategory: function (mode) {
            this.searchBarView.changeCategoryButton(mode);
        },
        search: function (mode, query, filter) {
            this.searchBarView.search(mode, query, filter);
        },
        exitAllFullScreen: function () {
            this.searchBarView.toggleProvider();
        },
        fullScreenMap: function (speed) {
            var d = {};
            var _map = this.map;
            var that = this;
            var _speed = this.animationSpeed;
            $(".ui-menu").hide();

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
                    that.searchBarView.mapResize(true, _speed);
                    // set focus on search text
                    document.search_form.search_input.focus();
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

                this.$header.slideDown(this.animationSpeed);
                this.$aboutSection.slideDown(this.animationSpeed);
                this.$partnerSection.show();
                this.$footerSection.show();

                d.width = this.mapContainerWidth;
                d.height = this.mapContainerHeight;

                this.$mapContainer.css('padding-top', 0);

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
                    that.searchBarView.mapResize(false, that.animationSpeed);
                    that.searchBarView.toggleProvider(e);
                });

                // set body content to previous
                this.$bodyContent.css('height', 'auto');

                // edit url
                Backbone.history.navigate('/');
            }
        },
        createPolygon: function (coordinates) {
            this.clearAllDrawnLayer();
            this.polygonLayer = L.polygon(coordinates, this.layerOptions());
            this.drawnItems.addLayer(this.polygonLayer);
            this.addLayer(this.drawnItems);
            this.map.fitBounds(this.polygonLayer);
        },
        createCircle: function(coords, radius) {
            this.clearAllDrawnLayer();
            this.circleLayer = L.circle([coords['lat'], coords['lng']], radius, this.layerOptions());
            this.drawnItems.addLayer(this.circleLayer);
            this.addLayer(this.drawnItems);
            this.map.fitBounds(this.circleLayer);
        }
    });

    return MapView;
});