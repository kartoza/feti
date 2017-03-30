define([
    'common',
    'scripts/views/search',
    'scripts/views/sidebar',
    'scripts/views/layer-administrative',
    'scripts/share'
], function (Common, SearchView, SidebarView, LayerAdministrativeView, Share) {
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
            if (Common.EmbedVersion) {
                this.animationSpeed = 0;
            }

            this.mapContainerWidth = 0;
            this.mapContainerHeight = 0;

            // Leaflet draw
            this.drawnItems = new L.FeatureGroup();
            this.listDrawnItems = {};

            // Polygon draw handler
            this.polygonDrawer = null;
            this.polygonLayer = null;
            this.circleDrawer = null;
            this.circleLayer = null;
            this._tooltip = null;

            this.render();
            this.searchView = new SearchView({parent: this});
            this.sideBarView = new SidebarView({parent: this});

            this.listenTo(this.searchView, 'backHome', this.backHome);

            this.layerAdministrativeView = new LayerAdministrativeView({parent: this});
            // Common Dispatcher events
            Common.Dispatcher.on('map:pan', this.pan, this);
            Common.Dispatcher.on('map:addLayer', this.addLayer, this);
            Common.Dispatcher.on('map:addLayerToMode', this.addLayerToModeLayer, this);
            Common.Dispatcher.on('map:removeLayer', this.removeLayer, this);
            Common.Dispatcher.on('map:exitFullScreen', this.exitFullScreen, this);
            Common.Dispatcher.on('map:toFullScreen', this.fullScreenMap, this);
            Common.Dispatcher.on('map:showShareBar', this.showShareBar, this);
            Common.Dispatcher.on('map:hideShareBar', this.hideShareBar, this);
            Common.Dispatcher.on('map:repositionMap', this.repositionMap, this);

            Common.Dispatcher.on('map:addLayerToFilterLayers', this.addLayerToFilterLayers, this);
            Common.Dispatcher.on('map:removeLayerFromFilterLayers', this.removeLayerFromFilterLayers, this);

            this.modesLayer = {
                'provider': L.featureGroup(),
                'course': L.featureGroup(),
                'favorites': L.featureGroup()
            }
        },
        updateMapSize: function () {
            this.map._onResize();
        },
        backHome: function () {
            Common.Router.navigate('', true);
        },
        zoomToDefault: function () {
            // zoom map to default
            this.map.setView([-32.35, 20], 7);
        },
        render: function () {
            this.$el.html(this.template());
            $('#map-section').append(this.$el);
            this.map = L.map(this.$('#feti-map')[0]).setView([-32.35, 20], 7);

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
            // this.map.addLayer(this.drawnItems);

            this.polygonDrawer = new L.Draw.Polygon(this.map);

            this.circleDrawer = new L.Draw.Circle(this.map, {metric: true, feet: false});

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
            this.map.on(L.Draw.Event.CREATED, this.drawCreated, this);
            this.map.on(L.Draw.Event.DRAWSTOP, this.drawStop, this);

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

            // Add control button
            var _this = this;

            var deactivateState = function (previousState) {
                return {
                    stateName: 'deactivate',
                    icon: 'fa-times',
                    title: 'cancel',
                    onClick: function (btn, map) {
                        btn.state(previousState);

                        _this._enableOtherControlButtons('clear');
                        switch (previousState) {
                            case 'locationButton':
                                _this.disableLocationFilter();
                                break;
                            case 'polygonButton':
                                _this.disablePolygonDrawer();
                                break;
                            case 'circleButton':
                                _this.disableCircleDrawer();
                                break;
                            default:
                                break;
                        }
                    }
                }
            };

            this.locationButton = L.easyButton({
                states: [
                    {
                        stateName: 'locationButton',
                        icon: 'fa-globe',
                        title: 'Filter map by location',
                        onClick: function (btn, map) {
                            btn.state('deactivate');
                            _this.searchView.clearAllDraw();
                            _this.enableLocationFilter();
                            _this._disableOtherControlButtons(btn);
                        }
                    },
                    deactivateState('locationButton')
                ]
            });

            this.polygonButton = L.easyButton({
                states: [
                    {
                        stateName: 'polygonButton',
                        icon: 'fa-square-o',
                        title: 'Filter map by polygon',
                        onClick: function (btn, map) {
                            btn.state('deactivate');
                            _this.searchView.clearAllDraw();
                            _this.enablePolygonDrawer();
                            _this._disableOtherControlButtons(btn);
                            btn._map.on('finishedDrawing', function (e) {
                                if (e.layerType == 'polygon') {
                                    btn.state('polygonButton');
                                }
                            });
                        }
                    },
                    deactivateState('polygonButton')
                ]
            });

            this.circleButton = L.easyButton({
                states: [
                    {
                        stateName: 'circleButton',
                        icon: 'fa-circle-o',
                        title: 'Filter map by circle',
                        onClick: function (btn, map) {
                            btn.state('deactivate');
                            _this.searchView.clearAllDraw();
                            _this.enableCircleDrawer();
                            _this._disableOtherControlButtons(btn);
                            btn._map.on('finishedDrawing', function (e) {
                                if (e.layerType == 'circle') {
                                    btn.state('circleButton');
                                }
                            });
                        }
                    },
                    deactivateState('circleButton')
                ]
            });

            this.clearButton = L.easyButton({
                states: [
                    {
                        stateName: 'clearButton',
                        icon: 'fa-trash-o',
                        title: 'Clear filter',
                        onClick: function (btn, map) {
                            btn.disable();
                            _this.clearAllDrawnLayer();
                            Common.Dispatcher.trigger('search:updateRouter');
                        }
                    }
                ]
            });

            this.clearButton.disable();

            this.locationFilterBar = L.easyBar([
                this.locationButton,
                this.polygonButton,
                this.circleButton,
                this.clearButton
            ]);

            this.locationFilterBar.options.position = 'topleft';
            this.locationFilterBar.options.id = 'filter-bar-container';

            if (!Common.EmbedVersion) {
                this.locationFilterBar.addTo(this.map);
            }

            // Share bar

            this.sharePDF = L.easyButton({
                id: 'share-pdf-button',
                position: 'topright',
                states: [
                    {
                        stateName: 'sharePDF',
                        icon: 'fa-file-pdf-o',
                        title: 'Download PDF Summary',
                        onClick: function (btn, map) {
                            Share.sharePDF();
                        }
                    }
                ]
            });

            this.shareEmail = L.easyButton({
                id: 'share-email-button',
                position: 'topright',
                states: [
                    {
                        stateName: 'shareEmail',
                        icon: 'fa-envelope-o',
                        title: 'Send Summary Via Email',
                        onClick: function (btn, map) {
                            Share.shareEmail();
                        }
                    }
                ]
            });

            this.shareTwitter = L.easyButton({
                id: 'share-twitter-button',
                position: 'topright',
                states: [
                    {
                        stateName: 'shareTwitter',
                        icon: 'fa-twitter',
                        title: 'Share To Twitter',
                        onClick: function (btn, map) {
                            Share.shareToTwitter();
                        }
                    }
                ]
            });

            this.shareURL = L.easyButton({
                id: 'share-url-button',
                states: [
                    {
                        stateName: 'shareURL',
                        icon: 'fa-link',
                        title: 'Share Link',
                        onClick: function (btn, map) {
                            Share.shareURL();
                        }
                    }
                ]
            });

            this.shareEmbedCode = L.easyButton({
                id: 'share-embed-code',
                states: [
                    {
                        stateName: 'shareEmbedCode',
                        icon: 'fa-code',
                        title: 'Embed Code',
                        onClick: function (btn, map) {
                            Share.getEmbedCode();
                        }
                    }
                ]
            });

            this.shareBar = L.easyBar([
                this.sharePDF,
                this.shareEmail,
                this.shareTwitter,
                this.shareURL,
                this.shareEmbedCode
            ]);

            this.shareBar.options.position = 'topright';
            this.shareBar.options.id = 'share-bar-container';

            if (!Common.EmbedVersion) {
                this.shareBar.addTo(this.map);
            }

            this.hideShareBar();
        },
        hideShareBar: function () {
            $('#share-pdf-button').hide();
            $('#share-email-button').hide();
            $('#share-twitter-button').hide();
            $('#share-url-button').hide();
        },
        showShareBar: function () {
            var mode = Common.CurrentSearchMode;

            // No need to share link and twitter in favorites
            if (mode != 'favorites') {
                $('#share-twitter-button').show();
                $('#share-url-button').show();
            } else {
                $('#share-twitter-button').hide();
                $('#share-url-button').hide();
            }
            $('#share-pdf-button').show();
            $('#share-email-button').show();
        },
        _disableOtherControlButtons: function (currentControl) {
            for (var i = 0; i < this.locationFilterBar._buttons.length; i++) {
                if (this.locationFilterBar._buttons[i] != currentControl) {
                    this.locationFilterBar._buttons[i].disable();
                }
            }
        },
        _enableOtherControlButtons: function (excluded) {
            for (var i = 0; i < this.locationFilterBar._buttons.length; i++) {
                var button_title = this.locationFilterBar._buttons[i]._states[0].title;

                if (this.locationFilterBar._buttons[i] != this.clearButton) {
                    this.locationFilterBar._buttons[i].enable();
                }

                if (typeof excluded != 'undefined' && excluded == button_title) {
                    this.locationFilterBar._buttons[i].disable();
                }
            }
        },
        onMouseMove: function (e) {
            var latlng = e.latlng;
            this._tooltip.updatePosition(latlng);
        },
        drawCreated: function (e) {
            var type = e.layerType,
                layer = e.layer;

            this.clearButton.enable();

            var currentMode = Common.CurrentSearchMode;

            this.listDrawnItems[currentMode] = L.featureGroup();
            this.listDrawnItems[currentMode].addLayer(layer);
            this.map.addLayer(this.listDrawnItems[currentMode]);

            if (type === 'polygon') {
                this.polygonLayer = layer;
                this.map.fire('finishedDrawing', {'layerType': 'polygon'});
            } else if (type === 'circle') {
                this.circleLayer = layer;
                this.map.fire('finishedDrawing', {'layerType': 'circle'});
            }
            this._enableOtherControlButtons();
            this.map.fitBounds(layer.getBounds(), {paddingTopLeft: [75, 75]});
        },
        drawStop: function (e) {
            Common.Dispatcher.trigger('search:updateRouter');
            this.isDrawing = false;
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
            $('.leaflet-container').css('cursor', 'pointer');
            this.layerAdministrativeView.activate();

            // Add tooltip
            this._tooltip = new L.Draw.Tooltip(this.map);
            this._tooltip.updateContent({
                text: 'Click the map to show boundary'
            });
            this.map.on('mousemove', this.onMouseMove, this);
        },
        disableLocationFilter: function () {
            $('.leaflet-container').css('cursor', '');
            this.layerAdministrativeView.deactivate();

            // Remove tooltip
            $('.leaflet-draw-tooltip').hide();
            this._tooltip = null;
            this.map.off('mousemove', this.onMouseMove, this)
        },
        clearAllDrawnLayer: function () {
            var mode = Common.CurrentSearchMode;
            this.layerAdministrativeView.resetBasedLayer();
            if(typeof this.listDrawnItems[mode] == 'undefined') {
                return;
            }

            this.map.removeLayer(this.listDrawnItems[mode]);

            this.listDrawnItems[mode].eachLayer(function (layer) {
                this.listDrawnItems[mode].removeLayer(layer);
            }, this);
        },
        getCoordinatesQuery: function (mode) {
            if(this.layerAdministrativeView.getCurrentAdminLayer()) {
                this.clearButton.enable();
                return 'administrative=' + this.layerAdministrativeView.getCurrentAdminLayer()
            }

            if (typeof this.listDrawnItems[mode] !== 'undefined') {
                this.clearButton.enable();
                var drawnLayers = this.listDrawnItems[mode].getLayers();
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
                }
            }
            this.clearButton.disable();
        },
        clearLayerMode: function (mode) {
            if (this.map.hasLayer(this.modesLayer[mode])) {
                var layers = this.modesLayer[mode].getLayers();
                for (var i = 0; i < layers.length; i++) {
                    this.modesLayer[mode].removeLayer(layers[i]);
                }
                this.map.removeLayer(this.modesLayer[mode]);
            }
        },
        addLayerToModeLayer: function (layer) {
            var mode = Common.CurrentSearchMode;

            if (typeof mode == 'undefined') {
                return
            }

            var opposite = Common.CurrentSearchMode == 'provider' ? 'course' : 'provider';

            this.modesLayer[mode].addLayer(layer);

            if (this.map.hasLayer(this.modesLayer[opposite])) {
                this.map.removeLayer(this.modesLayer[opposite]);
            }
            if (!this.map.hasLayer(this.modesLayer[mode])) {
                this.map.addLayer(this.modesLayer[mode]);
            }
        },
        addLayerToFilterLayers: function(layer) {
            var mode = Common.CurrentSearchMode;
            if (typeof this.listDrawnItems[mode] == 'undefined') {
                this.listDrawnItems[mode] = L.featureGroup();
            }
            this.listDrawnItems[mode].addLayer(layer);
            this.map.addLayer(this.listDrawnItems[mode]);
        },
        removeLayerFromFilterLayers: function(layer) {
            var mode = Common.CurrentSearchMode;
            if (typeof this.listDrawnItems[mode] == 'undefined') {
                return
            }
            this.listDrawnItems[mode].removeLayer(layer);
        },
        repositionMap: function (mode) {
            // Reposition map after category changed
            if(this.listDrawnItems[mode]) {
                if (typeof this.listDrawnItems[mode].getBounds()._northEast != 'undefined') {
                    this.map.fitBounds(this.listDrawnItems[mode].getBounds(), {paddingTopLeft: [75, 75]});
                    return;
                }
            }

            if (!this.modesLayer[mode]) {
                return;
            }
            if (typeof this.modesLayer[mode].getBounds()._northEast != 'undefined')
                this.map.fitBounds(this.modesLayer[mode].getBounds(), {paddingTopLeft: [75, 75]});
        },
        addLayer: function (layer) {
            this.map.addLayer(layer);
        },
        changeSearchLayer: function (fromMode, toMode) {
            // Triggered when search category changed
            if (this.map.hasLayer(this.modesLayer[fromMode])) {
                this.map.removeLayer(this.modesLayer[fromMode]);
            }
            if (this.map.hasLayer(this.listDrawnItems[fromMode])) {
                this.map.removeLayer(this.listDrawnItems[fromMode]);
            }
            if (!this.map.hasLayer(this.listDrawnItems[toMode])) {
                if(typeof this.listDrawnItems[toMode] != 'undefined') {
                    this.repositionMap(toMode);
                    this.map.addLayer(this.listDrawnItems[toMode]);
                }
            }

            if (toMode == 'occupation') {
                this.hideShareBar();
                return;
            }
            if (!this.map.hasLayer(this.modesLayer[toMode])) {
                this.map.addLayer(this.modesLayer[toMode]);
                if (this.modesLayer[toMode].getLayers().length > 0) {
                    this.repositionMap(toMode);
                    this.showShareBar();
                } else {
                    this.hideShareBar();
                }
            }
        },
        removeLayer: function (layer) {
            this.map.removeLayer(layer);
        },
        maximise: function () {
            alert('maximising');
        },
        clickMap: function (e) {
            var last_route = Common.Router.get_latest_route();
            if (!this.isFullScreen) {
                if (last_route) {
                    Common.Router.navigate(Common.Router.get_latest_route(), true);
                } else {
                    Common.Router.navigate('map/' + Common.CurrentSearchMode, true);
                }
            }
        },
        pan: function (latLng) {
            this.map.panTo(latLng);
        },
        changeCategory: function (mode) {
            this.changeSearchLayer(Common.CurrentSearchMode, mode);
            this.searchView.changeCategoryButton(mode);
        },
        search: function (mode, query, filter) {
            this.searchView.search(mode, query, filter);
            if (mode == 'favorites') {
                filter = query;
            }
            if (filter && filter.indexOf('administrative') >= 0) {
                filter = filter.split('=')[1];
                this.layerAdministrativeView.showPolygon(filter);
            } else {
                this.layerAdministrativeView.resetBasedLayer();
            }
        },
        exitAllFullScreen: function () {
            this.searchView.exitOccupation();
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
                    that.searchView.mapResize(true, _speed);
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
                    that.searchView.mapResize(false, that.animationSpeed);
                    that.searchView.exitOccupation(e);
                    $('#feti-map').css('width', '100%');
                });

                // set body content to previous
                this.$bodyContent.css('height', 'auto');

                // edit url
                Backbone.history.navigate('/');
            }
        },
        openResultContainer: function (div) {
            var that = this;
            if (!this.sideBarView.is_open()) {
                if (!Common.EmbedVersion) {
                    div.removeClass('fa-caret-left');
                    div.addClass('fa-caret-right');
                }
                this.sideBarView.open();
                // change map width
                var $mapContainer = $('#feti-map');
                var d = {};
                d.width = $('#shadow-map').width() - $('#result-wrapper').width();
                d.height = '100%';
                if (!Common.EmbedVersion) {
                    $mapContainer.animate(d, 500, function () {
                        $mapContainer.css('padding-right', '500px');
                        that.updateMapSize();
                    });
                }
                // close filter if open
                this.searchView.hideFilterPanel();
            }
            this.sideBarView.showMapCover();
            this.sideBarView.updateOccupationDetail();
        },
        closeResultContainer: function (div) {
            var $mapContainer = $('#feti-map');

            if (this.sideBarView.is_open()) {
                if (!Common.EmbedVersion) {
                    div.removeClass('fa-caret-right');
                    div.addClass('fa-caret-left');
                }
                this.sideBarView.close();
                var d = {};
                d.width = '100%';
                d.height = '100%';
                var that = this;

                $mapContainer.animate(d, 500, function () {
                    $mapContainer.css('padding-right', '0');
                    that.updateMapSize();
                });
            }
        },
        createPolygon: function (coordinates) {
            var mode = Common.CurrentSearchMode;

            if (typeof this.listDrawnItems[mode] == 'undefined') {
                this.listDrawnItems[mode] = L.featureGroup()
            }

            this.clearAllDrawnLayer();
            this.polygonLayer = L.polygon(coordinates, this.layerOptions());

            this.listDrawnItems[mode].addLayer(this.polygonLayer);
            this.addLayer(this.listDrawnItems[mode]);

            this.map.fitBounds(this.polygonLayer);
            this.clearButton.enable();
        },
        createCircle: function (coords, radius) {
            var mode = Common.CurrentSearchMode;

            if (typeof this.listDrawnItems[mode] == 'undefined') {
                this.listDrawnItems[mode] = L.featureGroup()
            }

            this.clearAllDrawnLayer();
            this.circleLayer = L.circle([coords['lat'], coords['lng']], radius, this.layerOptions());

            this.listDrawnItems[mode].addLayer(this.circleLayer);
            this.addLayer(this.listDrawnItems[mode]);

            this.map.fitBounds(this.circleLayer);
            this.clearButton.enable();

            var draggable = new L.Draggable(this.circleLayer);
            draggable.enable();
        },
        showResultContainer: function (mode) {
            $('#result-container-wrapper').find('.result-container').hide();
            $('#result-container-' + mode).show();
            this.sideBarView.hideMapCover();
        }
    });

    return MapView;
});