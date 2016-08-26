/*global define*/
define([
    'common'
], function (Common) {

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

	return Course;
});
