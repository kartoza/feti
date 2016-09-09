define([
    'text!static/feti/js/scripts/templates/sharebar.html',
    'common'
], function (sharebarTemplate, Common) {
    var ShareBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#share-container',
        template: _.template(sharebarTemplate),
        events: {
            'click #share-pdf': 'clicked'
        },
        initialize: function (options) {
            this.render();
        },
        clicked: function () {
            alert('share pdf');
        },
        render: function () {
            this.$el.empty();
            this.$el.addClass('share-row');
            this.$el.html(this.template());
            $(this.container).append(this.$el);
        }
    });

    return ShareBarView;
});
