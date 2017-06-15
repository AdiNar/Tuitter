$(document).ready(function() {
    $('#friend-add-form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: "/add_friend/" + $('#id_user').val() + "/",
            type: "POST",
            success: function(data) {
                $('#users-list').append(data);
            },
            error: function(json) {
                alert("error");
            },
        });
    });
});