var searchCriteria = ($("#search-criteria").length ? $("#search-criteria").val() : "");

var beverageTypeLookupDataSource = {
    store: new DevExpress.data.CustomStore({
        key: "id",
        loadMode: "raw",
        load: function() {
            return $.getJSON("../get_all_beverage_types");
        }
    }),
    sort: "name"
};

SetUpSearchResults(searchCriteria);

function SetUpSearchResults(criteria) {
    $("#gridContainer").dxDataGrid({
        dataSource: "../get_all_bottle_caps/",
        showBorders: true,
        showRowLines: true,
        rowAlternationEnabled: true,
        searchPanel: {
            highlightCaseSensitive: false,
            highlightSearchText: true,
            searchVisibleColumnsOnly: true,
            text: criteria,
            visible: true,
            width: 400
        },
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
                width: 20
            },
            {
                dataField: "id",
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
                dataField: 'beverage_type',
                caption: 'Beverage type',
                lookup: {
                    dataSource: beverageTypeLookupDataSource,
                    valueExpr: 'id',
                    displayExpr: 'name'
                }
            },
            {
                dataField: "date_acquired",
                dataType: "date"
            }
        ],
        allowColumnResizing: true,
        columnResizingMode: "nextColumn",
        columnMinWidth: 50,
        columnAutoWidth: true
    });
}
