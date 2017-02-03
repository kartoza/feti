define([
    'text!/static/feti/js/scripts/templates/sidebar.html',
    'common'
], function (sidebarTemplate, Common) {
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
            this.$result_detail = $('#result-detail');
            Common.Dispatcher.on('sidebar:categoryClicked', this.showResultTitle, this);
            Common.Dispatcher.on('sidebar:update_title', this.updateResultTitle, this);
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
                this.hideOccupationDetail()
            }
        },
        render: function () {
            $(this.container).append(this.template());
        },
        is_open: function () {
            return this._isOpen;
        },
        open: function () {
            this._isOpen = true;
            $(this.container).show("slide", {direction: "right"}, 500);
            this.showMapCover();
        },
        close: function () {
            this._isOpen = false;
            this.exitOccupation();
        },
        exitOccupation: function () {
            var that = this;
            var $cover = $('#shadow-map');
            if ($cover.is(":visible")) {
                $cover.fadeOut(500);
                $('#result-detail').hide("slide", {direction: "right"}, 500, function () {
                    that.exitResult();
                });
            } else {
                that.exitResult();
            }
        },
        exitResult: function () {
            if ($('#result').is(":visible")) {
                $('#result-toogle').removeClass('fa-caret-right');
                $('#result-toogle').addClass('fa-caret-left');
                $('#result').hide("slide", {direction: "right"}, 500);
            }
        },
        showMapCover: function () {
            if (Common.CurrentSearchMode == 'occupation') {
                var $cover = $('#shadow-map');
                if (!$cover.is(":visible")) {
                    $cover.fadeIn(200);
                }
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
                if (radius % 1000 > 1) {
                    radius = (radius % 1000) + " km"
                } else {
                    radius = radius + " meters"
                }
                $result_title_place.html(' in radius ' + radius + ' from [' + coordinate['lat'].toFixed(3) + " , " + coordinate['lng'].toFixed(3) + "]");
            }
            else {
                $result_title_place.html('');
            }
            $result_title_campus.append($result_title_place);

            this.$result_title.append($result_title_campus);
        },
        showResultTitle: function (newMode, oldMode) {
            $('#result-title-' + oldMode).hide();
            $('#result-title-' + newMode).show();
        }
    });

    return SideBarView;
});
