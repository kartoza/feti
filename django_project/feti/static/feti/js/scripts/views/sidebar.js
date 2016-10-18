define([
    'text!static/feti/js/scripts/templates/sidebar.html',
    'common'
], function (sidebarTemplate, Common) {
    var SideBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#result',
        template: _.template(sidebarTemplate),
        events: {
        },
        initialize: function (options) {
            this.render();
            this._parent = options.parent;
            this._isOpen = false;
            this.$result_title = $('#result-title');
            this.$result_detail = $('#result-detail');
            Common.Dispatcher.on('sidebar:change_title', this.showResultTitle, this);
            Common.Dispatcher.on('sidebar:update_title', this.updateResultTitle, this);
        },
        render: function () {
            $(this.container).append(this.template());
        },
        is_open: function () {
            return this._isOpen;
        },
        open: function() {
            this._isOpen = true;
            $(this.container).show("slide", {direction: "right"}, 500);
        },
        close: function () {
            this._isOpen = false;
            $(this.container).hide("slide", {direction: "right"}, 500);
        },
        updateResultTitle: function(number_result, mode, query) {
            this.$result_title.find('#result-title-'+mode).remove();

            var $result_title_number = $("<span>", {class: "result-title-number"});
            $result_title_number.html(number_result);

            var $result_title_mode = $("<span>", {class: "result-title-mode"});
            if(mode == 'occupation') {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  occupations': ' occupation');
            } else {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  campuses': ' campus');
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
        showResultTitle: function(mode) {
            $('#result-title').children().hide();
            $('#result-title-'+mode).show();
        }
    });

    return SideBarView;
});
