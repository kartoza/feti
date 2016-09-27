define([
    'common',
    '/static/feti/js/scripts/models/occupation.js',
    'text!static/feti/js/scripts/templates/result-detail.html',
    'text!static/feti/js/scripts/templates/step-detail.html'
], function (Common, Occupation, Detail, StepDetail) {
    var OccupationView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-title result-title-occupation',
        template: _.template('<h3><%- title %></h3>'),
        detailTemplate: _.template(Detail),
        stepDetailTemplate: _.template(StepDetail),
        container: '#result-container',
        model: Occupation,
        events: {
            'click': 'clicked'
        },
        clicked: function () {
            Common.Dispatcher.trigger('occupation:clicked', this.model.attributes.id);
            this.update_detail();
        },
        update_detail: function () {
            this.$detail.html(this.detailTemplate(this.model.attributes));
            if (!this.$detail.is(":visible")) {
                this.$detail.show("slide", {direction: "right"}, 500);
            }
            this.renderPathways();
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template(this.model.attributes));
            $(this.container).append(this.$el);
        },
        initialize: function () {
            this.render();
            this.$detail = $('#result-detail');
            Common.Dispatcher.on('occupation-' + this.model.attributes.id + ':routed', this.update_detail, this);
        },
        destroy: function () {
            this.model.destroy();
            this.model = null;
            this.$el.remove();
            return Backbone.View.prototype.remove.call(this);
        },
        renderPathways: function () {
            var that = this;
            var $pathways = this.$detail.find('#pathways');
            $pathways.html('<ul id="tabs"><ul>');
            var pathways = this.model.attributes.pathways;
            var pathway_keys = Object.keys(this.model.attributes.pathways);
            pathway_keys.sort();
            _.each(pathway_keys, function (key) {
                var step_keys = Object.keys(pathways[key]);
                step_keys.sort();
                $('#tabs').append('<li><a href="#tabs-' + key + '">Pathway ' + key + '</a></li>');
                var html = '<div id="tabs-' + key + '"><p>';
                _.each(step_keys, function (step_key) {
                    var step_detail = pathways[key][step_key];
                    step_detail['step_number'] = step_key;
                    html += that.stepDetailTemplate(step_detail);
                });
                html += '</p></div>';
                $pathways.append(html);
            });
            $pathways.tabs();
        }
    });

    return OccupationView;
});
