/**
 * 
 * @authors Your Name (you@example.org)
 * @date    2017-11-28 21:21:55
 * @version $Id$
 */

var app = (function ($) {
    var config = $('#config'),
        app = JSON.parse(config.text());
    
    $(document).ready(function () {
    	var router = new app.router();
    });
        
    return app;
})(jQuery);
