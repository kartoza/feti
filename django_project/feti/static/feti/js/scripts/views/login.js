define([
    'common'
], function (Common) {
    var LoginModalView = Backbone.View.extend({
        id: 'login-modal',
        className: 'modal fade',
        template: null,
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
                this.$el.modal({show: false});
            }
            return this;
        }
    });

    return LoginModalView;
});
