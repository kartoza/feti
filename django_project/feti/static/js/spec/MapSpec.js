describe("View :: Map", function () {

    beforeEach(function () {
        var flag = false;
        var that = this;

        require(['scripts/views/map'], function (MapView) {
            that.mapView = new MapView();
            that.mapView.render();
        });
    });
    
    afterEach(function () {
        this.mapView.remove();
    });

    describe('Shows and Hides', function () {

        it('should be hidden', function () {
            expect(this.mapView.$el.is(':visible')).toEqual(false);
        });

    });
});
