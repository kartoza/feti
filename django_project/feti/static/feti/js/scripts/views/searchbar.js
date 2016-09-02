define([
    'text!static/feti/js/scripts/templates/searchbar.html',
    'common',
    '/static/feti/js/scripts/collections/search.js'
], function (searchbarTemplate, Common, searchCollection) {
    var SearchBarView = Backbone.View.extend({
        minimumWords: 3,
        tagName: 'div',
        container: '#map-search',
        template: _.template(searchbarTemplate),
        events: {
            'click #where-to-study': 'categoryClicked',
            'click #what-to-study': 'categoryClicked',
            'click #choose-occupation': 'categoryClicked',
            'click #back-home': 'backHomeClicked',
            'click #result-toogle': 'toogleResult'
        },
        initialize: function () {
            this.render();
            $("#result-toogle").hide();
            this.$search_bar = $(".search-bar");
            this.$search_bar_input = $("#search-bar-input");
            this.$provider_button = $("#where-to-study");
            this.$course_button = $("#what-to-study");
            this.$occupation_button = $("#choose-occupation");
            this.$result_loading = $("#result-loading");
            this.$result_empty = $("#result-empty");
            this.search_bar_hidden = true;
            Common.Dispatcher.on('search:finish', this.searchingFinish, this);
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template());
            $(this.container).append(this.$el);
            // form submit
            var that = this;
            $("#search-form").submit(function (e) {
                that.search();
                e.preventDefault(); // avoid to execute the actual submit of the form.
            });
        },
        categoryClicked: function (event) {
            this.changeRoute($(event.target).data("mode"));
            this.search();
            this.trigger('categoryClicked', event);
        },
        backHomeClicked: function (e) {
            this.toggleProvider(e);
            this.trigger('backHome', e);
        },
        search: function () {
            this.changeRoute();
            var mode = this.categorySelected();
            if (mode) {
                var query = this.$search_bar_input.val();
                if (query.length >= this.minimumWords) {
                    searchCollection.search(mode, this.$search_bar_input.val());
                    this.in_show_result = true;
                    this.$result_loading.show();
                    this.$result_empty.hide();
                    this.showResult();
                }
            }
        },
        searchingFinish: function (is_not_empty) {
            this.$result_loading.hide();
            if (!is_not_empty) {
                this.$result_empty.show();
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
                    $('#result').show("slide", {direction: "right"}, 500);
                }
            } else {
                $(event.target).removeClass('fa-caret-right');
                $(event.target).addClass('fa-caret-left');
                if ($('#result').is(":visible")) {
                    $('#result').hide("slide", {direction: "right"}, 500);
                }
            }
        },
        categorySelected: function () {
            var button = this.$el.find('.search-category').find('.m-button.active');
            if (button[0]) {
                return $(button[0]).attr("data-mode");
            } else {
                return "";
            }
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
                // set focus on search text
                document.search_form.search_input.focus();
            }
        },
        changeRoute: function (mode) {
            if (mode) {
                Backbone.history.navigate('map/' + mode, true);
            } else {
                Backbone.history.navigate('map/' + this.categorySelected(), true);
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
        toggleProvider: function () {
            if ($('#result').is(":visible")) {
                $('#result-toogle').removeClass('fa-caret-right');
                $('#result-toogle').addClass('fa-caret-left');
                $('#result').hide("slide", {direction: "right"}, 500, function () {
                    Common.Dispatcher.trigger('map:exitFullScreen');
                });
            } else {
                Common.Dispatcher.trigger('map:exitFullScreen');
            }
        }
    });

    return SearchBarView;
});