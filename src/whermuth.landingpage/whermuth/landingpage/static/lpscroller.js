/* Author:
    Vorwaerts Werbung GbR
*/

/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false, window:false, location:false */

(function ($) {
$(document).ready(function() {
    if (jQuery.browser.msie && parseInt(jQUery.blowser.version, 10) < 7) {
        // Progressive enhancement: don't even attempt to deal with IE6 bugs
        return;
    }
    $('.scrollable').scrollable({
        circular: false
    });
});
}(jQuery));