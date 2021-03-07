function setUpControls() {
    $("#image-migrate").dxButton();

    $("#trigger-thumbnail-refresh").dxButton({
        stylingMode: "contained",
        text: "Refresh thumbnails",
        onClick: function(e) {
            $.ajax({
                type: "GET",
                url: "/get_all_collection_item_ids/",
                success: function (data) {
                    for(let i = 0; i < data.length; i++) {
                        const collection_item_id = data[i].id;
                        console.log(collection_item_id);
                        $.ajax({
                            type: "GET",
                            url: "/refresh_thumbnails/" + collection_item_id + "/",
                            success: function () {
                                console.log(String(i + 1) + "/" + String(data.length));
                            },
                            error: function(xhr, status, error) {
                                console.log("Error on item #" + String(i));
                                let err = eval("(" + xhr.responseText + ")");
                                console.log(err.Message);
                            }
                        });
                    }
                },
                error: function() {
                    alert("error");
                }
            });
        }
    });
}

setUpControls();
