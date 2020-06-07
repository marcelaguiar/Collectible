let scrollDebounce = true;
let loadedThumbnailsCount = parseInt(document.getElementById("initial_load_quantity").value);
const loadSize = 100;

$("#dxLoadIndicator").dxLoadIndicator({
    height: 40,
    width: 40,
    visible: false
});


function loadData() {
    scrollDebounce = false;

    $("#dxLoadIndicator").dxLoadIndicator('instance').option('visible', true);

    const start = loadedThumbnailsCount;
    const end = loadedThumbnailsCount + loadSize;

    $.ajax({
        type: "GET",
        url: "/get_n_thumbnails/" + String(start) + "/" + String(end),
        success: function (data) {
            $("#dxLoadIndicator").dxLoadIndicator('instance').option('visible', false);

            let i;
            for (i = 0; i < data.length; i++) {
                $(".image-grid").append(
                    "<div class='grid-item'>" +
                        "<a href='" + data[i].collection_item_url + "' >" +
                            "<img src='" + data[i].image_url + "' alt='" + data[i].collection_item_name + "'>" +
                        "</a>" +
                    "</div>"
                );
            }

            loadedThumbnailsCount += loadSize;
        },
        error: function() {
            console.log("error");
        }
    });

    setTimeout(function () { scrollDebounce = true; }, 1000);
}

$(window).scroll(function() {
    if(scrollDebounce) {
        const bottom = $("footer").offset().top;
        const viewBottom = $(window).scrollTop() + $(window).height();
        const distance = bottom - viewBottom;

        if (distance < 200) {
            loadData();
        }
    }
});