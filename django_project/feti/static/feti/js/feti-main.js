/**
 * Created by Dimas Ciputra <dimas@kartoza.com> on 08/08/16.
 */
/* Backbone apps */

// Map view
var MapView = Backbone.View.extend({
    template: _.template($('#map-template').html()),
    render: function () {
        this.$el.html(this.template());

        var map = L.map(this.$('#feti-map')[0]).setView([-29, 20], 6);
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        return this;
    }
});

var mapView = new MapView();
$('#map-container').append(mapView.el);
mapView.render();

