SetUpSearchResults();

function SetUpSearchResults() {
    $("#gridContainer").dxDataGrid({
        dataSource: "json/",
        showBorders: true,
        searchPanel: {
            highlightCaseSensitive: false,
            highlightSearchText: true,
            searchVisibleColumnsOnly: true,
            text: criteria,
            visible: true,
            width: 500
        }
    });
}
