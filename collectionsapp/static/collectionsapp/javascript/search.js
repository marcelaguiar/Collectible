var url = window.location.href;

if(new RegExp('explore_collection\/[0-9]+\/details$').test(url) || new RegExp('search\/').test(url)) {
    SetUpDataGrid();//SetUpDataGrid('details');
}
else if(new RegExp('explore_collection\/[0-9]+\/imageanddetails$').test(url)) {
    SetUpDataGrid();//SetUpDataGrid('imageanddetails');
}

function SetUpDataGrid() {
    var criteria = document.getElementById("search-criteria").value;

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
        dataSource: "/get_all_bottle_caps/",
        searchPanel: {
            highlightCaseSensitive: false,
            highlightSearchText: true,
            searchVisibleColumnsOnly: true,
            text: criteria,
            visible: true
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
                dataType: "Number",
                visible: false
            },
            {
                dataField: "company",
                dataType: "String"
            },
            {
                dataField: "brand",
                dataType: "String"
            },
            {
                dataField: "product",
                dataType: "String"
            },
            {
                dataField: "variety",
                dataType: "String"
            },
            {
                dataField: "beverage_type",
                caption: "Beverage type",
                lookup: {
                    dataSource: beverageTypeLookupDataSource,
                    valueExpr: "id",
                    displayExpr: "name"
                },
                dataType: "String"
            },
            {
                dataField: "date_acquired",
                dataType: "Date"
            }
        ]
    });
}