/**
 * Created by meomancer on 08/08/16.
 */
var SearchResult = Backbone.Model.extend({
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
        if (this.attributes.location) {
            var location = this.attributes.location.split("(")[1].replace(")", "").split(" ");
            // not sure is the best way
            this.marker = new L.marker([parseFloat(location[1]), parseFloat(location[0])]).bindPopup(this.attributes._campus_popup);
            this.set('layer', L.layerGroup([this.marker]));
            dispatcher.trigger('map:addLayer', this.get('layer'));
        }
    },
    destroy: function () {
        // destroy by remove layers and delete this object
        if (this.get('layer')) {
            this.get('layer').clearLayers();
        }
        delete this;
    },
    clicked: function () {
        var location = this.attributes.location.split("(")[1].replace(")", "").split(" ");
        this.marker.openPopup();
        dispatcher.trigger('map:pan', new L.LatLng(parseFloat(location[1]), parseFloat(location[0])));
    }
});