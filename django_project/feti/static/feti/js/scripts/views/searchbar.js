define([
    'text!static/feti/js/scripts/templates/searchbar.html',
    'common',
    '/static/feti/js/scripts/collections/search.js',
    '/static/feti/js/scripts/views/sharebar.js'
], function (searchbarTemplate, Common, searchCollection, SharebarView) {
    var SearchBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#map-search',
        template: _.template(searchbarTemplate),
        events: {
            'click #where-to-study': 'categoryClicked',
            'click #what-to-study': 'categoryClicked',
            'click #choose-occupation': 'categoryClicked',
            'click #back-home': 'backHomeClicked',
            'click #result-toogle': 'toogleResult',
            'click #draw-polygon': 'drawModeSelected',
            'click #draw-circle': 'drawModeSelected',
            'click #cancel-draw-polygon': 'cancelDrawClicked',
            'click #cancel-draw-circle': 'cancelDrawClicked',
            'click #clear-draw': 'clearAllDraw'
        },
        initialize: function (options) {
            this.render();
            $("#result-toogle").hide();
            this.$search_bar = $(".search-bar");
            this.$search_bar_input = $("#search-bar-input");
            this.$provider_button = $("#where-to-study");
            this.$course_button = $("#what-to-study");
            this.$occupation_button = $("#choose-occupation");
            this.$result_loading = $("#result-loading");
            this.$result_empty = $("#result-empty");
            this.$clear_draw = $("#clear-draw");
            this.search_bar_hidden = true;
            this.parent = options.parent;
            this.initAutocomplete();
            this.shareBarView = new SharebarView({parent: this});
            Common.Dispatcher.on('search:finish', this.searchingFinish, this);
            Common.Dispatcher.on('occupation:clicked', this.occupationClicked, this);

            this._drawer = {
                polygon: this._initializeDrawPolygon,
                circle: this._initializeDrawCircle
            }
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template());
            $(this.container).append(this.$el);
            // form submit
            var that = this;
            $("#search-form").submit(function (e) {
                that.searchRouting();
                e.preventDefault(); // avoid to execute the actual submit of the form.
            });
        },
        initAutocomplete: function () {
            var that = this;
            this.$search_bar_input.autocomplete({
                source: function (request, response) {
                    that.$search_bar_input.css("cursor", "wait");
                    var url = "/api/autocomplete/" + that.categorySelected();
                    $.ajax({
                        url: url,
                        data: {
                            q: request.term
                        },
                        success: function (data) {
                            that.$search_bar_input.css("cursor", "");
                            response(data);
                        },
                        error: function (request, error) {
                            that.$search_bar_input.css("cursor", "");
                        },
                    });
                },
                minLength: 3,
                select: function (event, ui) {
                    $(this).val(ui.item.value);
                    $("#search-form").submit()
                },
                open: function () {
                    //$(this).removeClass("ui-corner-all").addClass("ui-corner-top");
                },
                close: function () {
                    //$(this).removeClass("ui-corner-top").addClass("ui-corner-all");
                }
            });
            var width = this.$search_bar_input.css('width');
            $('.ui-autocomplete').css('width', width);
        },
        categoryClicked: function (event) {
            this.changeCategoryButton($(event.target).data("mode"));
            this.searchRouting();
            this.trigger('categoryClicked', event);
        },
        backHomeClicked: function (e) {
            this.exitOccupation(e);
            this.trigger('backHome', e);
        },
        updateRouting: function (filter) {
            // update route based on query and filter
            var that = this;
            var new_url = ['map'];
            var mode = that.categorySelected();
            if (mode == "occupation") {
                this.clearAllDrawWithoutRouting();
                this.disableFilterResult();
            } else {
                this.enableFilterResult();
            }

            var query = that.$search_bar_input.val();
            new_url.push(mode);
            if (query) {
                new_url.push(query);
                if (filter) {
                    new_url.push(filter);
                } else {
                    // Get coordinates query from map
                    var coordinates = this.parent.getCoordinatesQuery();
                    if (coordinates) {
                        new_url.push(coordinates);
                    }
                }
            }
            return new_url;
        },
        searchRouting: function (filter) {
            var new_url = this.updateRouting(filter);
            Backbone.history.navigate(new_url.join("/"), true);
        },
        occupationClicked: function (id, pathway) {
            Common.Router.inOccupation = true;
            var new_url = this.updateRouting();
            new_url.push(id);
            if (pathway) {
                new_url.push(pathway);
            }
            Backbone.history.navigate(new_url.join("/"), false);
        },
        search: function (mode, query, filter) {
            this.$search_bar_input.val(query);
            if (!filter) {
                this.clearAllDraw();
            } else {
                var filters = filter.split('&');

                if (filters[0].split('=').pop() == 'polygon') { // if polygon
                    var coordinates_json = JSON.parse(filters[1].split('=').pop());
                    var coordinates = [];
                    _.each(coordinates_json, function (coordinate) {
                        coordinates.push([coordinate.lat, coordinate.lng]);
                    });
                    this.parent.createPolygon(coordinates);
                } else if (filters[0].split('=').pop() == 'circle') { // if circle
                    var coords = JSON.parse(filters[1].split('=').pop());
                    var radius = filters[2].split('=').pop();
                    this.parent.createCircle(coords, radius);
                }
            }

            // search
            searchCollection.search(mode, query, filter);
            this.in_show_result = true;
            this.$result_loading.show();
            this.$result_empty.hide();
            this.showResult();
        },
        searchingFinish: function (is_not_empty) {
            this.$result_loading.hide();
            this.shareBarView.show();

            if (!is_not_empty) { // empty
                this.shareBarView.hide();
                this.$result_empty.show();
            }
            if (Common.Router.selected_occupation) {
                Common.Dispatcher.trigger('occupation-' + Common.Router.selected_occupation + ':routed');
            } else {
                if ($('#result-detail').is(":visible")) {
                    $('#result-detail').hide("slide", {direction: "right"}, 500);
                }
            }
        },
        showResult: function () {
            var that = this;
            if (this.map_in_fullscreen) {
                var $toogle = $('#result-toogle');
                if ($toogle.hasClass('fa-caret-left')) {
                    $toogle.removeClass('fa-caret-left');
                    $toogle.addClass('fa-caret-right');
                    if (!$('#result').is(":visible")) {
                        $('#result').show("slide", {direction: "right"}, 500, function () {
                            that.in_show_result = false;
                        });
                    }
                }
            }
        },
        toogleResult: function (event) {
            if ($(event.target).hasClass('fa-caret-left')) {
                $(event.target).removeClass('fa-caret-left');
                $(event.target).addClass('fa-caret-right');
                if (!$('#result').is(":visible")) {
                    if (this.categorySelected() == 'occupation') {
                        $('#shadow-map').fadeIn(500);
                    }
                    $('#result').show("slide", {direction: "right"}, 500, function () {
                        if (Common.Router.selected_occupation) {
                            $('#result-detail').show("slide", {direction: "right"}, 500);
                        }
                    });
                }
            } else {
                $(event.target).removeClass('fa-caret-right');
                $(event.target).addClass('fa-caret-left');
                if ($('#result-detail').is(":visible")) {
                    $('#result-detail').hide("slide", {direction: "right"}, 500, function () {
                        $('#shadow-map').fadeOut(500);
                        if ($('#result').is(":visible")) {
                            $('#result').hide("slide", {direction: "right"}, 500);
                        }
                    });
                } else {
                    $('#shadow-map').fadeOut(500);
                    if ($('#result').is(":visible")) {
                        $('#result').hide("slide", {direction: "right"}, 500);
                    }

                }
            }
        },
        drawModeSelected: function (event) {
            if (!$(event.target).hasClass('disabled')) {
                this.cancelDraw('circle');
                this.cancelDraw('polygon');

                this.$el.find('.search-bar').find('.m-button').removeClass('active');
                $(event.target).addClass('active');
                var selected = $(event.target).get(0).id;

                var drawer = this._drawer[selected.split('-').pop()];
                drawer.call(this);
                this.clearAllDraw();
            }
        },
        _initializeDrawPolygon: function () {
            $('#draw-polygon').hide();
            $('#cancel-draw-polygon').show();
            // enable polygon drawer
            this.parent.enablePolygonDrawer();
        },
        _initializeDrawCircle: function () {
            $('#draw-circle').hide();
            $('#cancel-draw-circle').show();
            // enable circle drawer
            this.parent.enableCircleDrawer();
        },
        cancelDrawClicked: function (element) {
            var shape = $(element.target).attr('id').split('-').pop();
            this.cancelDraw(shape);
        },
        cancelDraw: function (shape) {
            if (shape == 'circle') {
                this.parent.disableCircleDrawer();
            } else if (shape == 'polygon') {
                this.parent.disablePolygonDrawer();
            }
            $('#draw-' + shape).show();
            $('#cancel-draw-' + shape).hide();
            this.$el.find('.search-bar').find('.m-button').removeClass('active');
        },
        clearAllDrawWithoutRouting: function () {
            $('#clear-draw').hide();
            // remove all drawn layer in map
            this.parent.clearAllDrawnLayer();
            this.parent.layerAdministrativeView.resetBasedLayer();
        },
        clearAllDraw: function () {
            this.clearAllDrawWithoutRouting();
            this.searchRouting();
        },
        showClearDrawButton: function () {
            $('#clear-draw').show();
        },
        categorySelected: function () {
            var button = this.$el.find('.search-category').find('.m-button.active');
            if (button[0]) {
                return $(button[0]).attr("data-mode");
            } else {
                return "";
            }
        },
        // Draw Events
        onFinishedCreatedShape: function (shape) {
            this.cancelDraw(shape);
            this.showClearDrawButton();
            this.searchRouting();
            this.parent.layerAdministrativeView.resetBasedLayer();
        },
        changeCategoryButton: function (mode) {
            this.$el.find('.search-category').find('.m-button').removeClass('active');
            var $button = null;
            var highlight = "Choose what are you looking for";
            if (mode == "provider") {
                $button = this.$provider_button;
                highlight = 'Search for provider';
            } else if (mode == "course") {
                $button = this.$course_button;
                highlight = 'Search for courses';
            } else if (mode == "occupation") {
                $button = this.$occupation_button;
                highlight = 'Search for occuption';
            }

            // change placeholder of input
            this.$search_bar_input.attr("placeholder", highlight);
            if ($button) {
                $button.addClass('active');
                this.showSearchBar(0);
                Common.CurrentSearchMode = mode;
            }
        },
        mapResize: function (is_resizing) {
            this.map_in_fullscreen = is_resizing;
            if (is_resizing) { // To fullscreen
                this.$('#back-home').show();
                this.$('#result-toogle').show();
                if (this.in_show_result) {
                    this.showResult();
                }
            } else { // Exit fullscreen
                this.$('#back-home').hide();
                this.$('#result-toogle').hide();
            }
        },
        showSearchBar: function (speed) {
            if (this.search_bar_hidden) {
                this.$search_bar.slideToggle(speed);
                // zoom control animation
                var $zoom_control = $('.leaflet-control-zoom');
                $zoom_control.animate({
                    marginTop: '+=55px'
                }, speed);
                var $result = $('#result');
                $result.animate({
                    paddingTop: '+=55px'
                }, speed);

                // now it is shown
                this.search_bar_hidden = false;
            }
        },
        hideSearchBar: function (e) {
            if (!this.search_bar_hidden) {
                this.$search_bar.slideToggle(500, function () {
                    Common.Dispatcher.trigger('map:exitFullScreen');
                });
                // zoom control animation
                var $zoom_control = $('.leaflet-control-zoom');
                $zoom_control.animate({
                    marginTop: '-=55px'
                }, 500);

                // now it is shown
                this.search_bar_hidden = true;
            }
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
                $('#result').hide("slide", {direction: "right"}, 500, function () {
                    Common.Dispatcher.trigger('map:exitFullScreen');
                });
            } else {
                Common.Dispatcher.trigger('map:exitFullScreen');
            }
        },
        enableFilterResult: function () {
            $('#draw-polygon').removeClass('disabled');
            $('#draw-circle').removeClass('disabled');
        },
        disableFilterResult: function () {
            this.cancelDraw('circle');
            this.cancelDraw('polygon');
            $('#draw-polygon').addClass('disabled');
            $('#draw-circle').addClass('disabled');
        }
    });

    return SearchBarView;
});