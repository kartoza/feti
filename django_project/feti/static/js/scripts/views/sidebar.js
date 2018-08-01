define([
    'text!scripts/templates/sidebar.html',
    'common',
    'backbone',
    'jquery',
    'underscore'
], function (sidebarTemplate, Common, Backbone, $, _) {
    var SideBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#result',
        template: _.template(sidebarTemplate),
        events: {},
        initialize: function (options) {
            this.render();
            this._parent = options.parent;
            this._isOpen = false;
            this.$empty_result_div = $('.result-empty');
            this.$loading_div = $('.result-loading');
            this.$result_title = $('#result-title');
            this.$result_filter_data = $('#result-filter-data');
            this.$result_detail = $('#result-detail');
            Common.Dispatcher.on('sidebar:categoryClicked', this.showResultTitle, this);
            Common.Dispatcher.on('sidebar:update_title', this.updateResultTitle, this);
            Common.Dispatcher.on('sidebar:update_filter_data', this.updateFilterData, this);
            Common.Dispatcher.on('sidebar:show_loading', this.addLoadingView, this);
            Common.Dispatcher.on('sidebar:hide_loading', this.clearContainerDiv, this);
            Common.Dispatcher.on('sidebar:clear_search', this.clearSidebar, this);
        },
        showOccupationDetail: function () {
           this.$result_detail.show("slide", {direction: "right"}, 300);
        },
        hideOccupationDetail: function () {
            if (this.$result_detail.is(":visible")) {
                this.$result_detail.hide("slide", {direction: "right"}, 300);
            }
        },
        updateOccupationDetail: function () {
            if (!Common.Router.selected_occupation) {
                this.hideOccupationDetail();
            }
        },
        render: function () {
            $(this.container).append(this.template());
        },
        is_open: function () {
            return this._isOpen;
        },
        open: function () {
            var that = this;
            $(this.container).show("slide", {direction: "right"}, 500, function () {
                that._isOpen = true;
            });
            this.showMapCover();
        },
        close: function () {
            this._isOpen = false;
            this.exitOccupation();
        },
        exitOccupation: function (exitMap) {
            Common.Dispatcher.trigger('occupation:removeAllMarker');
        },
        exitResult: function (exitMap) {
        },
        showMapCover: function () {
            if (Common.CurrentSearchMode == 'occupation') {
                var $cover = $('#shadow-map');
            }
        },
        hideMapCover: function () {
            if (Common.CurrentSearchMode != 'occupation') {
                var $cover = $('#shadow-map');
                if ($cover.is(":visible")) {
                    $cover.fadeOut(200);
                }
            }
        },
        addLoadingView: function (mode) {
            this.clearContainerDiv(mode);
            this.$result_title.find('#result-title-' + mode).remove();
            $('#result-container-' + mode).append(this.$loading_div.show());

            // for embed version
            if (Common.EmbedVersion) {
                $("#embed-loading-wrapper").show();
                $("#embed-loading-wrapper").append(this.$loading_div.show());
                var $embedLoadingWrapper = $("#embed-loading-wrapper");
                if ($embedLoadingWrapper.find(".result-loading").width() > $embedLoadingWrapper.width()) {
                    $embedLoadingWrapper.find(".result-loading").width($embedLoadingWrapper.width());
                    $embedLoadingWrapper.find("img").width($embedLoadingWrapper.width());
                }
            }
        },
        clearSidebar: function (mode) {
            $('#result-container-' + mode).empty();
            this.$result_title.find('#result-title-' + mode).remove();
            Common.Dispatcher.trigger('occupation:removeAllMarker');
        },
        showEmptyResult: function (mode) {
            var $_empty_result_div = this.$empty_result_div.clone();
            $('#result-container-' + mode).append($_empty_result_div.show());
        },
        clearContainerDiv: function (mode) {
            if ($('#result-container-' + mode + ' .result-empty').length > 0) {
                $('#result-container-' + mode + ' .result-empty').remove();
            }
            if ($('#result-container-' + mode + ' .result-loading').length > 0) {
                $('#result-container-' + mode + ' .result-loading').remove();
            }
            // for embed version
            if (Common.EmbedVersion) {
                $("#embed-loading-wrapper").hide();
                $("#embed-loading-wrapper .result-loading").remove();
            }
        },
        updateFilterData: function(data){
            /**
             * Data Sent
             * course
                    :
                    Object
                    field-of-study-select:null
                    minimum-credits:0
                    nqf-level-select:null
                    qualification-type-select:null
                    subfield-of-study-select:null
                    __proto__:Object

                    provider:
                    Object
                    field-of-study-provider-select:"2"
                    public-institution-select:"1"
             */

            var $labels = "";
            var $spanLabel = "<span class='badge badge-warning'>";
            if(data.course["field-of-study-select"] != null){
                val = $("select#field-of-study-select option:selected").text();
                $labels += $spanLabel + "Field Of Study : " + val + "</span>";
            }

            if(data.course["minimum-credits"] != 0){
                val = data.course["minimum-credits"];
                $labels += $spanLabel + "Minimum Credits : " + val + "</span>";
            }

            if(data.course["nqf-level-select"] != null){
                val = $("select#nqf-level-select option:selected").text();
                $labels += $spanLabel + "NQF Level : " + val + "</span>";
            }

            if(data.course["qualification-type-select"] != null){
                val = $("select#qualification-type-select option:selected").text();
                $labels += $spanLabel + "Qualification Type : " + val + "</span>";
            }

            if(data.course["subfield-of-study-select"] != null){
                val = $("select#subfield-of-study-select option:selected").text();
                $labels += $spanLabel + "Subfield of Study : " + val + "</span>";
            }

            if(data.provider["field-of-study-provider-select"] != null){
                val = $("select#field-of-study-provider-select option:selected").text();
                $labels += $spanLabel + "Field of Study Provider : "+ val + "</span>";
            }

            if(data.provider["public-institution-select"] != null){
                val = $("select#public-institution-select option:selected").text();
                $labels += $spanLabel + "Institution : " + val + "</span>";
            }

            this.$result_filter_data.html($labels);
        },
        updateResultTitle: function (number_result, mode, query) {
            this.clearContainerDiv(mode);
            if (number_result == 0) {
                this.showEmptyResult(mode);
            }
            this.$result_title.find('#result-title-' + mode).remove();

            var $result_title_number = $("<span>", {class: "result-title-number"});
            $result_title_number.html(number_result);

            var $result_title_mode = $("<span>", {class: "result-title-mode"});
            if (mode == 'occupation') {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  occupations' : ' occupation');
            } else {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  campuses' : ' campus');
            }

            var $result_title_campus = $("<div>", {id: "result-title-" + mode});
            $result_title_campus.append($result_title_number);
            $result_title_campus.append($result_title_mode);

            var $result_title_place = $("<span>", {class: "result-title-place"});

            if (query.indexOf("administrative") >= 0) {
                query = query.split("=")[1];
                query = query.split();
                query.reverse();
                $result_title_place.html(' in ' + query.join().replace(",", ", "));
            } else if (query.indexOf("circle") >= 0) {
                var coordinates_index = query.indexOf("coordinate=") + "coordinate=".length;
                var radius_index = query.indexOf("&radius=");
                var coordinates = query.substring(coordinates_index, radius_index);
                radius_index = query.indexOf("&radius=") + "&radius=".length;
                var radius = parseInt(query.substring(radius_index, query.length));
                var coordinate = JSON.parse(coordinates);
                if (radius / 1000 > 1) {
                    radius = (radius / 1000) + " km"
                } else {
                    radius = radius + " meters"
                }
                $result_title_place.html(' in radius ' + radius + ' from [' + coordinate['lat'].toFixed(3) + " , " + coordinate['lng'].toFixed(3) + "]");
                this.$result_filter_data.css("margin-top",60);
            } else if(query.indexOf("circle") < 0){
                this.$result_filter_data.css("margin-top",40);
            }
            else {
                $result_title_place.html('');
            }
            $result_title_campus.append($result_title_place);

            this.$result_title.append($result_title_campus);

            var $height = this.$result_filter_data.height() +
                /*space margin */
                parseInt($("#result-filter-data").css("margin-top")) + 10;
            $('#result-container-wrapper').css('padding-top',$height);
        },
        showResultTitle: function (newMode, oldMode) {
            Common.Dispatcher.trigger('occupation:removeAllMarker');
            $('#result-title-' + oldMode).hide();
            $('#result-title-' + newMode).show();
        }
    });

    return SideBarView;
});
