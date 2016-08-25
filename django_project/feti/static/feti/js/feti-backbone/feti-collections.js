/**
 * Created by meomancer on 08/08/16.
 */
var SearchCollection = Backbone.Collection.extend({
    model: SearchResult,
    SearchResultViews: [],
    provider_url_template: _.template("/api/campus?q=<%- q %>"),
    url: function () {
        return this.url;
    },
    reset: function () {
        _.each(this.SearchResultViews, function (view) {
            view.destroy();
        });
        this.SearchResultViews = [];
        searchBarView.showResult();
    },
    getProvider: function (q) {
        var that = this;
        this.url = this.provider_url_template({q: q});
        this.fetch({
            success: function (collection, response) {
                that.reset();
                _.each(that.models, function (model) {
                    that.SearchResultViews.push(new SearchResultView({
                        model: model,
                        id: "search_" + model.get('id'),
                    }));
                });
            },
            error: function () {
                that.trigger('errorOnFetch');
            }
        });
    }
});

