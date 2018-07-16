/*global define*/
define([
    'common',
    'backbone',
    'underscore',
    'leafletExtraMarkers'
], function (Common, Backbone, _) {
    var Occupation = Backbone.Model.extend({
        parse: function (options) {
            var data;
            if (_.isObject(options.results)) {
                data = options.results;
            } else {
                data = options;
            }
            return data;
        },
        show: function () {
            this.renderMarker();
        },
        hide: function () {
            this.removeMarker();
        },
        destroy: function () {
            // destroy by remove layers and delete this object
            this.removeMarker();
            delete this;
        },
        removeMarker: function () {
            if (this.get('layer')) {
                this.get('layer').clearLayers();
            }
        },
        renderMarker: function (data) {
            var layerGroup = L.featureGroup();
            if (!this.get('layer')) {
                for(var i=0; i<data.length; i++){
                    var object=data[i];
                    var location = object['location'];
                    var public_institution = true;
                    var markercolor;
                    if (public_institution) {
                        markercolor = 'blue leaflet-clickable';
                    } else {
                        markercolor = 'red leaflet-clickable';
                    }

                    var marker = new L.marker([location.coordinates[1], location.coordinates[0]], {
                        icon: L.ExtraMarkers.icon({
                            markerColor: markercolor,
                            icon: 'true',
                            extraClasses: 'fa fa-graduation-cap',
                            iconColor: 'white'
                        })
                    });

                    var popup = '';
                    var campus = 'Campus : ' + object['campus'];
                    var phone = object['phone'];

                    popup = '<div class="leaflet-header"><h3>' +
                        object['provider'] +
                        '</h3></div>' +
                        '<div class="leaflet-place"><strong> ' +
                        campus +
                        '</strong></div>' +
                        '<div class="leaflet-content">' +
                        '<div><i class="fa fa-map-marker"></i> ' + object['address'] + ' </div>' +
                        // '<div><i class="fa fa-link"></i> <a href="' + this.attributes.website + '" target="_blank">' + this.attributes.website + '</a> </div>' +
                        '<div><i class="fa fa-phone"></i> ' + phone + '</div>' +
                        '</div>';

                    var that = this;

                    // Events on marker and popup
                    marker.bindPopup(popup);
                    marker.off('click');
                    marker.on('click', function (e) {
                        e.originalEvent.preventDefault();
                        that.set('marker_clicked', true);
                    });
                    marker.on('mouseover', function (e) {
                        this.openPopup();
                    });
                    marker.on('mouseout', function (e) {
                        if (!that.get('marker_clicked')) {
                            this.closePopup();
                        }
                    });
                    marker.on('popupclose', function (e) {
                        that.set('marker_clicked', false);
                    });
                    this.set('marker', marker);
                    layerGroup.addLayer(marker);
                }
            }
            this.set('layer', layerGroup);
            Common.Dispatcher.trigger('map:addLayer', this.get('layer'));
        },
    });

    return Occupation;
});
