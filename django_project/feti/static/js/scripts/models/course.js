/*global define*/
define([
    'common',
    'backbone'
], function (Common, Backbone) {
    var Course = Backbone.Model.extend({
        initialize: function (options) {
            this.attributes = options;
            if (this.attributes.national_learners_records_database) {
                this.attributes.national_learners_records_database = "[" + this.attributes.national_learners_records_database + "]";
            }
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
