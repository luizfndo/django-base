(function() {
    var formRequestDelete = $('.request-delete form');

    $('.request-delete button').on('click', function(event) {
        event.preventDefault();
        if(confirm("Are you sure about delete your account ?")) {
            formRequestDelete.submit();
        }
    });
})();
