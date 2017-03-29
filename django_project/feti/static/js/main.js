// Require.js allows us to configure shortcut alias
require.config({
    paths: {
        text: 'libs/text',
        common: 'common'
    }
});

require([
    'routers/router',
    'common'
], function (Workspace, Common) {
    Common.Router = new Workspace();
    Backbone.history.start();


    if (Common.EmbedVersion) {
        // for embed version
        $(document).ready(function () {
            var $toogleButton = $('#toogle-button');
            $toogleButton.click(function (event) {
                var $faButton = $toogleButton.find('.fa');
                Common.Dispatcher.trigger('toogle:result', event);
                if ($faButton.hasClass('fa-caret-left')) {
                    $faButton.removeClass('fa-caret-left');
                    $faButton.addClass('fa-caret-right');
                    $toogleButton.attr('title', 'Hide side panel');
                } else {
                    $faButton.removeClass('fa-caret-right');
                    $faButton.addClass('fa-caret-left');
                    $toogleButton.attr('title', 'Show side panel');
                }
                $toogleButton.tooltip();
            });
        });
    }
});
