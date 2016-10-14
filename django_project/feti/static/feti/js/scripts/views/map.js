define([
    'common',
    '/static/feti/js/scripts/views/searchbar.js',
    '/static/feti/js/scripts/views/layer-administrative.js'
], function (Common, SearchbarView, LayerAdministrativeView) {
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
            this.$cover = $('#shadow-map');

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
            this._tooltip = null;

            this.render();
            this.searchBarView = new SearchbarView({parent: this});
            this.listenTo(this.searchBarView, 'backHome', this.backHome);
            this.listenTo(this.searchBarView, 'categoryClicked', this._onSearchBarCategoryClicked);

            this.layerAdministrativeView = new LayerAdministrativeView({parent: this});
            // Common Dispatcher events
            Common.Dispatcher.on('map:pan', this.pan, this);
            Common.Dispatcher.on('map:addLayer', this.addLayer, this);
            Common.Dispatcher.on('map:addLayerToMode', this.addLayerToModeLayer, this);
            Common.Dispatcher.on('map:removeLayer', this.removeLayer, this);
            Common.Dispatcher.on('map:exitFullScreen', this.exitFullScreen, this);
            Common.Dispatcher.on('map:toFullScreen', this.fullScreenMap, this);

            this.modesLayer = {
                'provider': L.layerGroup(),
                'course': L.layerGroup()
            }
        },
        backHome: function () {
            Common.Router.navigate('', true);
        },
        render: function () {
            this.$el.html(this.template());
            $('#map-section').append(this.$el);
            this.map = L.map(this.$('#feti-map')[0]).setView([-29, 20], 6);

            var that = this;
            // init click
            this.map.on('click', function (e) {
                if (that.isFullScreen) {
                    if (!that.isDrawing) {
                        Common.Dispatcher.trigger('map:click', e.latlng);
                    }
                }
            });
            this.map.on('dblclick', function (e) {
            });


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
            this.map.on('draw:drawstop', this.drawStop, this);
            this.map.on('draw:created', this.drawCreated, this);

            // Add marker for userlocation
            if (Common.UserLocation != 'None') {
                var regExp = /\(([^)]+)\)/;
                var location = regExp.exec(Common.UserLocation)[1].split(' ');
                var marker = new L.marker([location[1], location[0]], {
                    icon: L.ExtraMarkers.icon({
                        markerColor: 'orange leaflet-clickable',
                        icon: 'true',
                        extraClasses: 'fa fa-user',
                        iconColor: 'white'
                    })
                }).bindPopup("<b>My location</b>").addTo(this.map);
            }

        },
        onMouseMove: function (e) {
            var latlng = e.latlng;
            this._tooltip.updatePosition(latlng);
        },
        _onSearchBarCategoryClicked: function(event) {
            this.fullScreenMap();
            var mode = $(event.target).parent().data("mode");
            this._changeSearchLayer(Common.CurrentSearchMode, mode);
        },
        drawCreated: function (e) {
            var type = e.layerType,
                layer = e.layer;

            this.drawnItems.addLayer(layer);
            this.layerAdministrativeView.resetBasedLayer();

            if (type === 'polygon') {
                this.polygonLayer = layer;
                this.searchBarView.onFinishedCreatedShape('polygon');
            } else if (type === 'circle') {
                this.circleLayer = layer;
                this.searchBarView.onFinishedCreatedShape('circle');
            }
        },
        drawStop: function (e) {
            var type = e.layerType;
            this.searchBarView.cancelDraw(type);
        },
        enablePolygonDrawer: function () {
            this.isDrawing = true;
            this.clearAllDrawnLayer();
            if (this.polygonDrawer) {
                this.polygonDrawer.enable();
            }
        },
        disablePolygonDrawer: function () {
            this.isDrawing = false;
            this.polygonDrawer.disable();
        },
        enableCircleDrawer: function () {
            this.isDrawing = true;
            this.clearAllDrawnLayer();
            if (this.circleDrawer) {
                this.circleDrawer.enable();
            }
        },
        disableCircleDrawer: function () {
            this.isDrawing = false;
            this.circleDrawer.disable();
        },
        enableLocationFilter: function () {
            $('.leaflet-container').css('cursor','pointer');
            this.layerAdministrativeView.activate();

            // Add tooltip
            this._tooltip = new L.Tooltip(this.map);
            this._tooltip.updateContent({
				text: 'Click the map to show boundary'
			});
            this.map.on('mousemove', this.onMouseMove, this);
        },
        disableLocationFilter: function () {
            $('.leaflet-container').css('cursor','');
            this.layerAdministrativeView.deactivate();

            // Remove tooltip
			this._tooltip = null;
            this.map.off('mousemove', this.onMouseMove, this)
        },
        clearAllDrawnLayer: function () {
            this.drawnItems.eachLayer(function (layer) {
                this.drawnItems.removeLayer(layer);
            }, this);
            this.layerAdministrativeView.resetBasedLayer();
        },
        getCoordinatesQuery: function () {
            var drawnLayers = this.drawnItems.getLayers();
            if (drawnLayers.length > 0) {
                var _layer = drawnLayers[0];
                var query = '';
                // check if layer is polygon or circle
                if (_layer instanceof L.Polygon) {
                    var coordinates = _layer.getLatLngs();
                    var coordinates_string = JSON.stringify(coordinates);
                    query = 'shape=polygon&coordinates=' + coordinates_string;
                } else if (_layer instanceof L.Circle) {
                    var circleCoordinate = _layer.getLatLng();
                    var circleRadius = _layer.getRadius();
                    query = 'shape=circle&coordinate=' + JSON.stringify(circleCoordinate) + '&radius=' + circleRadius;
                }
                return query;
            } else {
                if (this.layerAdministrativeView.current_adm) {
                    return 'administrative=' + this.layerAdministrativeView.current_adm
                }
            }
        },
        addLayerToModeLayer: function (layer) {
            var mode = Common.CurrentSearchMode;
            var opposite = Common.CurrentSearchMode == 'provider' ? 'course' : 'provider';

            this.modesLayer[mode].addLayer(layer);
            if(this.map.hasLayer(this.modesLayer[opposite])) {
                this.map.removeLayer(this.modesLayer[opposite]);
            }
            if(!this.map.hasLayer(this.modesLayer[mode])) {
                this.map.addLayer(this.modesLayer[mode]);
            }
        },
        addLayer: function (layer) {
            this.map.addLayer(layer);
        },
        _changeSearchLayer: function (fromMode, toMode) {
            if(this.map.hasLayer(this.modesLayer[fromMode])) {
                this.map.removeLayer(this.modesLayer[fromMode]);
            }
            if(toMode=='occupation') {
                this.showMapCover();
                return;
            }
            this.hideMapCover();
            if(!this.map.hasLayer(this.modesLayer[toMode])) {
                this.map.addLayer(this.modesLayer[toMode]);
            }
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
            this._changeSearchLayer(Common.CurrentSearchMode, mode);
            this.searchBarView.changeCategoryButton(mode);
        },
        search: function (mode, query, filter) {
            this.searchBarView.search(mode, query, filter);
            if (filter && filter.indexOf('administrative') >= 0) {
                filter = filter.split('=')[1];
                this.layerAdministrativeView.showPolygon(filter);
            } else {
                this.layerAdministrativeView.resetBasedLayer();
            }
        },
        exitAllFullScreen: function () {
            this.searchBarView.exitOccupation();
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
                    that.searchBarView.exitOccupation(e);
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
            this.searchBarView.$clear_draw.show();
        },
        createCircle: function (coords, radius) {
            this.clearAllDrawnLayer();
            this.circleLayer = L.circle([coords['lat'], coords['lng']], radius, this.layerOptions());
            this.drawnItems.addLayer(this.circleLayer);
            this.addLayer(this.drawnItems);
            this.map.fitBounds(this.circleLayer);
            this.searchBarView.$clear_draw.show();

            var draggable = new L.Draggable(this.circleLayer);
            draggable.enable();
        },
        showMapCover: function () {
            if (!this.$cover.is(":visible")) {
                this.$cover.fadeIn(200);
            }
        },
        hideMapCover: function () {
            if (this.$cover.is(":visible")) {
                this.$cover.fadeOut(200);
            }
        },
        showResultContainer: function (mode) {
            $('#result-container-wrapper').find('.result-container').hide();
            $('#result-container-'+mode).show();
        }
    });

    return MapView;
});