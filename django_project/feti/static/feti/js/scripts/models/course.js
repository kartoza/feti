/*global define*/
define([
    'common'
], function (Common) {
    var Course = Backbone.Model.extend({
        initialize: function (options) {
            this.attributes = options;
            this.set('marker', options.marker);
        },
        destroy: function () {
            delete this;
        },
        clicked: function () {
            var marker = this.get('marker');
            marker.openPopup();
            Common.Dispatcher.trigger('map:pan', marker._latlng);
        },
    });

    return Course;
});
