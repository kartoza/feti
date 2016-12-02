define([
    'text!static/feti/js/scripts/templates/sidebar.html',
    'common'
], function (sidebarTemplate, Common) {
    var SideBarView = Backbone.View.extend({
        tagName: 'div',
        container: '#result',
        template: _.template(sidebarTemplate),
        events: {
        },
        initialize: function (options) {
            this.render();
            this._parent = options.parent;
            this._isOpen = false;
            this.$empty_result_div = $('.result-empty');
            this.$loading_div = $('.result-loading');
            this.$result_title = $('#result-title');
            this.$result_detail = $('#result-detail');
            Common.Dispatcher.on('sidebar:categoryClicked', this.showResultTitle, this);
            Common.Dispatcher.on('sidebar:update_title', this.updateResultTitle, this);
            Common.Dispatcher.on('sidebar:show_loading', this.addLoadingView, this);
            Common.Dispatcher.on('sidebar:hide_loading', this.clearContainerDiv, this);
            Common.Dispatcher.on('sidebar:clear_search', this.clearSidebar, this);

        },
        showOccupationDetail: function () {
            this.$result_detail.show("slide", {direction: "right"}, 300);
        },
        hideOccupationDetail: function () {
            if (this.$result_detail.is(":visible")) {
                this.$result_detail.hide("slide", {direction: "right"}, 300);
            }
        },
        render: function () {
            $(this.container).append(this.template());
        },
        is_open: function () {
            return this._isOpen;
        },
        open: function() {
            this._isOpen = true;
            $(this.container).show("slide", {direction: "right"}, 500);
        },
        close: function () {
            this._isOpen = false;
            $(this.container).hide("slide", {direction: "right"}, 500);
            this.hideOccupationDetail();
        },
        addLoadingView: function (mode) {
            this.clearContainerDiv(mode);
            this.$result_title.find('#result-title-'+mode).remove();
            $('#result-container-'+mode).append(this.$loading_div.show());
        },
        clearSidebar: function (mode) {
            if($('#result-container-'+mode+' .result-title').length > 0) {
                $('#result-container-'+mode+' .result-title').remove();
            }
            if($('#result-container-'+mode+' .share-item').length > 0) {
                $('#result-container-'+mode+' .share-item').remove();
            }
            this.$result_title.find('#result-title-'+mode).remove();
        },
        showEmptyResult: function (mode) {
            var $_empty_result_div = this.$empty_result_div.clone();
            $('#result-container-'+mode).append($_empty_result_div.show());
        },
        clearContainerDiv: function (mode) {
            if($('#result-container-'+mode+' .result-empty').length > 0) {
                $('#result-container-'+mode+' .result-empty').remove();
            }
            if($('#result-container-'+mode+' .result-loading').length > 0) {
                $('#result-container-'+mode+' .result-loading').remove();
            }
            if($('#result-container-'+mode+' .share-container').length > 0) {
                $('#result-container-'+mode+' .share-container').remove();
            }
        },
        addShareBar: function (mode) {
            if(mode!='favorites' && mode!='occupation') {
                var $share_container = $('.share-container');
                $('#result-container-'+mode).append($share_container.clone().show());
                var _this = this;
                $('#result-container-'+mode+' .share-pdf').click(function () {
                    _this.sharePDF();
                });
                $('#result-container-'+mode+' .share-social-twitter').click(function () {
                    _this.shareToTwitter();
                });
                $('#result-container-'+mode+' .share-email').click(function () {
                    _this.shareEmail();
                })
            }
        },
        updateResultTitle: function(number_result, mode, query) {
            this.hideOccupationDetail();
            this.clearContainerDiv(mode);
            if(number_result == 0) {
                this.showEmptyResult(mode);
            } else {
                this.addShareBar(mode);
            }
            this.$result_title.find('#result-title-'+mode).remove();

            var $result_title_number = $("<span>", {class: "result-title-number"});
            $result_title_number.html(number_result);

            var $result_title_mode = $("<span>", {class: "result-title-mode"});
            if(mode == 'occupation') {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  occupations': ' occupation');
            } else {
                $result_title_mode.html(parseInt(number_result) > 1 ? '  campuses': ' campus');
            }

            var $result_title_campus = $("<div>", {id: "result-title-" + mode});
            $result_title_campus.append($result_title_number);
            $result_title_campus.append($result_title_mode);

            var $result_title_place = $("<span>", {class: "result-title-place"});

            if (query.indexOf("administrative") >= 0) {
                query = query.split("=")[1];
                query = query.split();
                query.reverse();
                $result_title_place.html(' in ' + query.join().replace(",", ", "));
            } else if (query.indexOf("circle") >= 0) {
                var coordinates_index = query.indexOf("coordinate=") + "coordinate=".length;
                var radius_index = query.indexOf("&radius=");
                var coordinates = query.substring(coordinates_index, radius_index);
                radius_index = query.indexOf("&radius=") + "&radius=".length;
                var radius = parseInt(query.substring(radius_index, query.length));
                var coordinate = JSON.parse(coordinates);
                if (radius % 1000 > 1) {
                    radius = (radius % 1000) + " km"
                } else {
                    radius = radius + " meters"
                }
                $result_title_place.html(' in radius ' + radius + ' from [' + coordinate['lat'].toFixed(3) + " , " + coordinate['lng'].toFixed(3) + "]");
            }
            else {
                $result_title_place.html('');
            }
            $result_title_campus.append($result_title_place);

            this.$result_title.append($result_title_campus);
        },
        showResultTitle: function(newMode, oldMode) {
            $('#result-title-'+oldMode).hide();
            $('#result-title-'+newMode).show();
        },
        sharePDF: function() {
            var url = '/pdf_report/';
            var currentRoute = Backbone.history.getFragment().split('/');
            console.log(currentRoute);
            if(currentRoute.length > 2) {
                window.location = url + currentRoute[1] + '/' + currentRoute[2];
            }

        },
        shareEmail: function() {
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
        },
        shareToTwitter: function () {

            // get url
            var full_url = Backbone.history.location.href;
            var host = Backbone.history.location.host;

            // generate random string
            $.ajax({
                url:'api/generate-random-string/',
                type:'POST',
                data: JSON.stringify({
                    'url': full_url
                }),
                success: function(response) {
                    var twitter_intent = 'https://twitter.com/intent/tweet?text=Check this out!%0A'+
                        host+'/url/'+response;
                    // open twitter box
                    window.open(twitter_intent, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
                },
                error: function(response) {
                },
                complete: function() {
                }
            });
        }
    });

    return SideBarView;
});
