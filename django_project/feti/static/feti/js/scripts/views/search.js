define([
    'common',
    '/static/feti/js/scripts/models/search.js'
], function (Common, SearchResult) {
    var SearchResultView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-row',
        template: _.template('<%- provider %> [<%- locations.length %>]'),
        container: '#providers',
        model: SearchResult,
        events: {
            'click': 'clicked'
        },
        clicked: function () {
            this.model.clicked();
            return false;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
            this.model.renderMarker();
        },
        initialize: function () {
            this.render();
            Common.Dispatcher.on('map:moved', this.map_moved_handle, this);
        },
        map_moved_handle: function (minx, miny, maxx, maxy) {
            var latlng = this.model.attributes.location;
            if (latlng) {
                if (maxx < latlng.lng || minx > latlng.lng || maxy < latlng.lat || miny > latlng.lat) {
                    this.model.removeMarker();
                } else {
                    this.model.renderMarker();
                }
            }
        },
        destroy: function () {
            this.model.destroy();
            this.$el.remove();
            return Backbone.View.prototype.remove.call(this);
        }
    });

    return SearchResultView;
});
