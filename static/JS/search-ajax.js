$(document).ready(function(){

    $('#search-input').keyup(function(e) {
        e.preventDefault() ;
        var query = $(this).val();

        if (query.length > 0) {
            $.get(suggestUrl,
                {'suggestion': query},
                function(data) {
                    $('#search-suggestions').html(data);
                    $('#search-suggestions').show();
                });
        } else {
            $('#search-suggestions').hide();
        }
    });

    $('#nav-search').submit(function(e) {
        e.preventDefault();
    });

    $(document).click(function(e) {
        if (!$(e.target).closest('#nav-search').length) {
            $('#search-suggestions').hide();
        }
    });

}) ;
