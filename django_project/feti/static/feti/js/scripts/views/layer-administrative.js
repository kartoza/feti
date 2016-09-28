define([
    'common'
], function (Common) {
    var LayerAdministrative = Backbone.View.extend({
        MAX_SIZE: 100,
        layer: ['country', 'province'],
        polygons: {},
        cache: {},
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
                    Common.Dispatcher.trigger('map:removeLayer', polygon);
                    this.polygons[layer] = null;
                }
            }
            this.setCurrentAdm();
        },
        setCurrentAdm: function () {
            // routing
            var adm = "";
            for (var i = 0; i <= this.layer.length - 1; i++) {
                var polygon = this.polygons[this.layer[i]];
                if (polygon) {
                    adm = polygon.getLayers()[0].feature.properties.title;
                }
            }
            this.current_adm = adm;
        },
        getAdministrativeByLatlng: function (latlng, layer) {
            var that = this;
            if(this.active) {
                if (layer == null) {
                    layer = this.layer[0];
                }
                $.ajax({
                    url: '/api/administrative',
                    data: {
                        lat: latlng.lat,
                        lng: latlng.lng,
                        layer: layer
                    },
                    success: function (data) {
                        var polygon = that._createPolygon(data);
                        that.resetBasedLayer(layer);
                        if (polygon) {
                            that.polygons[data.properties.layer] = polygon;
                        }
                        that.setCurrentAdm();
                        if (that.current_adm == "") {
                            that.map.searchBarView.searchRouting('');
                        } else {
                            that.map.searchBarView.searchRouting('administrative=' + that.current_adm);
                        }
                        that.showPolygon(that.current_adm);
                    },
                    error: function (request, error) {
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
            if (this.polygons[polygon.getLayers()[0].feature.properties.layer]) {
                Common.Dispatcher.trigger('map:removeLayer', this.polygons[polygon.getLayers()[0].feature.properties.layer]);
            }
            this.polygons[polygon.getLayers()[0].feature.properties.layer] = polygon;
            Common.Dispatcher.trigger('map:addLayer', polygon);
            this.map.searchBarView.$clear_draw.show();
        },
        showPolygon: function (adm_list) {
            this.resetBasedLayer();
            var adms = adm_list.split(',');
            var now_adm = [];
            var cache = this.cache;
            var that = this;
            _.each(adms, function (adm) {
                now_adm.push(adm);
                var string_adm = now_adm.join();
                var polygon = cache[string_adm];
                if (polygon) {
                    that.renderPolygon(polygon);
                } else {
                    that.getAdministrativeByString(string_adm);
                }
            });
            this.setCurrentAdm();
        },
        _createPolygon: function (data) {
            var that = this;
            if (data.geometry) {
                var mp = {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": data.geometry.coordinates
                    },
                    "properties": {
                        "name": "MultiPolygon",
                        "title": data.properties.title,
                        "layer": data.properties.layer,
                        "style": that.map.layerOptions(),
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
                that.cache[data.properties.title] = polygon;
                return polygon;
            }
            return null;
        }
    });

    return LayerAdministrative;
});
