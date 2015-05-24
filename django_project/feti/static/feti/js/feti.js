/**
 * Created by christian@    kartoza on 03/15.
 */
/*global $, jQuery, L, window, console*/
var map;
var campus_lookup = [];
var campus_cluster_group;
var campus_marker = [];
var highlighted_feature;

jQuery.download = function (url, data, method) {
    /* Taken from http://www.filamentgroup.com/lab/jquery-plugin-for-requesting-ajax-like-file-downloads.html*/
    'use strict';
    //url and data options required
    if (url && data) {
        //data can be string of parameters or array/object
        data = typeof data === 'string' ? data : jQuery.param(data);
        //split params into form inputs
        var inputs = '';
        jQuery.each(data.split('&'), function () {
            var pair = this.split('=');
            inputs += '<input type="hidden" name="' + pair[0] + '" value="' + pair[1] + '" />';
        });
        //send request
        jQuery('<form action="' + url + '" method="' + (method || 'post') + '">' + inputs + '</form>')
            .appendTo('body').submit().remove();
    }
};

function toggle_side_panel() {
    'use strict';
    var map_div = $('#map'),
        side_panel = $('#side_panel'),
        show_hide_div = $('#show_hide');
    /* hide */
    if (side_panel.is(":visible")) {
        show_hide_div.removeClass('glyphicon-chevron-right');
        show_hide_div.addClass('glyphicon-chevron-left');
        side_panel.removeClass('col-lg-4');
        side_panel.hide();
        map_div.removeClass('col-lg-8');
        map_div.addClass('col-lg-12');
        map.invalidateSize();
    } else { /* show */
        show_hide_div.addClass('glyphicon-chevron-right');
        show_hide_div.removeClass('glyphicon-chevron-left');
        side_panel.addClass('col-lg-4');
        side_panel.show();
        map_div.removeClass('col-lg-12');
        map_div.addClass('col-lg-8');
        map.invalidateSize();
    }
}

function show_map() {
    'use strict';
    $('#navigationbar').css('height', window.innerHeight * 0.1);
    $('#map').css('height', window.innerHeight * 0.9);
    map = L.map('map').setView([-25.7461, 28.1881], 8);
    //map = L.map('map').setView([-33.9200, 18.8600], 8);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // create cluster layer
    campus_cluster_group = L.markerClusterGroup().addTo(map);

}

/*jslint unparam: true*/
function style(feature) {
    'use strict';
    return {
        weight: 2,
        opacity: 1,
        color: 'blue',
        dashArray: '',
        fillOpacity: 0.5,
        fillColor: 'blue'
    };
}
/*jslint unparam: false*/

function highlightFeature(e) {
    'use strict';
    var marker = e.target;
    marker.setStyle({
        weight: 5,
        color: 'white',
        dashArray: '',
        fillOpacity: 0.3,
        fillColor: 'blue'
    });
}

function resetHighlight(e) {
    'use strict';
    var marker = e.target;
    marker.setStyle(style(e));
}

function zoomToFeature(e) {
    'use strict';
    var marker;
    marker = e.target;
    map.fitBounds(marker.getBounds());
}

function set_offset() {
    'use strict';
    var navbar, navbar_height, map, content, map_offset, content_offset;
    navbar = $('.navbar');
    navbar_height = navbar.height();
    map = $('#map');
    content = $('#content');

    if (map.length) {
        map_offset = map.offset();
        map.offset({top: navbar_height, left: map_offset.left});
    }
    if (content.length) {
        content_offset = content.offset();
        content.offset({top: navbar_height, left: content_offset.left});
    }

}


function add_campus(campus_json, campus_id) {
    'use strict';
    campus_json.features[0].properties.id = campus_id;
    campus_lookup[campus_id] = campus_json;

    // create markers
    var feature = campus_json.features[0];
    var coordinate = feature.geometry.coordinates;
    var latlon = {lat: coordinate[1], lon: coordinate[0]};
    var marker = L.circleMarker(latlon, style(null));
    campus_marker[campus_id] = marker;
    marker.addTo(campus_cluster_group);

    // setup marker
    marker.bindPopup(feature.properties.popup_content);
    marker.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        dblclick: zoomToFeature
    });
}


function SelectFeature(campus_id){
    try{
        var feature = campus_lookup[campus_id].features[0];
        var coordinate = feature.geometry.coordinates;
        feature.properties.selected = true;
        var e = {
            target: campus_marker[campus_id]
        };
        if(highlighted_feature){
            resetHighlight(highlighted_feature);
        }
        highlightFeature(e);
        highlighted_feature=e;
        campus_cluster_group.zoomToShowLayer(e.target, function(){
            map.panTo({lat: coordinate[1], lon: coordinate[0]}, {animate: true});
        });
        openCampusPopup(campus_id);
    }
    catch(e){
        console.log(e);
    }
}

function CampusItemToggle(el){
    var panel = $(el).closest('.panel-primary').find('.panel-collapse');
    panel.toggleClass('collapse');
    var icon = $(el).find("i");
    if(panel.hasClass('collapse')){
        icon.removeClass('mdi-navigation-expand-less');
        icon.addClass('mdi-navigation-expand-more');
    }
    else{
        icon.removeClass('mdi-navigation-expand-more');
        icon.addClass('mdi-navigation-expand-less');
    }
}

function openCampusPopup(campus_id){
    var marker = campus_marker[campus_id];
    marker.openPopup();
}