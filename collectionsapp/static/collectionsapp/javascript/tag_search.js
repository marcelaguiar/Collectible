let specifiedTag = document.getElementById("slug").value;
let specifiedCollectionId = document.getElementById("collection-id").value;
let specifiedCollectionOwnerUserName = document.getElementById("collection-owner-username").value;
let specifiedCollectionTypeName = document.getElementById("collection-type_name").value;
let initialLoad = true;

setUpControls();
loadResults(specifiedTag, specifiedCollectionId);

function setUpControls() {
    $("#tagSelector").dxSelectBox({
        dataSource: "/get_all_tags/",
        displayExpr: "name",
        valueExpr: "slug",
        placeholder: "Search & select...",
        searchEnabled: true,
        //width: "300px",
        itemTemplate: function (data) {
            return "<div style='display: flex; justify-content: space-between;'><div>"
                + data.name + "</div><div style='color:silver'>"
                + data.count + "</div></div>";
        },
        value: specifiedTag,
        onSelectionChanged: function(e){
            if(initialLoad) {
                initialLoad = false;
            }
            else {
                specifiedTag = e.selectedItem.slug;
                loadResults(specifiedTag, specifiedCollectionId);
            }
        }
    });

    $("#collectionToggle").dxButtonGroup({
        items: [
            {
                "collectionId": specifiedCollectionId,
                "text": specifiedCollectionOwnerUserName + "'s collection"
            },
            {
                "collectionId": null,
                "text": "All " + specifiedCollectionTypeName + " collections"
            }
        ],
        keyExpr: "collectionId",
        stylingMode: "outlined",
        selectedItemKeys: specifiedCollectionId,
        onSelectionChanged: function(e){
            specifiedCollectionId = e.addedItems[0].collectionId
            loadResults(specifiedTag, specifiedCollectionId);
        }
    });
}

function loadResults(slug, collectionId) {
    alert(slug);
    // Clear container
    $(".image-grid").empty();

    // Determine datasource url
    let dataUrl = "";
    if(collectionId == null)
        dataUrl = "/get_by_tag/" + slug + "/";
    else
        dataUrl = "/get_by_tag_and_collection/" + slug + "/" + collectionId + "/";

    // Get results and put into container
    $.ajax({
        dataType: "json",
        url: dataUrl,
        success: function(data) {
            data.forEach(addToResults);

            function addToResults(value, index, array) {
                const id = value.id;
                const url = value.full_url;

                let e = "<div class=\"grid-item\"><a href=\"/bottle_cap/" + id + "/\"><img src=\"" + url + "\" alt=\"test\"></a></div>";

                $(".image-grid").append(e);
            }
        }
    });
}