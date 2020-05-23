if(!!document.getElementById("gridContainer")) {
    SetUpDataGrid();
}

function SetUpDataGrid() {
    var collection_id = 0;

    if(!!document.getElementById("collection-id")) {
        collection_id = document.getElementById("collection-id").value;
    }

    var beverageTypeLookupDataSource = {
        store: new DevExpress.data.CustomStore({
            key: "id",
            loadMode: "raw",
            load: function() {
                return $.getJSON("/get_all_beverage_types");
            }
        }),
        sort: "name"
    };

    $("#gridContainer").dxDataGrid({
        dataSource: "/get_all_bottle_caps_by_collection/" + collection_id +"/",
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
            {
                dataField: "id",
                dataType: "number",
                visible: false
            },
            {
                dataField: "company",
                dataType: "string",
                filterValue: "unidentified",
                selectedFilterOperation: "<>"
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