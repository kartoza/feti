/*global define*/
define([
    'common'
], function (Common) {
    var Provider = Backbone.Model.extend({
        parse: function (options) {
            var data;
            if (_.isObject(options.results)) {
                data = options.results;
            } else {
                data = options;
            }
            return data;
        },
        renderMarker: function () {
            if (!this.get('layer')) {
                var location = this.attributes.location;
                var marker = new L.marker([location.lat, location.lng], {
                    icon: L.ExtraMarkers.icon({
                        markerColor: 'blue leaflet-clickable',
                        icon: 'true',
                        extraClasses: 'fa fa-graduation-cap',
                        iconColor: 'white'
                    })
                }).bindPopup(this.attributes._campus_popup);
                this.set('marker', marker);
            }
            this.set('layer', L.layerGroup([this.get('marker')]));
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
            var marker = this.get('marker');
            marker.openPopup();
            Common.Dispatcher.trigger('map:pan', marker._latlng);
        },
    });

    return Provider;
});
