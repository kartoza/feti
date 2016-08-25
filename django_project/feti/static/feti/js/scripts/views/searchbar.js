define([
    'text!static/feti/js/scripts/templates/searchbar.html',
    'common'
], function(searchbarTemplate, Common){
    var SearchBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#map-search',
        template: _.template(searchbarTemplate),
        events: {
            'click #where-to-study': 'categoryClicked',
            'click #what-to-study': 'categoryClicked',
            'click #choose-occupation': 'categoryClicked',
            'click #back-home': 'exitFullScreen',
            'click #carousel-toogle': 'carouselToogling'
        },
        categoryClicked: function (event) {
            Common.Router.navigate('map/fullscreen', true);
            this.changeCategory(event.target);
        },
        exitFullScreen: function (e) {
            this.toogleProviderWithMap(e);
        },
        carouselToogling: function (event) {
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
        initialize: function () {
            this.render();
            Common.Dispatcher.on('map:resize', this.mapResize, this);
            this.$search_bar = $(".search-bar");
            this.search_bar_hidden = true;
        },
        render: function () {
            this.$el.empty();
            this.$el.html(this.template());
            $(this.container).append(this.$el);
        },
        categorySelected: function () {
            var button = this.$el.find('.search-category').find('.m-button.active');
            if (button[0]) {
                return $(button[0]).html();
            } else {
                return null;
            }
        },
        changeCategory: function (button) {
            this.$el.find('.search-category').find('.m-button').removeClass('active');
            $(button).addClass('active');
            //if (mapView.isFullScreen) {
            //    this.showSearchBar();
            //}
        },
        mapResize: function (is_resizing) {
            if (is_resizing) {
                this.$('#back-home').show();
                this.showSearchBar();
            } else {
                this.$('#back-home').hide();

            }
        },
        showSearchBar: function () {
            if (this.search_bar_hidden && this.categorySelected()) {
                this.$search_bar.slideToggle(500);
                // zoom control animation
                var $zoom_control = $('.leaflet-control-zoom');
                $zoom_control.animate({
                    marginTop: '+=55px'
                }, 500);
                var $result = $('#providers');
                $result.animate({
                    paddingTop: '+=55px'
                }, 500);

                // now it is shown
                this.search_bar_hidden = false;
            }
        },
        hideSearchBarWithMap: function (e) {
            if (!this.search_bar_hidden) {
                this.$search_bar.slideToggle(500, function () {
                    // mapView.exitFullScreen(e);
                });
                // zoom control animation
                var $zoom_control = $('.leaflet-control-zoom');
                $zoom_control.animate({
                    marginTop: '-=55px'
                }, 500);

                // now it is shown
                this.search_bar_hidden = true;
            } else {
                // mapView.exitFullScreen(e);
            }
        },
        toogleProviderWithMap: function (e) {
            var that = this;
            if ($('#providers').is(":visible")) {
                $('#carousel-toogle').removeClass('fa-caret-right');
                $('#carousel-toogle').addClass('fa-caret-left');
                $('#providers').hide("slide", {direction: "right"}, 500, function () {
                    that.hideSearchBarWithMap(e);
                });
            } else {
                that.hideSearchBarWithMap(e);
            }
        }
    });

    return SearchBarView;
});