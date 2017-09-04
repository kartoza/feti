define(['common', 'scripts/views/search', 'scripts/views/map'], function(
    Common, MapView, SearchView) {

    describe("View :: Search", function () {

        beforeEach(function () {
            this.mapView = new MapView();
            this.mapView.render();
            this.common = Common;
            this.searchView = new SearchView({parent: that.mapView});
        });

        afterEach(function () {
            this.searchView.remove();
            this.common.Router.navigate('', true);
        });

        describe('Category tab', function () {
            it('should be changed', function () {
                var oldMode = this.common.CurrentSearchMode;
                this.searchView.$el.find('#what-to-study').click();
                var newMode = this.common.CurrentSearchMode;
                expect(oldMode).toEqual('provider');
                expect(newMode).toEqual('course');
            });

        });

        describe('Search bar', function () {
            it('should be cleared', function () {
                var $clearSearchButton = this.searchView.$search_clear;
                var $searchBarInput = this.searchView.$search_bar_input;

                $searchBarInput.val('something');

                expect($searchBarInput.val()).toEqual('something');

                $clearSearchButton.click();
                expect($searchBarInput.val()).toEqual('');
            });

        });
    });
});
