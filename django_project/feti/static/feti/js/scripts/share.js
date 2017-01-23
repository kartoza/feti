/**
 * Created by Dimas on 12/3/16.
 */
define([
], function () {

    var Share = new function(){

        this.sharePDF = function() {
            var url = '/pdf_report/';
            var currentRoute = Backbone.history.getFragment().split('/');
            if(currentRoute.length > 2) {
                window.location = url + currentRoute[1] + '/' + currentRoute[2];
            } else if(currentRoute.indexOf('favorites') > 0) {
                window.location = url + currentRoute[1] + '/all';
            }
        }
        ;

        this.shareEmail = function() {
            var currentRoute = Backbone.history.getFragment().split('/');
            // Open Modal
            if(currentRoute.length > 1) {
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
                    url:'share_email/',
                    type:'POST',
                    data: JSON.stringify(all_data),
                    success: function(response) {
                        if(response=='success') {
                            $('#email-modal').modal('toggle');
                            alert('Email sent!');
                        }
                    },
                    error: function(response) {
                        alert('Error sending email');
                    },
                    complete: function() {
                        $('#email-submit').prop('disabled', false);
                        $('#email').prop('disabled', false);
                    }
                });
            });
        };

        this.shareToTwitter = function () {
            // get url
            var host = Backbone.history.location.host;

            _generateURL(function (data) {
                var twitter_intent = 'https://twitter.com/intent/tweet?text=Check this out!%0A'+
                    host+'/url/'+data;
                // open twitter box
                window.open(twitter_intent, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
            });
        };

        this.shareURL = function () {
            // get url
            var host = Backbone.history.location.host;

            _generateURL(function (data) {
                window.prompt("Copy to clipboard: Ctrl+C, Enter", host+'/url/'+data);
            });
        };

        var _generateURL = function (callback) {
            var full_url = Backbone.history.location.href;

            $.ajax({
                url:'api/generate-random-string/',
                type:'POST',
                data: JSON.stringify({
                    'url': full_url
                }),
                success: callback
            });
        }
    };

    return Share;

});