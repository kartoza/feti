define(['jquery', 'underscore', 'scripts/views/map', 'scripts/views/layer-administrative'], function(
    $, _, MapView, LayerAdministrativeView) {

    describe('just checking', function() {

        beforeEach(function () {
            this.mapView = new MapView();
            this.mapView.render();
            this.layerAdministrativeView = new LayerAdministrativeView({parent: this.mapView});
        });

        it('works for app', function() {
            var el = $('<input type="text">');

            el.val('require.js up and running');
            expect(el.val()).toEqual('require.js up and running');
        });

        it('works for underscore', function() {
            // just checking that _ works
            expect(_.size([1,2,3])).toEqual(3);
        });

    });

});