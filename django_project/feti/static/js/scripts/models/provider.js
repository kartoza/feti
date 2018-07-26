/*global define*/
define([
    'common',
    'backbone',
    'jquery',
    'leafletExtraMarkers'
], function (Common, Backbone, $) {
    var Provider = Backbone.Model.extend({
        parse: function (options) {
            var data;
            if (_.isObject(options.results)) {
                data = options.results;
            } else {
                data = options;
            }
            if (!data.icon) {
                data.icon = '/static/feti/images/default-provider-logo-sm.png';
            }
            data.counts = data.courses.length;
            return data;
        },
        renderMarker: function () {
            if (!this.get('layer')) {
                var location = this.attributes.location;
                var public_institution = this.attributes.public_institution;
                var markercolor;
                if (public_institution) {
                    markercolor = 'blue leaflet-clickable';
                } else {
                    markercolor = 'red leaflet-clickable';
                }
                var marker = new L.marker([location.lat, location.lng], {
                    icon: L.ExtraMarkers.icon({
                        markerColor: markercolor,
                        icon: 'true',
                        extraClasses: 'fa fa-graduation-cap',
                        iconColor: 'white'
                    })
                });

                var popup = '';

                if ('_campus_popup' in this.attributes) {
                    popup = this.attributes._campus_popup;
                } else {

                    var campus = '';
                    var phone = '';

                    if (typeof this.attributes.campus != 'undefined') {
                        campus = 'Campus : ' + this.attributes.campus;
                    }

                    if (this.attributes.campus_phone && this.attributes.campus_phone != '[]') {
                        phone = this.attributes.campus_phone;
                    } else {
                        phone = '-';
                    }

                    popup = '<div class="leaflet-header"><h3>' +
                        this.attributes.provider +
                        '</h3></div>' +
                        '<div class="leaflet-place"><strong> ' +
                        campus +
                        '</strong></div>' +
                        '<div class="leaflet-content">' +
                        '<div><i class="fa fa-map-marker"></i> ' + this.attributes.address + ' </div>' +
                        '<div><i class="fa fa-link"></i> <a href="' + this.attributes.website + '" target="_blank">' + this.attributes.website + '</a> </div>' +
                        '<div><i class="fa fa-phone"></i> ' + phone + '</div>' +
                        '</div>';
                }


                if (Common.UserLocation != 'None') {
                    var regExp = /\(([^)]+)\)/;
                    var user_location = regExp.exec(Common.UserLocation)[1].split(' ');
                    var origin = user_location[1] + ',' + user_location[0];

                    popup += '<i class="fa fa-map-o" aria-hidden="true"></i>' +
                        ' <a href="https://www.google.com/maps/dir/' + origin + '/' + location.lat + ',' + location.lng + '" target="_blank">' +
                        'Get directions</a>';
                    this.getUserLocation(popup, marker, origin);
                    popup += '<div class="user-location">Calculating travel time... </div>';
                } else {
                    popup += '<i class="fa fa-map-o" aria-hidden="true"></i>' +
                        ' <a href="https://maps.google.com?saddr=My+Location&daddr=' + location.lat + ',' + location.lng + '" target="_blank">' +
                        'Get directions</a>';
                }

                var that = this;

                // Events on marker and popup
                marker.bindPopup(popup);
                marker.off('click');
                marker.on('click', function (e) {
                    e.originalEvent.preventDefault();
                    that.set('marker_clicked', true);
                    this.openPopup();
                });
                marker.on('popupclose', function (e) {
                    that.set('marker_clicked', false);
                });
                this.set('marker', marker);
            }
            this.set('layer', L.featureGroup([this.get('marker')]));
            Common.Dispatcher.trigger('map:addLayerToMode', this.get('layer'));
        },
        getUserLocation: function (popup, marker, origin) {
            var marker_location = this.attributes.location;

            var destinations = marker_location.lat + ',' + marker_location.lng;

            $.ajax({
                url: 'api/travel-time/' + origin + '/' + destinations,
                type: 'GET',
                success: function (response) {
                    popup += '<div class="user-location">Travel time: ' + response + '</div>';
                },
                error: function (response) {
                },
                complete: function () {
                    marker._popup.setContent(popup)
                }
            });
        },
        removeMarker: function () {
            if (this.get('layer')) {
                this.get('layer').clearLayers();
            }
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
        clicked: function () {
            var marker = this.get('marker');
            marker.openPopup();
            Common.Dispatcher.trigger('map:pan', marker._latlng);
        },
    });

    return Provider;
});
