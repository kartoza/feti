define([
    'text!static/feti/js/scripts/templates/sharebar.html',
    'common'
], function (sharebarTemplate, Common) {
    var ShareBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#share-container',
        template: _.template(sharebarTemplate),
        events: {
            'click #share-pdf': 'sharePDF',
            'click #share-social-twitter': 'shareToTwitter'
        },
        initialize: function (options) {
            this.render();
            this.parent = options.parent;
        },
        render: function () {
            this.$el.empty();
            this.$el.addClass('share-row');
            this.$el.html(this.template());
            $(this.container).append(this.$el);
        },
        sharePDF: function() {
            var url = '/pdf_report/';

            var currentRoute = Backbone.history.getFragment().split('/');

            if(currentRoute.length > 2) {
                window.location = url + currentRoute[1] + '/' + currentRoute[2];
            }

        },
        shareToTwitter: function () {
            // get url
            var url = Backbone.history.location.href.replace("#", "%23");

            var twitter_intent = 'https://twitter.com/intent/tweet?text=Check this out!%0A'+url;

            // open twitter box
            window.open(twitter_intent, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
        }
    });

    return ShareBarView;
});
