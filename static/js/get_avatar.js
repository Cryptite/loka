$(function () {
    function getAvatar(player) {
        $.ajax({
            type: "GET",
            url: "http://localhost:3000/avatar/" + player,
            contentType: 'application/json',
            complete: function (xhr, status) {
                if (status === 'error' || !xhr.responseText) {
                }
                else {
                    var data = JSON.parse(xhr.responseText);
                    $('.' + player).attr('src', data["path"]);
                }
            }
        });
    }
});