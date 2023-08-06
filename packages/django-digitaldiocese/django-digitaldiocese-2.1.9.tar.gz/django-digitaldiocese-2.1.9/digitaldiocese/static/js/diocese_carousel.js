/* global $, Flickity */

$(function() {
    var carousel = $('.js-carousel');

    $.each(carousel, function(index, elem) {
        var self = $(this);

        var body = $('body');
        var lightbox = $('#lightbox');
        var lightbox_content = $('#lightbox_content');
        var lightbox_backdrop = $('#lightbox_backdrop');
        var carousel = self.find('.diocese-carousel');
        var videos = self.find('.slide-video');
        var buttons = $(elem).find('.js-carousel-button');

        var flickity_options = {
            cellAlign: 'left',
            contain: true,
            pageDots: false,
            draggable: false,
            arrowShape: 'M 20,50 L 65,5 L 65,95 L 20,50 Z',
            wrapAround: true,
            imagesLoaded: true
        };

        if (self.data('autoplay')) {
            flickity_options.autoPlay = self.data('autoplay');
        }

        var flkty = carousel.flickity(flickity_options);
        var flkty_data = flkty.data('flickity');

        flkty.on('select.flickity', function() {
            /*
                when you change slide using the arrows it will update the respective
                navigation panel button.
            */
            buttons.removeClass('active');
            $(buttons[flkty_data.selectedIndex]).addClass('active');
        });

        videos.on('click', function(e) {
            /*
                when you click a video it will open the link in a light box.
            */
            var self = $(this);
            var iframe = self.data('iframe');

            body.addClass('lightbox-open');
            lightbox.addClass('visible');
            lightbox_content.html('<div class="video-iframe">' + iframe + '</div>');
        });

        buttons.on('click', function(){
            /*
                when you click a navigation panel button tab it will change slide and update the
                appropriate button with an active class.
            */
            var self = $(this);
            var index = self.index();

            buttons.removeClass('active');
            self.addClass('active');

            flkty.flickity('stopPlayer');
            flkty.flickity('select', index, true);
            flkty.flickity('playPlayer');
        });

        lightbox_backdrop.on('click', function() {
            body.removeClass('lightbox-open');
            lightbox.removeClass('visible');
            lightbox_content.html('');

        });
    });
});
