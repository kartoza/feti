/**
 * Created by meomancer on 08/08/16.
 */
var Course = Backbone.Model.extend({
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
    }
});

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
    render_marker: function () {
        var location = this.attributes.location.split("(")[1].replace(")", "").split(" ");
        // not sure is the best way
        this.marker = new L.marker([parseFloat(location[1]), parseFloat(location[0])]).bindPopup(this.attributes._campus_popup);
        dispatcher.trigger('map:add_layer', this.marker);
    }
});