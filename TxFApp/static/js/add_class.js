$(function() {
    $('.add-class').click(function() {
        $(this).find('i').toggleClass('fa-plus fa-check');
        $("#fakealert").show();
    });
});