SetUpSearchResults();

function SetUpSearchResults() {
    $("#gridContainer").dxDataGrid({
        dataSource: "json/",
        showBorders: true,
        showRowLines: true,
        rowAlternationEnabled: true,
        searchPanel: {
            highlightCaseSensitive: false,
            highlightSearchText: true,
            searchVisibleColumnsOnly: true,
            text: $("#search-criteria").val(),
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
         columns: [{
            type: "buttons",
            buttons: [{
                text: "Link",
                onClick: function (e) {
                    var itemId = e.row.values[1];
                    window.location = '/bottle_cap/' + (itemId).toString();
                }
            }]
        }, "Id", "Company", "Brand", "Product", "Variety", "Date acquired"],
        allowColumnResizing: true,
        columnResizingMode: "nextColumn",
        columnMinWidth: 50,
        columnAutoWidth: true,
    });
}
