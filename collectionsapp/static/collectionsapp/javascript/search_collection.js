if(!!document.getElementById("gridContainer")) {
    let urlStr = String(window.location);
    let layout = urlStr.substring(urlStr.lastIndexOf("/") + 1, urlStr.length)
    SetUpDataGrid(layout);
}

function SetUpDataGrid(layout) {
    let collection_id = 0;

    if(!!document.getElementById("collection-id")) {
        collection_id = document.getElementById("collection-id").value;
    }

    const beverageTypeLookupDataSource = {
        store: new DevExpress.data.CustomStore({
            key: "id",
            loadMode: "raw",
            load: function() {
                return $.getJSON("/get_all_beverage_types");
            }
        }),
        sort: "name"
    };

    // Set data source (more efficient in cases when we don't need images)
    let dataSource = "";
    if(layout === "details") {
        dataSource = "/get_all_bottle_caps_by_collection/" + collection_id +"/"
    }
    else if(layout === "imagedetails") {
        dataSource = "/get_all_bottle_caps_with_image_by_collection/" + collection_id +"/"
    }

    // Set up data grid
    $("#gridContainer").dxDataGrid({
        dataSource: dataSource,
        searchPanel: {
            highlightCaseSensitive: false,
            highlightSearchText: true,
            searchVisibleColumnsOnly: true,
            visible: true,
            width: 300
        },
        showBorders: true,
        showRowLines: true,
        rowAlternationEnabled: true,
        allowColumnResizing: true,
        columnResizingMode: "nextColumn",
        columnMinWidth: 50,
        columnAutoWidth: true,
         filterRow: {
            visible: true,
            applyFilter: "auto"
        },
        headerFilter: {
            visible: true
        },
        columns: [
            {
                cellTemplate: function(element, info) {
                    element.append("<a href='/bottle_cap/" + info.data.id +"'>Link</a>").css("text-align", "center");
                },
                allowFiltering: false,
                allowSorting: false,
                allowSearch: false,
                width: 20
            },
            (layout == "imagedetails" ? {
                cellTemplate: function (container, options) {
                    $("<div>")
                        .append($("<img>", {
                            "src": options.data.full_url,
                            "width": '100px'
                        }))
                        .appendTo(container);
                },
                allowFiltering: false,
                allowSorting: false,
                width: 116
            } : {}
            ),
            {
                dataField: "id",
                dataType: "number",
                visible: false
            },
            {
                dataField: "company",
                dataType: "string",
            },
            {
                dataField: "brand",
                dataType: "string"
            },
            {
                dataField: "product",
                dataType: "string"
            },
            {
                dataField: "variety",
                dataType: "string"
            },
            {
                dataField: "beverage_type",
                caption: "Beverage type",
                lookup: {
                    dataSource: beverageTypeLookupDataSource,
                    valueExpr: "id",
                    displayExpr: "name"
                },
                dataType: "string"
            },
            {
                dataField: "region",
                dataType: "string"
            },
            {
                dataField: "date_acquired",
                dataType: "date"
            }
        ]
    });
}