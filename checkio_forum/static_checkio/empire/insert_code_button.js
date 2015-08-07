$(function () {
    function wrapText($text, start, end) {
        var preSelection = $text.val().substring(0, $text[0].selectionStart),
            selection = $text.val().substring($text[0].selectionStart, $text[0].selectionEnd),
            postSelection = $text.val().substring($text[0].selectionEnd);
        $text.val(preSelection + start + selection + end + postSelection);
    }
    var $panel = $('.reply-markdown');
    if ($panel.length) {
        var $text = $('form.js-reply textarea');
        var $lastIcon = $panel.find('.js-box-preview').parents('li');

        var $link = $('<a href="#" title="Inline code"></a>');
        $link.append('<i class="fa fa-code"></i>');
        $('<li></li>').append($link).insertBefore($lastIcon);
        $link.click(function(event){
            event.stopPropagation();
            event.preventDefault();
            wrapText($text, '`', '`');
        });

        var $link2 = $('<a href="#" title="Block code"></a>');
        $('<li></li>').append($link2).insertBefore($lastIcon);
        $link2.append('<i class="fa fa-bars"></i>');
        $link2.click(function(event){
            event.stopPropagation();
            event.preventDefault();
            wrapText($text, '\n```\n', '\n```\n');
        });
    }
});
