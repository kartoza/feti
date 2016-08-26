/*global define */
define([
	'/static/feti/js/scripts/models/campus.js'
], function (Campus) {

    var CampusCollection = Backbone.Collection.extend({
        model: Campus,
        campus_views: [],
        url: function () {
            return "/api/campuss/";
        }
    });

	return new CampusCollection();
});
