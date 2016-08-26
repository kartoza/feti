define([
    'text!static/feti/js/scripts/templates/searchbar.html',
    'common',
    '/static/feti/js/scripts/collections/search.js'
], function (searchbarTemplate, Common, searchCollection) {
    var SearchBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#map-search',
        template: _.template(searchbarTemplate),
        events: {
            'click #where-to-study': 'categoryClicked',
            'click #what-to-study': 'categoryClicked',
            'click #choose-occupation': 'categoryClicked',
            'click #back-home': 'backHomeClicked',
            'click #result-toogle': 'resultToogling'
        },
        initialize: function () {
            this.render();
            this.$search_bar = $(".search-bar");
            this.$search_bar_input = $("#search-bar-input");
            this.$provider_button = $("#where-to-study");
            this.$course_button = $("#what-to-study");
            this.$occupation_button = $("#choose-occupation");
            this.search_bar_hidden = true;
            Common.Dispatcher.on('result:show', this.showResult(), this);
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template());
            $(this.container).append(this.$el);
            // form submit
            var that = this;
            $("#search-form").submit(function (e) {
                var mode = that.categorySelected();
                if (mode == 'provider') {
                    searchCollection.getProvider(that.$search_bar_input.val());
                }
                e.preventDefault(); // avoid to execute the actual submit of the form.
            });
        },
        categoryClicked: function (event) {
            this.changeCategory($(event.target).data("mode"));
            this.trigger('categoryClicked', event);
        },
        backHomeClicked: function (e) {
            this.toggleProvider(e);
            this.trigger('backHome', e);
        },
        showResult: function () {
            var $toogle = $('#result-toogle');
            if ($toogle.hasClass('fa-caret-left')) {
                $toogle.removeClass('fa-caret-left');
                $toogle.addClass('fa-caret-right');
                if (!$('#providers').is(":visible")) {
                    $('#providers').show("slide", {direction: "right"}, 500);
                }
            }
        },
        resultToogling: function (event) {
            if ($(event.target).hasClass('fa-caret-left')) {
                $(event.target).removeClass('fa-caret-left');
                $(event.target).addClass('fa-caret-right');
                if (!$('#providers').is(":visible")) {
                    $('#providers').show("slide", {direction: "right"}, 500);
                }
            } else {
                $(event.target).removeClass('fa-caret-right');
                $(event.target).addClass('fa-caret-left');
                if ($('#providers').is(":visible")) {
                    $('#providers').hide("slide", {direction: "right"}, 500);
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
                this.showSearchBar();
            }
        },
        changeCategory: function (mode) {
            Backbone.history.navigate('map/' + mode, true);
        },
        mapResize: function (is_resizing, speed) {
            if (is_resizing) { // To fullscreen
                this.$('#back-home').show();
                this.showSearchBar(speed);
            } else { // Exit fullscreen
                this.$('#back-home').hide();
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
                var $result = $('#providers');
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
        toggleProvider: function (e) {
            var that = this;
            this.changeCategoryButton("");
            if ($('#providers').is(":visible")) {
                $('#carousel-toogle').removeClass('fa-caret-right');
                $('#carousel-toogle').addClass('fa-caret-left');
                $('#providers').hide("slide", {direction: "right"}, 500, function () {
                    that.hideSearchBar(e);
                });
            } else {
                that.hideSearchBar(e);
            }
        }
    });

    return SearchBarView;
});