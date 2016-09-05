/*global define*/
define([
    'common'
], function (Common) {
    var Course = Backbone.Model.extend({
        initialize: function (options) {
            this.attributes = options;
        },
        destroy: function () {
            delete this;
        },
    });

    return Course;
});
