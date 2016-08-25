define([], function () {
    var LoginModalView = Backbone.View.extend({
        id: 'login-modal',
        className: 'modal fade',
        template: _.template($('#login-modal-template').html()),
        events: {
            'hidden.bs.modal': 'teardown'
        },

        initialize: function() {
            _.bindAll(this, 'show', 'teardown', 'render', 'hide');
            this.render();
        },

        show: function() {
            this.$el.modal('show');
        },

        hide: function () {
            this.$el.modal('hide');
        },

        teardown: function() {
            Backbone.history.navigate('');
        },

        render: function() {
            this.$el.html(this.template());
            this.$el.modal({show:false});
            return this;
        }
    });

    return LoginModalView;
});


