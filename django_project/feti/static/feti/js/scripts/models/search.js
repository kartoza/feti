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
                if (this.attributes.locations.length > 0) {
                    // not sure is the best way
                    this.marker = new L.marker([this.attributes.locations[0].lat, this.attributes.locations[0].lng], {
                        icon: L.ExtraMarkers.icon({
                            markerColor: 'blue leaflet-clickable',
                            icon: 'true',
                            extraClasses: 'fa fa-graduation-cap',
                            iconColor: 'white'
                        })
                    }).bindPopup(this.attributes.locations[0].popup);
                    this.set('layer', L.layerGroup([this.marker]));
                    Common.Dispatcher.trigger('map:addLayer', this.get('layer'));
                }
            } else {
                this.set('layer', L.layerGroup([this.marker]));
                Common.Dispatcher.trigger('map:addLayer', this.get('layer'));
            }
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
            this.marker.openPopup();
            Common.Dispatcher.trigger('map:pan', this.attributes.location);
        },
    });

    return SearchResult;
});
