// Require.js allows us to configure shortcut alias
require.config({
	paths: {
		text: '/static/feti/js/libs/text',
        common: '/static/feti/js/scripts/common',
		service: '/static/feti/js/scripts/service'
	}
});

require([
	'/static/feti/js/scripts/routers/router.js',
    'common'
], function (Workspace, Common) {
	Common.Router = new Workspace();
	Backbone.history.start();
});
