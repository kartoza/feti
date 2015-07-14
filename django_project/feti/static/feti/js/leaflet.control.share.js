/**
 * Created by lucernae on 04/06/15.
 */

/** Share control logic **/
L.Control.Share = L.Control.extend({
    options: {
        position: 'topright'
    },
    initialize: function(options){
        L.Util.setOptions(this, options);
    },
    onAdd: function(map){
        var container = L.DomUtil.create('div', 'share-container info');
        container.innerHTML = $("#share-control").html();

        $("#share-control-button", container).on('click', this.shareButtonClick);
        $("#share-control-popup-close-button", container).on('click', this.closePopupClick);
        $("#share-control-pdf-button", container).on('click', this.downloadPDF);

        // set clipboard handler
        var client = new ZeroClipboard($("#share-link-copy-button", container));
        client.on("ready", function(readyEvent){

            this.on("copy", function(e){
                var clipboard = e.clipboardData;
                var url = $("#share-link-url").val();
                clipboard.setData("text/plain", url);
            });

            this.on("aftercopy", function(e){
                if(e.success["text/plain"]){
                    alert("Url copied to clipboard.");
                }
                else{
                    alert("Can't copy url automatically  to clipboard.")
                }
            });
        });

        client.on("error", function(e){
            $("#share-link-copy-button", container).css("display", "none");
            ZeroClipboard.destroy();
        });
        this.container = container;
        this.clipboardClient = client;

        // disable drag in the div
        $(container).on('mouseover', function(){
            map.dragging.disable();
            map.doubleClickZoom.disable();
        });
        $(container).on('mouseout', function(){
            map.dragging.enable();
            map.doubleClickZoom.enable();
        });
        return container;
    },
    onRemove: function(map){
        $(this.container).remove();
    },
    shareButtonClick: function(e){
        $("#share-control-button").css('display', 'none');
        $("#share-control-action").css('display', 'block');
        var url = window.location.href;
        $("#share-link-url").val(url);
    },
    closePopupClick: function(e){
        $("#share-control-button").css('display', 'block');
        $("#share-control-action").css('display', 'none');
    },
    downloadPDF: function(e){
        leafletImage(map, function(error, canvas) {
            var img = canvas.toDataURL();
            var doc = new jsPDF();
            var map = $('#map');
            var height = map.height();
            var width = map.width();
            height = 180*height/width;
            width = 180;
            doc.fromHTML(
                $('#navbar-header').get(0),
                0,
                0,
                {
                 'width': 180 // max width of content on PDF
                }
                );
            doc.setFontSize(24);

            doc.text(35, 25, "FETI");
            doc.addImage(img, 'JPEG', 15, 40, width, height);
            doc.save('Further Education and Training Institute.pdf');
        });
    }
});

L.control.share = function(id, options){
    return new L.Control.Share(id, options);
}