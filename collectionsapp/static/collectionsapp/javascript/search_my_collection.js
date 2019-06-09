var searchCriteria = ($("#search-criteria").length ? $("#search-criteria").val() : "");

SetUpSearchResults(searchCriteria);

function SetUpSearchResults(criteria) {
    $("#gridContainer").dxDataGrid({
        dataSource: "json/",
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
                    element.append("<a href='/bottle_cap/" + info.data.Id +"'>Link</a>").css("text-align", "center");
                    },
                allowFiltering: false,
                allowSorting: false,
                width: 20
            },
            {
                dataField: "Id",
                visible: false
            }, "Company", "Brand", "Product", "Variety",
            {
                dataField: "Date acquired",
                dataType: "date"
            }],
        allowColumnResizing: true,
        columnResizingMode: "nextColumn",
        columnMinWidth: 50,
        columnAutoWidth: true
    });
}
