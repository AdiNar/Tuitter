$(document).ready(function() {
    $('#twit-post-form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: "/twits/add_twit/",
            type: "POST",
            success: function(data) {
                $('#twits').prepend(data);
            },
            error: function(json) {
                alert("error");
            },
            data: {
                text:$('#id_text').val()
            }
        });
    });
});