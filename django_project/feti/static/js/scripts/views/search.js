define([
    'text!scripts/templates/searchbar.html',
    'common',
    'scripts/collections/occupation',
    'scripts/collections/campus',
    'scripts/collections/course',
    'scripts/collections/favorites'
], function (searchbarTemplate, Common, occupationCollection, campusCollection, courseCollection, favoritesCollection) {
    var SearchBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#map-search',
        template: _.template(searchbarTemplate),
        events: {
            'click #where-to-study': '_categoryClicked',
            'click #what-to-study': '_categoryClicked',
            'click #choose-occupation': '_categoryClicked',
            'click #favorites': '_categoryClicked',
            'click #result-toogle': 'toogleResult',
            'click #search-clear': 'clearSearch',
            'click #show-filter-button': 'showFilterPanel',
            'click #hide-filter-button': 'hideFilterPanel',
            'change #field-of-study-select': 'filterChanged',
            'change #qualification-type-select': 'filterChanged',
            'change #subfield-of-study-select': 'filterChanged',
            'change #nqf-level-select': 'filterChanged',
            'change #public-institution-select': 'filterChanged',
            'change #field-of-study-provider-select': 'filterChanged',
            'click #search-icon': 'searchIconClicked',
            'click #search-with-filter': 'searchIconClicked',
            'click #clear-filter' : 'clearFilters'
        },
        initialize: function (options) {
            this.render();
            this.$result_toggle = $('#result-toogle');
            this.$search_bar = $(".search-bar");
            this.$search_bar_input = $("#search-bar-input");
            this.$search_form = $("#search-form");
            this.$provider_button = $("#where-to-study");
            this.$course_button = $("#what-to-study");
            this.$occupation_button = $("#choose-occupation");
            this.$favorites_button = $("#favorites");
            this.$clear_draw = $("#clear-draw");
            this.$search_clear = $("#search-clear");
            this.$filter_tag_label = $('#filter-tag');

            this.$filter_panel_course = $('.filter-panel-course');
            this.$filter_panel_campus = $('.filter-panel-campus');
            this.$filter_panel_button = $('.filter-panel-button');

            this.$search_clear.hide();
            this.$filter_tag_label.hide();

            this.search_bar_hidden = true;
            this.$result_toggle.hide();
            this.parent = options.parent;
            this.initAutocomplete();
            Common.Dispatcher.on('toogle:result', this.toogleResult, this);
            Common.Dispatcher.on('search:finish', this.onFinishedSearch, this);
            Common.Dispatcher.on('occupation:clicked', this.occupationClicked, this);
            Common.Dispatcher.on('favorites:added', this._favoriteAdded, this);
            Common.Dispatcher.on('favorites:deleted', this._favoriteDeleted, this);
            Common.Dispatcher.on('search:updateRouter', this.updateSearchRoute, this);

            this._drawer = {
                polygon: this._initializeDrawPolygon,
                circle: this._initializeDrawCircle
            };
            this._addResponsiveTab($('.nav.nav-tabs'));
            this._search_query = {};
            this._search_filter = {};
            this._search_results = {};
            this._search_need_update = {
                'provider': false,
                'course': false,
                'favorite': false
            };

            var that = this;

            // Flag to show search is initiated through search form
            this.isSearchFromInput = false;

            this.$search_form.submit(function (e) {
                e.preventDefault(); // avoid to execute the actual submit of the form.
                that.isSearchFromInput = true;
                that.updateSearchRoute();
            });
            this.$search_bar_input.keyup(function(e){
                if(e.keyCode == 13)
                {
                    if(that.$search_bar_input.val()) {
                        that.isSearchFromInput = true;
                        that.updateSearchRoute();
                    }
                }
            });

            this.loadFilters();
        },
        searchIconClicked: function (e) {
            this.isSearchFromInput = true;
            this.updateSearchRoute();
        },
        render: function () {
            this.$el.empty();
            var attributes = {
                'is_logged_in': Common.IsLoggedIn
            };
            this.$el.html(this.template(attributes));
            $(this.container).append(this.$el);
        },
        initAutocomplete: function () {
            var that = this;
            var enter_clicked = false;

            this.$search_bar_input.autocomplete({
                source: function (request, response) {
                    if(!enter_clicked) {
                        that.$search_bar_input.css("cursor", "wait");
                        var url = "/api/autocomplete/" + Common.CurrentSearchMode;
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
                            }
                        });
                    }
                    enter_clicked = false;
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
            }).keyup(function (e) {
                if(e.which === 13) {
                    enter_clicked=true;
                }
            });
            var width = this.$search_bar_input.css('width');
            $('.ui-autocomplete').css('width', width);
        },
        getSearchRoute: function (filter) {
            var that = this;
            var new_url = ['map'];
            var mode = this.$el.find('.search-category').find('.search-option.active').data('mode');
            Common.CurrentSearchMode = mode;
            var query = '';

            if(this.isSearchFromInput) {
                query = that.$search_bar_input.val();
                if(mode != 'occupation' && mode != 'favorites')
                    query += that.getAdvancedFilters();
                this.isSearchFromInput = false;
            } else {
                query = that._search_query[mode];
            }

            if (!query && mode in this._search_query) {
                query = this._search_query[mode];
            }
            if (query == "" && mode != 'favorites') {
                this.parent.closeResultContainer($('#result-toogle'));
            }
            new_url.push(mode);
            new_url.push(query);

            if (filter) {
                new_url.push(filter);
            } else {
                // Get coordinates query from map
                var coordinates = this.parent.getCoordinatesQuery(mode);
                if (coordinates) {
                    new_url.push(coordinates);
                }
            }

            if (mode == 'favorites') {
                // Remove empty strings from array if there is filter
                new_url.clean("");
            }

            return new_url;
        },
        updateSearchRoute: function (filter) {
            // update route based on query and filter
            var new_url = this.getSearchRoute(filter);
            Common.Dispatcher.trigger('sidebar:update_filter_data',this.filtersInMode);
            Backbone.history.navigate(new_url.join("/"), true);
        },
        _categoryClicked: function (event) {
            event.preventDefault();
            if (!$(event.target).parent().hasClass('active')) {

                var mode = $(event.target).parent().data("mode");

                // Change active button
                this.changeCategoryButton(mode);

                this.clearFilters(event, true);

                // Trigger category click event
                Common.Dispatcher.trigger('sidebar:categoryClicked', mode, Common.CurrentSearchMode);

                this.clearSearch(event);

                Common.CurrentSearchMode = mode;

                if (mode != 'favorites') {
                    // Hide search bar if in favorite mode
                    $('.search-row').show();
                    Common.Dispatcher.trigger('map:hideShareBar');
                }

                if (mode != 'occupation') {
                    if ($('#result-detail').is(":visible")) {
                        $('#result-detail').hide("slide", {direction: "right"}, 500);
                    }
                }

                if (mode == 'occupation' || mode == 'favorites') {
                    this.$filter_tag_label.hide();
                } else {
                    // Update filters
                    this.updateFilters(mode);
                    $('.filter-button').show();
                }
            }
        },
        _favoriteAdded: function (mode) {
            for (var key in this._search_need_update) {
                if (this._search_need_update.hasOwnProperty(key)) {
                    if (key != mode) {
                        this._search_need_update[key] = true;
                    }
                }
            }
        },
        _favoriteDeleted: function (mode) {
            for (var key in this._search_need_update) {
                if (this._search_need_update.hasOwnProperty(key)) {
                    if (key != mode) {
                        this._search_need_update[key] = true;
                    }
                }
            }
            if (mode == 'favorites') {
                this._getFavorites();
            }
        },
        _openFavorites: function (filter) {
            console.log('open favorites');
            $('.search-row').hide();
            this.showResult();
            var mode = 'favorites';
            Common.CurrentSearchMode = mode;
            this._getFavorites(filter);
            this.parent.repositionMap(mode);
        },
        _getFavorites: function (filter) {
            var mode = Common.CurrentSearchMode;
            favoritesCollection.search(filter);
            this._search_query[mode] = '';
            this._search_filter[mode] = filter ? filter : '';
            Common.Dispatcher.trigger('sidebar:show_loading', mode);
            this._search_need_update[mode] = false;
        },
        occupationClicked: function (id, pathway) {
            Common.Router.inOccupation = true;
            var new_url = this.getSearchRoute();
            new_url.push(id);
            if (pathway) {
                new_url.push(pathway);
            }
            Backbone.history.navigate(new_url.join("/"), false);
        },
        updateSearchBarInput: function (query) {
            // Remove all filters from searchbar
            // filters are fos, qt, nqf, sos, mc
            query = query.replace(query.match(/&fos=\d+/g), '');
            query = query.replace(query.match(/&qt=\d+/g), '');
            query = query.replace(query.match(/&nqf=\d+/g), '');
            query = query.replace(query.match(/&sos=\d+/g), '');
            query = query.replace(query.match(/&mc=\d+/g), '');
            query = query.replace(query.match(/&pi=\d+/g), '');
            this.$search_bar_input.val(query);
        },
        search: function (mode, query, filter) {

            this.changeFilterPanel(Common.CurrentSearchMode);

            console.log(mode);

            if (query && mode != 'favorites') {

                // Put query to search input
                this.updateSearchBarInput(query);

                // Update filters
                if(mode != 'occupation') {
                    this.parseFilters(query);
                    this.updateFilters(mode);
                }

                if(!this.$search_bar_input.val()) {
                    return;
                }

                switch (mode) {
                    case 'provider':
                        campusCollection.search(query, filter);
                        break;
                    case 'course':
                        courseCollection.search(query, filter);
                        break;
                    case 'occupation':
                        occupationCollection.search(query);
                        break;
                    default:
                        return;
                }
                this._search_query[mode] = query;
                this._search_filter[mode] = filter;
                this._search_need_update[mode] = false;
                Common.Dispatcher.trigger('sidebar:show_loading', mode);
                this.showResult(mode);
            } else if (mode == 'favorites') {
                if (query) {
                    filter = query;
                }
                this._openFavorites(query);
            }
            // redraw filter
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
            if (mode == 'occupation' || mode == 'favorites') {
                this.hideFilterPanel();
                $('.filter-button').hide();
            } else {
                $('.filter-button').show();
            }
        },
        onFinishedSearch: function (is_not_empty, mode, num) {

            Common.Dispatcher.trigger('sidebar:hide_loading', mode);
            Common.Dispatcher.trigger('map:repositionMap', mode);

            $('#result-title').find('[id*="result-title-"]').hide();
            $('#result-title').find('#result-title-' + Common.CurrentSearchMode).show();
            if (mode) {
                this._search_results[mode] = num;
                this.$search_clear.show();
            }

            this.hideFilterPanel();
            if (num > 0 && mode != 'occupation') {
                // Show share bar
                Common.Dispatcher.trigger('map:showShareBar');
            } else {
                Common.Dispatcher.trigger('map:hideShareBar');
            }

            if (Common.Router.selected_occupation) {
                Common.Dispatcher.trigger('occupation-' + Common.Router.selected_occupation + ':routed');
            }
        },
        showResult: function (mode) {
            if (!Common.EmbedVersion) {
                if (this.map_in_fullscreen) {
                    var $toggle = $('#result-toogle');
                    this.parent.openResultContainer($toggle);
                }
            }
        },
        toogleResult: function (event) {
            if ($(event.target).hasClass('fa-caret-left') ||
                $(event.target.parentElement).hasClass('fa-caret-left') ||
                $(event.target).find('.fa-caret-left').length > 0) {

                this.parent.openResultContainer($(event.target));
            } else {
                this.parent.closeResultContainer($(event.target));
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
        clearAllDraw: function () {
            this.parent.clearAllDrawnLayer();
            this.updateSearchRoute();
        },
        changeCategoryButton: function (mode) {
            // Shows relevant search result container
            this.parent.showResultContainer(mode);

            this.$el.find('.search-category').find('.search-option').removeClass('active');
            var $button = null;
            var highlight = "";
            if (mode == "provider") {
                $button = this.$provider_button;
                highlight = 'Search for provider';
            } else if (mode == "course") {
                $button = this.$course_button;
                highlight = 'Search for courses';
            } else if (mode == "occupation") {
                $button = this.$occupation_button;
                highlight = 'Search for occupation';
            } else if (mode == "favorites") {
                $button = this.$favorites_button;
                highlight = '';
            }

            // change placeholder of input
            this.$search_bar_input.attr("placeholder", highlight);
            this.showSearchBar(0);
            if ($button) {
                $button.addClass('active');
            }
        },
        mapResize: function (is_resizing) {
            this.map_in_fullscreen = is_resizing;
            if (is_resizing) { // To fullscreen
                this.$('#back-home').show();
                this.$('#result-toogle').show();
                this.parent.closeResultContainer($('#result-toogle'));
                var mode = Common.CurrentSearchMode;
                if(mode in this._search_results) {
                    if(this._search_results[mode] > 0)
                        this.parent.openResultContainer($('#result-toogle'));
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
        _addResponsiveTab: function (div) {
            div.addClass('responsive-tabs');

            div.on('click', 'li.active > a, span.glyphicon', function () {
                div.toggleClass('open');
            }.bind(div));

            div.on('click', 'li:not(.active) > a', function () {
                div.removeClass('open');
            }.bind(div));
        },
        clearSearch: function (e) {
            e.preventDefault();

            // Clear search input
            this.$search_bar_input.val('');

            // Clear saved query
            this._search_query[Common.CurrentSearchMode] = '';

            // Clear saved marker
            this.parent.clearLayerMode(Common.CurrentSearchMode);

            // Hide clear button
            this.$search_clear.hide();

            // Update search
            this.updateSearchRoute();

            // Update sidebar
            Common.Dispatcher.trigger('sidebar:clear_search', Common.CurrentSearchMode);

            if(Common.CurrentSearchMode !== 'favorites')
                this.parent.zoomToDefault();
        },
        /*--------------------*/
        /* Advanced filter    */
        /*--------------------*/
        isFilterPanelOpened : false,
        fosFilter: 0,
        qtFilter: 0,
        filtered: {
            'course': false,
            'provider': false
        },
        filtersInMode: {
            'course': {
                'field-of-study-select': null,
                'qualification-type-select': null,
                'nqf-level-select': null,
                'subfield-of-study-select': null,
                'minimum-credits': 0
            },
            'provider': {
                'public-institution-select': null,
                'field-of-study-provider-select': null
            }
        },
        minimumCreditsSlider: null,
        showFilterPanel: function (e) {
            this.isFilterPanelOpened = true;
            $('#show-filter-button').hide();
            $('#hide-filter-button').show();

            // Hide side panel
            var resultToggle = $('#result-toogle');
            this.parent.closeResultContainer(resultToggle);
            resultToggle.removeClass('fa-caret-right');
            resultToggle.addClass('fa-caret-left');

            var $filterPanel = $('.filter-panel');

            if ($filterPanel.css('display') == 'none'){
                $filterPanel.animate({
                    height: "toggle"
                }, 500)
            }
        },
        filterChanged: function (e) {
            // Filter dropdown selected
            var id =  $('#'+e.target.id+ ' option:selected').val();
            var mode = Common.CurrentSearchMode;
            if(id != '-') {
                this.filtersInMode[mode][e.target.id] = id;
            } else {
                this.filtersInMode[mode][e.target.id] = null;
            }
        },
        hideFilterPanel: function (e) {
            $('#hide-filter-button').hide();
            $('#show-filter-button').show();

            // Show side panel
            var resultToggle = $('#result-toogle');
            if(typeof e != 'undefined' && typeof this._search_query[Common.CurrentSearchMode] != 'undefined') {
                this.parent.openResultContainer(resultToggle);
                resultToggle.removeClass('fa-caret-left');
                resultToggle.addClass('fa-caret-right');
            }

            var $filterPanel = $('.filter-panel');

            if(this.isFilterPanelOpened) {
                if ($filterPanel.css('display') != 'none'){
                    $filterPanel.animate({
                        height: "toggle"
                    }, 500)
                }
                this.isFilterPanelOpened = false;
            }

        },
        getAdvancedFilters: function () {
            // Return selected advanced filter for selected mode
            var filter = '';
            var mode = Common.CurrentSearchMode;
            var courseMode = 'course';
            var providerMode = 'provider';
            if(mode == courseMode) {
                if(this.filtersInMode[courseMode]['field-of-study-select']) {
                    filter += '&fos=' + this.filtersInMode[courseMode]['field-of-study-select'];
                }
                if(this.filtersInMode[courseMode]['qualification-type-select']) {
                    filter += '&qt=' + this.filtersInMode[courseMode]['qualification-type-select'];
                }
                if(this.filtersInMode[courseMode]['nqf-level-select']) {
                    filter += '&nqf=' + this.filtersInMode[courseMode]['nqf-level-select'];
                }
                if(this.filtersInMode[courseMode]['subfield-of-study-select']) {
                    filter += '&sos=' + this.filtersInMode[courseMode]['subfield-of-study-select'];
                }
                if(this.minimumCreditsSlider) {
                    var mcValue = this.minimumCreditsSlider.bootstrapSlider('getValue');
                    if(mcValue > 0) {
                        filter += '&mc=' + mcValue;
                    }
                }
                this.filtered[courseMode] = filter != '';
            } else if(mode == providerMode) {
                if(this.filtersInMode[providerMode]['public-institution-select']) {
                    filter += '&pi=' + this.filtersInMode[providerMode]['public-institution-select'];
                }
                if(this.filtersInMode[providerMode]['field-of-study-provider-select']) {
                    filter += '&fos=' + this.filtersInMode[providerMode]['field-of-study-provider-select'];
                }
                this.filtered[providerMode] = filter != '';
            }
            return filter;
        },
        parseFilters: function (query) {
            // Parse advance filter from URL
            var mode = Common.CurrentSearchMode;
            var courseMode = 'course';
            var providerMode = 'provider';

            var fosId = query.match(/&fos=\d+/g);
            var qtId = query.match(/&qt=\d+/g);
            var nqfId = query.match(/&nqf=\d+/g);
            var sosId = query.match(/&sos=\d+/g);
            var mcValue = query.match(/&mc=\d+/g);
            var piValue = query.match(/&pi=\d+/g);

            if(fosId) {
                fosId = fosId[0].split('=')[1];
                this.filtered[mode] = true;
                if(mode == courseMode)
                    this.filtersInMode[mode]['field-of-study-select'] = fosId;
                else if(mode == providerMode)
                    this.filtersInMode[mode]['field-of-study-provider-select'] = fosId;
            }
            if(qtId) {
                qtId = qtId[0].split('=')[1];
                this.filtered[courseMode] = true;
                this.filtersInMode[courseMode]['qualification-type-select'] = qtId;
            }
            if(nqfId) {
                nqfId = nqfId[0].split('=')[1];
                this.filtered[courseMode] = true;
                this.filtersInMode[courseMode]['nqf-level-select'] = nqfId;
            }
            if(sosId) {
                sosId = sosId[0].split('=')[1];
                this.filtered[courseMode] = true;
                this.filtersInMode[courseMode]['subfield-of-study-select'] = sosId;
            }
            if(piValue) {
                piValue = piValue[0].split('=')[1];
                this.filtered[providerMode] = true;
                this.filtersInMode[providerMode]['public-institution-select'] = piValue;
            }
            if(mcValue) {
                mcValue = mcValue[0].split('=')[1];
                this.filtered[courseMode] = true;
                this.filtersInMode[courseMode]['minimum-credits'] = mcValue;
                this.minimumCreditsSlider.bootstrapSlider('setValue', mcValue);
            }
        },
        updateFilters: function (mode) {
            // Update selected filters

            var courseMode = 'course';
            var providerMode = 'provider';

            if(this.filtersInMode[courseMode]['field-of-study-select']==null) {
                $('#field-of-study-select').val('-');
            } else {
                this.filtered[courseMode] = true;
                $('#field-of-study-select').val(this.filtersInMode[courseMode]['field-of-study-select']);
            }

            if(this.filtersInMode[courseMode]['qualification-type-select']==null) {
                $('#qualification-type-select').val('-');
            } else {
                this.filtered[courseMode] = true;
                $('#qualification-type-select').val(this.filtersInMode[courseMode]['qualification-type-select']);
            }

            if(this.filtersInMode[courseMode]['nqf-level-select']==null) {
                $('#nqf-level-select').val('-');
            } else {
                this.filtered[courseMode] = true;
                $('#nqf-level-select').val(this.filtersInMode[courseMode]['nqf-level-select']);
            }

            if(this.filtersInMode[courseMode]['subfield-of-study-select']==null) {
                $('#subfield-of-study-select').val('-');
            } else {
                this.filtered[courseMode] = true;
                $('#subfield-of-study-select').val(this.filtersInMode[courseMode]['subfield-of-study-select']);
            }

            if(this.filtersInMode[courseMode]['minimum-credits']>0) {
                this.filtered[courseMode] = true;
            }
            this.minimumCreditsSlider.bootstrapSlider('setValue', this.filtersInMode[courseMode]['minimum-credits']);

            if(this.filtersInMode[providerMode]['public-institution-select']==null) {
                $('#public-institution-select').val('-');
            } else {
                this.filtered[providerMode] = true;
                $('#public-institution-select').val(this.filtersInMode[providerMode]['public-institution-select']);
            }

            if(this.filtersInMode[providerMode]['field-of-study-provider-select']==null) {
                $('#field-of-study-provider-select').val('-');
            } else {
                this.filtered[providerMode] = true;
                $('#field-of-study-provider-select').val(this.filtersInMode[providerMode]['field-of-study-provider-select']);
            }

            $('#field-of-study-select').trigger("chosen:updated");
            $('#qualification-type-select').trigger("chosen:updated");
            $('#nqf-level-select').trigger("chosen:updated");
            $('#subfield-of-study-select').trigger("chosen:updated");
            $('#public-institution-select').trigger("chosen:updated");
            $('#field-of-study-provider-select').trigger("chosen:updated");


        },
        clearFilters: function (event, dontUpdateRoute) {
            var mode = Common.CurrentSearchMode;
            var courseMode = 'course';
            var providerMode = 'provider';
            this.filtered[mode] = false;

            $('#field-of-study-select').val('-');
            $('#field-of-study-select').trigger("chosen:updated");

            $('#qualification-type-select').val('-');
            $('#qualification-type-select').trigger("chosen:updated");

            $('#nqf-level-select').val('-');
            $('#nqf-level-select').trigger("chosen:updated");

            $('#subfield-of-study-select').val('-');
            $('#subfield-of-study-select').trigger("chosen:updated");

            $('#field-of-study-provider-select').val('-');
            $('#field-of-study-provider-select').trigger("chosen:updated");

            $('#public-institution-select').val('-');
            $('#public-institution-select').trigger("chosen:updated");

            this.minimumCreditsSlider.bootstrapSlider('setValue', 0);

            if(mode==courseMode){
                this.filtersInMode[mode] = {
                    'field-of-study-select': null,
                    'qualification-type-select': null,
                    'nqf-level-select': null,
                    'subfield-of-study-select': null,
                    'minimum-credits': 0
                }
            } else if(mode==providerMode) {
                this.filtersInMode[mode] = {
                    'public-institution-select': null,
                    'field-of-study-provider-select': null
                }
            }

            this.isSearchFromInput = true;
            if(typeof dontUpdateRoute === 'undefined') {
                this.updateSearchRoute();
            }
        },
        changeFilterPanel: function (mode) {
            this.$filter_panel_button.show();

            if(mode == 'course') {
                this.$filter_panel_campus.hide();
                this.$filter_panel_course.show();
            } else if(mode == 'provider') {
                this.$filter_panel_campus.show();
                this.$filter_panel_course.hide();
            } else {
                this.$filter_panel_campus.hide();
                this.$filter_panel_course.hide();
                this.$filter_panel_button.hide();
            }

        },
        loadFilters: function () {
            var that = this;
            var courseMode = 'course';
            var providerMode = 'provider';
            this.minimumCreditsSlider = $('#minimum-credits').bootstrapSlider({
	            formatter: function(value) {
                    that.filtersInMode[courseMode]['minimum-credits'] = value;
		            return value;
	            }
            });

            $('#public-institution-select').chosen({
                no_results_text: "Oops, nothing found!",
                width: "80%"
            });

            // Get field of study
            $.ajax({
                url: 'api/field_of_study',
                type: 'GET',
                success: function (response) {
                    $.each(response, function (i, item) {
                        $('#field-of-study-select').append($('<option>', {
                            value: item.id,
                            text : item.field_of_study_description,
                            selected: item.id == that.filtersInMode[courseMode]['field-of-study-select']
                        }));
                        $('#field-of-study-provider-select').append($('<option>', {
                            value: item.id,
                            text : item.field_of_study_description,
                            selected: item.id == that.filtersInMode[providerMode]['field-of-study-provider-select']
                        }));
                    });

                    $('#field-of-study-select').chosen({
                        no_results_text: "Oops, nothing found!",
                        width: "80%"
                    });
                    $('#field-of-study-provider-select').chosen({
                        no_results_text: "Oops, nothing found!",
                        width: "80%"
                    });

                    //update filter data if started from url
                    Common.Dispatcher.trigger('sidebar:update_filter_data',that.filtersInMode);
                }
            });
            $.ajax({
                url: 'api/qualification_type',
                type: 'GET',
                success: function (response) {
                    $.each(response, function (i, item) {
                        $('#qualification-type-select').append($('<option>', {
                            value: item.id,
                            text : item.type,
                            selected: item.id == that.filtersInMode[courseMode]['qualification-type-select']
                        }));
                    });
                    $('#qualification-type-select').chosen({
                        no_results_text: "Oops, nothing found!",
                        width: "80%"
                    });
                    //update filter data
                    Common.Dispatcher.trigger('sidebar:update_filter_data',that.filtersInMode);
                }
            });
            $.ajax({
                url: 'api/national_qualifications_framework',
                type: 'GET',
                success: function (response) {
                    $.each(response, function (i, item) {
                        $('#nqf-level-select').append($('<option>', {
                            value: item.id,
                            text : item.text,
                            selected: item.id == that.filtersInMode[courseMode]['nqf-level-select']
                        }));
                    });
                    $('#nqf-level-select').chosen({
                        no_results_text: "Oops, nothing found!",
                        width: "80%"
                    });
                    //update filter data
                    Common.Dispatcher.trigger('sidebar:update_filter_data',that.filtersInMode);
                }
            });
            $.ajax({
                url: 'api/subfield_of_study',
                type: 'GET',
                success: function (response) {
                    $.each(response, function (i, item) {
                        $('#subfield-of-study-select').append($('<option>', {
                            value: item.id,
                            text : item.learning_subfield,
                            selected: item.id == that.filtersInMode[courseMode]['subfield-of-study-select']
                        }));
                    });
                    $('#subfield-of-study-select').chosen({
                        no_results_text: "Oops, nothing found!",
                        width: "50%"
                    });
                    //update filter data
                    Common.Dispatcher.trigger('sidebar:update_filter_data',that.filtersInMode);
                }
            });
        }
    });

    return SearchBarView;
});