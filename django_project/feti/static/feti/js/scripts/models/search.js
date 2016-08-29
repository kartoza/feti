/*global define*/
define([
    'common'
], function (Common) {

    var SearchResult = Backbone.Model.extend({
        parse: function (options) {
            var data;
            if (_.isObject(options.results)) {
                data = options.results;
            } else {
                data = options;
            }
            if (data.location) {
                var location = data.location.split("(")[1].replace(")", "").split(" ");
                data.location = new L.LatLng(parseFloat(location[1]), parseFloat(location[0]));
            }
            return data;
        },
        renderMarker: function () {
            if (!this.get('layer')) {
                var markers = [];
                var that = this;
                _.each(this.attributes.locations, function (location) {
                    // not sure is the best way
                    marker = new L.marker([location.lat, location.lng], {
                        icon: L.ExtraMarkers.icon({
                            markerColor: 'blue leaflet-clickable',
                            icon: 'true',
                            extraClasses: 'fa fa-graduation-cap',
                            iconColor: 'white'
                        })
                    }).bindPopup(location.popup);
                    markers.push(marker);
                });
                this.set('markers', markers);
            }
            this.set('now_index', 0);
            this.set('layer', L.layerGroup(this.get('markers')));
            Common.Dispatcher.trigger('map:addLayer', this.get('layer'));
        },
        removeMarker: function () {
            if (this.get('layer')) {
                this.get('layer').clearLayers();
            }
        },
        destroy: function () {
            // destroy by remove layers and delete this object
            this.removeMarker();
            delete this;
        },
        clicked: function () {
            var now_index = this.get('now_index');
            if (this.get('markers').length > 0) {
                this.get('markers')[now_index].openPopup();
                now_index += 1;
                if (now_index >= this.get('markers').length) {
                    now_index = 0;
                }
                this.set('now_index', now_index);
            }
            Common.Dispatcher.trigger('map:pan', this.attributes.location);
        },
    });

    return SearchResult;
});
