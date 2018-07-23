define([
    'common',
    'scripts/models/occupation',
    'text!scripts/templates/result-detail.html',
    'text!scripts/templates/step-detail.html',
    'backbone',
    'jquery',
    'underscore'
], function (
    Common,
    Occupation,
    Detail,
    StepDetail,
    Backbone,
    $,
    _
) {

    var OccupationView = Backbone.View.extend({
        tagName: 'div',
        className: 'result-title result-title-occupation',
        template: _.template('<div class="selected-indicator-right"><i class="fa fa-caret-right" aria-hidden="true"></i> </div><div class="title"><%- occupation %><p><span class="info-occupation-summary">details</span></p></div>'),
        detailTemplate: _.template(Detail),
        stepDetailTemplate: _.template(StepDetail),
        container: '#result-container-occupation',
        model: Occupation,
        occupationDetail: null,
        events: {
            'click .info-occupation-summary': 'occupationDetailsClicked',
            'click': 'occupationClicked'
        },
        hide: function () {
            this.model.hide();
        },
        occupationClicked: function () {
            this.model.removeAllMarkers();
            var that = this;
            $('.selected-indicator-right .fa').hide();
            that.$el.find('.fa').show();
            var $occupationInfo = that.$el.find('.info-occupation-summary');
            if(!$occupationInfo.hasClass('selected')) {
                $('.info-occupation-summary').removeClass('selected');
                this.$detail.hide("slide", {direction: "right"}, 500);
            }
            this.get_campus_provider(this.model.attributes.id);
            Common.Dispatcher.trigger('occupation:clicked', this.model.attributes.id);
        },
        occupationDetailsClicked: function (e) {
            Common.Dispatcher.trigger('occupation:clicked', this.model.attributes.id);
            if(!$(e.currentTarget).hasClass('selected')) {
                $('.info-occupation-summary').removeClass('selected');
                this.update_detail();
            }else {
                this.$detail.hide("slide", {direction: "right"}, 500);
            }
            $(e.currentTarget).toggleClass('selected');
        },
        update_detail: function () {
            // Get occupation detail
            var that = this;
            $('.selected-indicator-right .fa').hide();
            that.$el.find('.fa').show();
            that.$detail.html('<div class="occupation-detail-loading"><img height="100%" src="/static/feti/images/spinner.gif"></div>');
            if(!that.$detail.is(":visible")) {
                that.$detail.show("slide", {direction: "right"}, 500);
            }
            $.ajax({
                url: '/api/occupation?id=' + that.model.attributes.id,
                success: function (response) {
                    that.occupationDetail = response;
                    that.$detail.html(that.detailTemplate(that.occupationDetail));
                    that.renderPathways();
                }
            });
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
            var pathways = this.occupationDetail.pathways;
            var pathway_keys = Object.keys(this.occupationDetail.pathways);
            // sort by number
            pathway_keys.sort(function (a, b) {
                if (isNaN(a) || isNaN(b)) {
                    return a > b ? 1 : -1;
                }
                return a - b;
            });

            // render pathways
            _.each(pathway_keys, function (key) {
                $('#tabs').append('<li><a id="tab-' + key + '" href="#content-tab-' + key + '">Pathway ' + key + '</a></li>');

                var step_keys = Object.keys(pathways[key]).sort();
                var html = '<div id="content-tab-' + key + '"><p>';
                _.each(step_keys, function (step_key) {
                    var step_detail = pathways[key][step_key];
                    step_detail['step_number'] = step_key;
                    html += that.stepDetailTemplate(step_detail);
                });
                html += '</p></div>';
                $pathways.append(html);

                $('#tab-' + key).click(function () {
                    Common.Dispatcher.trigger('occupation:clicked', that.model.attributes.id, key);
                });
            });
            $pathways.tabs();

            // check as default
            if (Common.Router.selected_pathway) {
                $('#tab-' + Common.Router.selected_pathway).click();
            }
        },
        get_campus_provider: function (occupation_id) {
            var that = this;
            $.ajax({
                url: '/api/course-by-occupation?id=' + that.model.attributes.id,
                success: function (data) {
                    that.model.renderMarker(data)
                }
            })
        },
    });

    return OccupationView;
});
