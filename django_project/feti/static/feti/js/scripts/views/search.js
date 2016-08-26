define([
    'common',
    '/static/feti/js/scripts/models/search.js'
], function (Common, SearchResult) {
    var SearchResultView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-row',
        template: _.template('<%- provider %>'),
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
        },
        destroy: function () {
            this.model.destroy();
            this.$el.remove();
            return Backbone.View.prototype.remove.call(this);
        }
    });

    return SearchResultView;
});
