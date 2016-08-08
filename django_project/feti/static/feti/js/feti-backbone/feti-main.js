/**
 * Created by meomancer on 08/08/16.
 */
// A $( document ).ready() block.
var dispatcher = _.extend({}, Backbone.Events);
$(document).ready(function () {
    var map_view = new MapView();
    var campus_collection = new CampusCollection();
    campus_collection.fetch({
        success: function () {
            _.each(campus_collection.models, function (model) {
                campus_collection.campus_views.push(new CampusView({
                    model: model,
                    id: "campus_" + model.get('id'),
                }));
            });
        }
    });
});