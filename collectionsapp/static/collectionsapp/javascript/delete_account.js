const targetUsername = $('#username-value').val();

$("#usernameConfirm").dxTextBox({
    onValueChanged: function (e) {
        if(e.value === targetUsername) {
            $('#deleteButton').prop('disabled', false);
        }
        else {
            $('#deleteButton').prop('disabled', true);
        }
    },
    valueChangeEvent: "keyup"
});