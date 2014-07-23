(function($){
    $.fn.putLoading = function(){
        $(this).each(function(){
            if (typeof this.loadingContainer != 'undefined'){
                return;
            }
            var container = document.createElement('div');

            var offset = $(this).offset();

            $(container).css('left', offset.left + 'px')
                        .css('top', offset.top + 'px')
                        .width($(this).width())
                        .height($(this).height())
                        .css('position', 'absolute');

            var modal = document.createElement('div');
            $(modal).addClass("modal-backdrop").addClass('fade').addClass('in');
            $(modal).css('position', 'static')
                    .height($(this).height());

            var animation = document.createElement('div');
            $(animation).html('<div class="progress progress-striped active">'
                                +'<div class="progress-bar progress-bar-success" style="width: 100%">Loading</div>'
                                + '</div>');
            var animationWidth = 200;
            $(animation).css('position', 'relative')
                        .css('width', animationWidth + 'px')
                        .css('top', -($(this).height() - $(animation).height()) / 2 + 'px')
                        .css('left', ($(this).width() - animationWidth)/2 + 'px');

            $(container).append(modal);
            $(container).append(animation);
            $("body").append(container);
            this.loadingContainer = container;
        });
    };
    $.fn.removeLoading = function(){
        $(this).each(function(){
            if (typeof this.loadingContainer != 'undefined'){
                $(this.loadingContainer).remove();
                delete this.loadingContainer;
            }
        });
    };

    //small loading

    $.fn.showLoading = function(){
        $(this).each(function(){
            $(this).append(LOADING_IMAGE_HTML);
        });
    };

    $.fn.hideLoading = function(){
        $(this).each(function(){
            $(".loading", this).remove();
        });
    };
})(jQuery);