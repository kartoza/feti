define([
    'common'
], function (Common) {
    var LayerAdministrative = Backbone.View.extend({
        MAX_SIZE: 100,
        layer: ['province', 'district', 'municiple'],
        polygons: {},
        cache: {},
        currentAdminLayer: {},
        getCurrentAdminLayer: function() {
            var mode = Common.CurrentSearchMode;
            if (typeof this.currentAdminLayer[mode] == 'undefined') {
                return;
            }
            return this.currentAdminLayer[mode];
        },
        initialize: function (options) {
            this.map = options.parent;
            this.active = false;
            Common.Dispatcher.on('map:click', this.getAdministrativeByLatlng, this);
        },
        activate: function () {
            this.active = true;
        },
        deactivate: function () {
            this.active = false;
        },
        resetBasedLayer: function (layer) {
            var index_layer = this.layer.indexOf(layer);
            for (var i = index_layer; i <= this.layer.length - 1; i++) {
                layer = this.layer[i];
                var polygon = this.polygons[layer];
                if (polygon) {
                    Common.Dispatcher.trigger('map:removeLayerFromFilterLayers', polygon);
                    this.polygons[layer] = null;
                }
            }
            this.setCurrentAdm();
        },
        setCurrentAdm: function () {
            // routing
            var adm = "";
            var mode = Common.CurrentSearchMode;
            for (var i = 0; i <= this.layer.length - 1; i++) {
                var polygon = this.polygons[this.layer[i]];
                if (polygon) {
                    adm = polygon.getLayers()[0].feature.properties.title;
                }
            }
            this.currentAdminLayer[mode] = adm;
        },
        getAdministrativeByLatlng: function (latlng, layer) {
            var that = this;
            if (this.active) {
                if (layer == null) {
                    layer = this.layer[0];
                }
                $("path").css("cursor", "progress");
                $.ajax({
                    url: '/api/administrative',
                    data: {
                        lat: latlng.lat,
                        lng: latlng.lng,
                        layer: layer
                    },
                    success: function (data) {
                        $("path").css("cursor", "pointer");
                        var polygon = that._createPolygon(data);
                        that.resetBasedLayer(layer);
                        if (polygon) {
                            that.polygons[data.layer] = polygon;
                        }
                        that.setCurrentAdm();
                        if (that.getCurrentAdminLayer() == "") {
                            Common.Dispatcher.trigger('search:updateRouter', '');
                        } else {
                            Common.Dispatcher.trigger('search:updateRouter', 'administrative=' + that.getCurrentAdminLayer());
                        }
                        that.showPolygon(that.getCurrentAdminLayer());
                    },
                    error: function (request, error) {
                        $("path").css("cursor", "pointer");
                    }
                });
            }
        },
        getAdministrativeByString: function (string) {
            var that = this;
            $.ajax({
                url: '/api/administrative',
                data: {
                    administrative: string
                },
                success: function (data) {
                    var polygon = that._createPolygon(data);
                    if (polygon) {
                        that.renderPolygon(polygon);
                    }
                },
                error: function (request, error) {
                }
            });
        },
        renderPolygon: function (polygon) {
            if (!Common.EmbedVersion) {
                if (this.polygons[polygon.getLayers()[0].feature.properties.layer]) {
                    Common.Dispatcher.trigger('map:removeLayerFromFilterLayers', this.polygons[polygon.getLayers()[0].feature.properties.layer]);
                }
                if(polygon) {
                    this.polygons[polygon.getLayers()[0].feature.properties.layer] = polygon;
                    Common.Dispatcher.trigger('map:addLayerToFilterLayers', polygon);
                    this.map.clearButton.enable();
                }
            }
        },
        showPolygon: function (adm_list) {
            this.resetBasedLayer();
            var adms = adm_list.split(',');
            var now_adm = [];
            var cache = this.cache;
            var that = this;
            var last_polygon = null;
            _.each(adms, function (adm) {
                now_adm.push(adm);
                var string_adm = now_adm.join();
                var polygon = cache[string_adm];
                if (polygon) {
                    last_polygon = polygon;
                    that.renderPolygon(polygon);
                } else {
                    that.getAdministrativeByString(string_adm);
                }
            });

            if(last_polygon) {
                this.map.map.fitBounds(last_polygon.getBounds());
            }

            this.setCurrentAdm();
        },
        _createPolygon: function (data) {
            var that = this;
            var province = {
                stroke: true,
                color: '#f06eaa',
                weight: 4,
                opacity: 0.5,
                fill: true,
                fillColor: null,
                fillOpacity: 0.1
            };

            var district = {
                stroke: true,
                color: '#1D69B3',
                weight: 4,
                opacity: 0.5,
                fill: true,
                fillColor: null,
                fillOpacity: 0.2
            };

            var style = null;

            if(data.layer === 'province') {
                style = province;
            } else if(data.layer === 'district') {
                style = district;
            }

            if (data.polygon_geometry) {
                var mp = {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": data.polygon_geometry.coordinates
                    },
                    "properties": {
                        "name": "MultiPolygon",
                        "title": data.title,
                        "layer": data.layer,
                        "style": style,
                        "parent": ""
                    }
                };
                var polygon = new L.GeoJSON(mp, {
                    style: function (feature) {
                        return feature.properties.style
                    },
                    onEachFeature: function (feature, layer) {
                        layer.on({
                            click: function (e) {
                                var index_layer = that.layer.indexOf(feature.properties.layer);
                                if (index_layer < that.layer.length - 1) {
                                    that.getAdministrativeByLatlng(e.latlng, that.layer[index_layer + 1])
                                }
                            }
                        });
                    }
                });
                that.cache[data.title] = polygon;
                return polygon;
            }
            return null;
        }
    });

    return LayerAdministrative;
});
