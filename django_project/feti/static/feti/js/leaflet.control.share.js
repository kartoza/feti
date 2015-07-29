/**
 * Created by lucernae on 04/06/15.
 */

/** Share control logic **/

function generate_pdf(show_courses){

    leafletImage(map, function(error, canvas) {
        function add_height(doc, height, additional_height){
            height += additional_height;
            if (height > 180 * 3 / 2){
                doc.addPage();
                return 15;
            }
            return height;
        }

        var img = canvas.toDataURL();

        var doc = new jsPDF();
        var doc_width = 190;
        var doc_cumulative = 10;

        doc.setDrawColor(19, 70, 167);
        doc.setFillColor(19, 70, 167);
        doc.rect(10, doc_cumulative, doc_width, 25, 'F');
        doc_cumulative = add_height(doc, doc_cumulative, 25 + 5);

        doc.setFontSize(24);
        doc.setTextColor(255, 255, 255);
        doc.text(30, 25, "Further Education and Training Institute");

        var map = $('#map');
        var height = map.height();
        var width = map.width();
        height = doc_width * height / width;
        width = doc_width;

        doc.addImage(img, 'JPEG', 10, doc_cumulative, width, height);
        doc_cumulative = add_height(doc, doc_cumulative, height + 5);

        doc.setDrawColor(19, 70, 167);
        doc.setFillColor(19, 70, 167);
        doc.rect(10, doc_cumulative, doc_width, 25, 'F');
        doc_cumulative = add_height(doc, doc_cumulative, 25 + 5);

        doc_cumulative = add_height(doc, doc_cumulative, 10);
        $('#side_panel').children(":first").children(":first").children().each(function(count, campus){
            doc.setDrawColor(19, 70, 167);
            doc.setFillColor(19, 70, 167);
            doc.rect(10, doc_cumulative - 8, doc_width, 14, 'F');
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(14);
            doc.text(15, doc_cumulative, $(campus).find(".panel-title").text().trim());
            doc_cumulative = add_height(doc, doc_cumulative, 15);
            if (show_courses){
                $(campus).find(".course-list-item").each(function(count2, course){
                    doc.setFontSize(8);
                    doc.setTextColor(0,0,0);
                    doc.text(15, doc_cumulative, $(course).children(":first").text().trim());
                    doc_cumulative = add_height(doc, doc_cumulative, 8);
                });
                doc_cumulative = add_height(doc, doc_cumulative, 10);
            }
        });

        doc.save('Further Education and Training Institute.pdf');
    });
}


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
        $("#share-control-full-pdf-button", container).on('click', this.downloadFullPDF);

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
        generate_pdf(false);
    },
    downloadFullPDF: function(e){
        generate_pdf(false);
    }
});

L.control.share = function(id, options){
    return new L.Control.Share(id, options);
}