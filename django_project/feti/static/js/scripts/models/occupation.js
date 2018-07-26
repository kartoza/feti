/*global define*/
define([
    'common',
    'text!scripts/templates/campus-popup.html',
    'backbone',
    'underscore',
    'leafletExtraMarkers'
], function (Common, popupTemplate, Backbone, _) {
    var markersCollection = [];
    var Occupation = Backbone.Model.extend({
        template: _.template(popupTemplate),
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
            this.layerGroup = L.featureGroup();
            if (!this.get('layer')) {
                for(var i=0; i<data.length; i++){
                    var object=data[i];
                    var location = object['location'];
                    var public_institution = object['public_institution'];
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
                    object['campus'] = 'Campus : ' + object['campus'];
                    popup = this.template(object);

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
                    this.layerGroup.addLayer(marker);
                }
            }
            this.set('layer', this.layerGroup);
            markersCollection.push(this.layerGroup);
            Common.Dispatcher.trigger('map:addLayer', this.get('layer'));
            Common.Dispatcher.trigger('map:pan', [location.coordinates[1], location.coordinates[0]]);
            this.set('layer', null)
        },
        removeAllMarkers: function () {
            $.each(markersCollection, function (key, marker) {
                Common.Dispatcher.trigger('map:removeLayer', marker);
            })
        }
    });

    return Occupation;
});
