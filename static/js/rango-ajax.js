$(document).ready(function() {
    // Let the feather icon display correctly
    feather.replace();

    $('#like_btn').click(function(){
        var categoryId = $(this).attr('data-categoryid');
        jQuery.get('/rango/like_category/', {'category_id': categoryId},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });
});