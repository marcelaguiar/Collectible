SetUpSearchResults();

function SetUpSearchResults() {
    $("#gridContainer").dxDataGrid({
        dataSource: "json/",
        showBorders: true,
        searchPanel: {
            highlightCaseSensitive: false,
            highlightSearchText: true,
            searchVisibleColumnsOnly: true,
            text: $("#search-criteria").val(),
            visible: true,
            width: 500
        },
        filterRow: {
            visible: true,
            applyFilter: "auto"
        }
    });
}
