function setUpControls() {
    $("#image-migrate").dxButton();

    $("#trigger-thumbnail-refresh").dxButton({
        stylingMode: "contained",
        text: "Refresh thumbnails",
        onClick: function(e) {
            $.ajax({
                type: "GET",
                url: "/refresh_thumbnails/",
                success: function () {
                    alert("Job completed.");
                },
                error: function() {
                    alert("error");
                }
            });
        }
    });
}

setUpControls();
