/*global define*/
define([
    'common',
    'backbone',
    'underscore'
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
        destroy: function () {
            delete this;
        },
        renderMarker: function () {

        },
    });

    return Occupation;
});
