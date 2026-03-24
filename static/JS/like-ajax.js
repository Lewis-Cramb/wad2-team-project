$(document).ready(function(){
    $('.likeBttn').click(function(){

        var bttn = $(this)
        var revIDVar ;
        revIDVar = $(this).attr('data-category-id') ;

        $.get(likeUrl,
            {'review_id':revIDVar},
            function(data){
                bttn.find('#like_count').html(data) ;
            })

    }) ;

}) ;



