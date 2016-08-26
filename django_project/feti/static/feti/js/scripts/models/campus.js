/*global define*/
define([
    'common'
], function (Common) {

	var Campus = Backbone.Model.extend({
        parse: function (options) {
            var data;
            if (_.isObject(options.results)) {
                data = options.results;
            } else {
                data = options;
            }
            return data;
        },
        destroy: function (options) {
            return Backbone.Model.prototype.destroy.call(this, options);
        },
        renderMarker: function () {
            if (this.attributes.location) {
                var location = this.attributes.location.split("(")[1].replace(")", "").split(" ");
                // not sure is the best way
                this.marker = new L.marker([parseFloat(location[1]), parseFloat(location[0])]).bindPopup(this.attributes._campus_popup);
                Common.Dispatcher.trigger('map:addLayer', this.marker);
            }
        }
    });

	return Campus;
});
