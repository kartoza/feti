/*global define */
define([
    'common',
    'scripts/views/occupation-view',
    'scripts/models/occupation',
    'scripts/collections/category'
], function (Common, OccupationView, Occupation, Category) {
    var OccupationCollection = Category.extend({
        model: Occupation,
        provider_url_template: _.template("/api/occupation?q=<%- q %>&page=<%- page %>"),
        total_page: 0,
        initialize: function() {
            this.url_template = this.provider_url_template;
            this.view = OccupationView;
            this.mode = 'occupation';
            Common.Dispatcher.on('collections:finishCreate', this.onFinishedCreateRow, this);
        },
        parse: function (response, model) {
            this.total_page = response['total_page'];
            this.current_page = response['current_page'];
            this.max_page = response['max'];
            return response['data'];
        },
        onFinishedCreateRow: function (resultsLength) {
            var that = this;
            if(this.current_page < this.total_page) {
                $('#result-container-occupation').append('<div id="result-load-more" class="result-title result-load-more" style="cursor: pointer;">\n' +
                                                            '<div class="title">Load More</div>\n' +
                                                         '</div>');
                $('.result-load-more').on('click', function (element) {
                    that.current_page += 1;
                    that.search_changed = false;
                    that.search(that.last_query);
                    $(this).remove();
                })
            } else {
                $('#result-container-occupation').find('.result-load-more').remove();
            }
        }

    });

    return new OccupationCollection();
});
