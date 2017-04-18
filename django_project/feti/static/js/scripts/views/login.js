define([
    'common',
    'backbone',
    'jquery'
], function (Common, Backbone, $) {
    var LoginModalView = Backbone.View.extend({
        id: 'login-modal',
        className: 'modal fade',
        template: null,
        last_route: '',
        setLastRoute: function (last_route) {
            if(last_route)
                this.last_route = last_route;
        },
        events: {
            'hidden.bs.modal': 'teardown'
        },
        initialize: function () {
            if ($('#login-modal-template').length > 0) {
                this.template = _.template($('#login-modal-template').html());
            }
            _.bindAll(this, 'show', 'teardown', 'render', 'hide');
            this.render();
        },

        show: function () {
            this.$el.find('#login-next').val('/#' + this.last_route);
            this.$el.modal('show');
        },

        hide: function () {
            this.$el.modal('hide');
        },

        teardown: function () {
            Common.Router.back('login');
        },

        render: function () {
            if (this.template) {
                this.$el.html(this.template());
                if(typeof this.$el !== 'undefined') {
                    this.$el.modal({show: false});
                }
            }
            return this;
        }
    });

    return LoginModalView;
});
