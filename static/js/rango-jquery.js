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

    $('#search-input').keyup(function() {
        var query;
        query = $(this).val();
        $.get('/rango/suggest/', {'suggestion': query},
            function(data) {
                $('#categories-listing').html(data);
        })
    });
});