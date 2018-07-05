/**
 * Created by Dimas on 12/3/16.
 */


define([
    'backbone',
    'jquery',
    'underscore',
    'common'
], function (Backbone, $, _, Common) {

    var Share = new function () {

        this.sharePDF = function () {
            var query = Common.Router.parameters.query;
            var currentRoute = Backbone.history.getFragment().split('/');
            var resource = currentRoute[1] || 'provider';
            var url = '/pdf_report/' + resource + '?export=pdf';
            // this is not pretty
            if (resource === 'favorites')
                url += '&' + query;
            else {
                if (typeof(currentRoute[2]) !== 'undefined')
                    url += '&q=' + currentRoute[2];

                if (typeof(currentRoute[3]) !== 'undefined')
                    url += '&' + currentRoute[3];

            }
            window.location = url;
        };

        this.shareEmail = function () {
            var currentRoute = Backbone.history.getFragment().split('/');
            // Open Modal
            if (currentRoute.length > 1) {
                $('#email-modal').modal('toggle');
            }

            $('#email-form').submit(function (e) {
                e.preventDefault();
                var all_data = {};

                all_data.email = $('#email').val();
                all_data.provider = currentRoute[1];
                all_data.query = currentRoute[2];
                all_data.link = Backbone.history.location.href;

                $('#email-submit').prop('disabled', true);
                $('#email').prop('disabled', true);

                $.ajax({
                    url: 'share_email/',
                    type: 'POST',
                    data: JSON.stringify(all_data),
                    success: function (response) {
                        if (response == 'success') {
                            $('#email-modal').modal('toggle');
                            alert('Email sent!');
                        }
                    },
                    error: function (response) {
                        alert('Error sending email');
                    },
                    complete: function () {
                        $('#email-submit').prop('disabled', false);
                        $('#email').prop('disabled', false);
                    }
                });
            });
        };

        this.shareToTwitter = function () {
            // get url
            var host = Backbone.history.location.host;
            var windowReference = window.open('', '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');

            _generateURL(function (data) {
                var twitter_intent = 'https://twitter.com/intent/tweet?text=Check this out!%0A' +
                    host + '/url/' + data;
                // open twitter box
                windowReference.location = twitter_intent;
            });
        };

        this.shareURL = function () {
            // get url
            var host = Backbone.history.location.host;
            $('input#clipboard').select();
            $('#copy-status').html('');

            _generateURL(function (data) {
                $('#clipboard-modal').modal('toggle');
                $('#clipboard').val(host + '/url/' + data);
            });
        };

        this.getEmbedCode = function () {
            // get url
            var host = Backbone.history.location.host;
            var url = Backbone.history.location.href;
            url = url.replace(host, host + '/embed')

            $('input#clipboard').select();
            $('#copy-status').html('');

            _generateURL(function (data) {
                $('#clipboard-modal').modal('toggle');
                var url = host + '/url/' + data;
                var iframe = '<iframe width="400" height="300" src="http://' + url + '">' + '</iframe>';
                $('#clipboard').val(iframe);
            }, url);
        };

        var _generateURL = function (callback, url) {
            var full_url = '';
            if (url) {
                full_url = url;
            } else {
                full_url = Backbone.history.location.href;
            }

            $.ajax({
                url: 'api/generate-random-string/',
                type: 'POST',
                data: JSON.stringify({
                    'url': full_url
                }),
                success: callback
            });
        };

        $('#copy-clipboard').click(function () {
            var clipboard = $('#clipboard').val();

            if (clipboard) {
                var $temp = $("<input>");
                $("body").append($temp);
                $temp.val(clipboard).select();
                document.execCommand("copy");
                $temp.remove();
                $('#copy-status').html('Copied to clipboard.');
            }
        })
    };

    return Share;

});