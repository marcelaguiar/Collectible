function setUpControls() {
    $("#image-migrate").dxButton({
        stylingMode: "contained",
        text: "Migrate images to collection items",
        type: "normal",
        onClick: function() {
            $.ajax({
                type: "GET",
                url: "/migrate_images/",
                success: function () {
                    alert("done!")
                }
            });
        }
    });
}

setUpControls();
