/**
 * Created by ismailsunni on 1/13/15.
 */
/*global $, jQuery, L, window, console*/
var map;
var campus_lookup = {};

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

}

function update_rws() {
    'use strict';
    var village_select = $('#id_village'),
        village_id = village_select.val(),
        rw_select = $('#id_rw'),
        rt_select = $('#id_rt');
    rw_select.find('option').remove().end();
    rw_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    if (village_id === '') {
        return;
    }
    village_select.attr("disabled", "disabled");
    $.get('/api/locations/' + village_id + '/?format=json', function (data) {
        /*jslint unparam: true*/
        $.each(data, function (dummy, rw) {
            $('#id_rw').append($("<option></option>")
                .attr("value", rw.id)
                .text(rw.name));
        });
        /*jslint unparam: false*/
        village_select.removeAttr("disabled");
    });
}

function update_rts() {
    'use strict';
    var village_id = $('#id_village').val(),
        rw_select = $('#id_rw'),
        rw_id = rw_select.val(),
        rt_select = $('#id_rt');
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    if ((village_id === '') || (rw_id === '')) {
        return;
    }
    rw_select.attr("disabled", "disabled");
    $.get('/api/locations/' + village_id + '/' + rw_id + '/?format=json',
        function (data) {
            /*jslint unparam: true*/
            $.each(data, function (dummy, rt) {
                $('#id_rt').append($("<option></option>")
                    .attr("value", rt.id)
                    .text(rt.name));
            });
            /*jslint unparam: false*/
            rw_select.removeAttr("disabled");
        });
}


function update_rts_rws() {
    'use strict';
    $('#nav_add_flood_status_report').addClass("active");
    // Setup location selecton
    $('#id_village').on('change', update_rws);
    $('#id_rw').on('change', update_rts);
    // Setup date time picker
    var date_time = $('#id_date_time');
    date_time.datetimepicker({
        format: 'YYYY-MM-DD HH:mm'
    });
}

function updateFloodAreaReport() {
    'use strict';
    var rt = $('#rt'),
        rt_id,
        depths = [];
    rt.prop('disabled', 'disabled');
    rt_id = rt.val();
    $.get('/api/reports/rt/' + rt_id + '/?format=json', function (data) {
        if (data.length === 0) {
            $('#current_flood_depth_div').hide();
            $('#flood_depth_over_time_div').hide();
        } else {
            var graph = $('#flood_depths_graph'),
                village = $('#village');
            $('#current_flood_depth').text(data[0].depth + 'm');
            $('#current_flood_depth_div').show();

            $.each(data, function (dummy, rt) {
                depths.push([
                    new Date(rt.date_time),
                    parseFloat(rt.depth),
                ]);
            });
            depths.reverse();
            graph.width(village.width());
            graph.height(village.height() * 10);
            $.plot(graph, [depths, depths],
            {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    splines: {
                        show: true,
                        tension: 0.4,
                        lineWidth: 1,
                        fill: 0.4
                    },
                    points: {
                        radius: 2,
                        show: true
                    },
                    shadowSize: 2
                },
                grid: {
                    hoverable: true,
                    clickable: true,
                    tickColor: "#d5d5d5",
                    borderWidth: 1,
                    color: '#d5d5d5',
                    labelMargin: 30
                },
                colors: ["#4285f4", "#4285f4"],
                xaxis: {
                    mode: "time",
                    tickSize: [
                        parseInt(
                            (depths[depths.length-1][0] - depths[0][0]) /
                            15000000
                        ),
                        "hour"
                    ],
                    tickLength: null,
                    axisLabel: "Date",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Arial',
                    axisLabelPadding: 10,
                    color: "#838383"
                },
                yaxis: {
                    position: 'left',
                    min: 0,
                    max: 10,
                    ticks: 5,
                    alignTicksWithAxis: 1
                }
            }
            );
            $("<div id='tooltip'></div>").css({
                position: "absolute",
                display: "none",
                border: "1px solid #fdd",
                padding: "2px",
                "background-color": "#fee",
                opacity: 0.80
            }).appendTo("body");
            graph.bind("plothover", function (event, pos, item) {
                if (item) {
                    var date_time = new Date(item.datapoint[0]),
                        water_depth = item.datapoint[1].toFixed(2),
                        tooltip_text;
                    tooltip_text = (
                        "Banjir sedalam " + water_depth +
                        "m<br>terjadi pada " + date_time.toLocaleString(
                            'id', {timeZone: 'ASIA/JAKARTA'})
                    );
                    $("#tooltip").html(tooltip_text)
                        .css({top: item.pageY+5, left: item.pageX+5})
                        .fadeIn(200);
                } else {
                    $("#tooltip").hide();
                }
            });
            $('#flood_depth_over_time_div').show();

        }
        rt.prop('disabled', false);
    });
}

function updateFloodAreaOptions(rw_id, rw_name) {
    'use strict';
    $('#rw').text(rw_name);
    $('#village').text('');
    var rt_select = $('#rt');
    rt_select.find('option').remove().end();
    rt_select.append($("<option></option>")
        .attr("value", '')
        .text('---------'));
    $.get('/api/village/' + rw_id + '/?format=json', function (data) {
        $('#village').text(data.name);
        var village_id = data.id;
        $.get('/api/locations/' + village_id + '/' + rw_id + '/?format=json', function (data) {
            /*jslint unparam: true*/
            $.each(data, function (dummy, rt) {
                rt_select.append($("<option></option>")
                    .attr("value", rt.id)
                    .text(rt.name));
            });
            /*jslint unparam: false*/
        });
    });
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
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        color: 'white',
        dashArray: '',
        fillOpacity: 0.3,
        fillColor: 'blue'
    });
    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
}

function resetHighlight(e) {
    'use strict';
    var layer = e.target;
    layer.setStyle(style(e));
}

function zoomToFeature(e) {
    'use strict';
    var layer;
    layer = e.target;
    map.fitBounds(layer.getBounds());
}

/*jslint unparam: true*/
function onEachFeature(feature, layer) {
    'use strict';
    console.log(feature);
    layer.bindPopup(feature.properties.popup_content);
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        dblclick: zoomToFeature
    });
}
/*jslint unparam: false*/

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
    var campus_feature;
    var geojsonMarkerOptions = {
        radius: 6,
        fillColor: "#ff7800",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };
    campus_feature = L.geoJson(campus_json, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, geojsonMarkerOptions);
        },
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
    campus_lookup[campus_id] = campus_feature;
}


function SelectFeature(campus_id){
    var feature = campus_lookup[campus_id];
    map.fitBounds(feature.getBounds());
    SelectFeature(feature);
}