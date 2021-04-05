(function() {
    $.validator.methods.email = function(value, element) {
        var exp = /^[\.\-\w]{2,50}@[\-\w]{2,50}\.\w{2,15}(\.\w{2,15})?$/;
        return this.optional(element) || exp.test($.trim(value));
    };

    $.validator.addMethod("username", function(value, element) {
        var exp = /^[\w-]*$/;
		return this.optional(element) || exp.test($.trim(value));
    }, "Invalid characters in the username");

    $.validator.addMethod("repetitive", function(value, element) {
        var exp = /.*(.)\1{2}.*/;
        return this.optional(element) || !exp.test($.trim(value));
    }, "Too many repeating characters");

    $.validator.addMethod("numeric", function(value, element) {
        var exp = /^\d*$/;
        return this.optional(element) || !exp.test($.trim(value));
    }, "Just numbers used");

    $('#form-signup').validate({
        errorPlacement: function(error, element) {
            // Case there is a hint element, so put the error message after it.
            var hint = element.siblings('.hint');
            if (hint.length > 0) {
                element = hint;
            }

            error.insertAfter(element);
        },
        rules: {
            username: {
                username: true,
                repetitive: true,
                remote: {
                    url: '/private-api/username-check/'
                },
                normalizer: function(value) {
                    // Trim white spaces from edges and force lowercase.
                    return $.trim(value).toLowerCase();
                }
            },
            email: {
                email: true
            },
            password1: {
                numeric: true,
                minlength: 8
            },
            password2: {
                minlength: 8,
                equalTo: "#id_password1",
            }
        },
        messages: {
            username: {
                remote: "This username is already being used"
            },
            password1: {
                numeric: 'Your password can\'t be entirely numeric.'
            },
            password2: {
                equalTo: "Please enter the same password as above"
            }
        }
    });
})();
