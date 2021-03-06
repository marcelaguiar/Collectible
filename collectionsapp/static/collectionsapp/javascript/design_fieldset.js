function addFieldToFieldset() {
    var fieldsetName = document.getElementById("fieldsetNameInput").value;
    var fieldsetType = document.getElementById("fieldsetTypeInput").value;


    if(String(fieldsetName) == "")
        return;

    var table = document.getElementById("fieldset");
    var row = table.insertRow(1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);

    cell1.innerHTML = "0";
    cell2.innerHTML = fieldsetName;
    cell3.innerHTML = fieldsetType;
    cell4.innerHTML = "<button type=\"button\" class=\"btn btn-outline-danger btn-sm\"  onclick=\"removeField(this)\">remove</button>";

    cell3.style.color = "darkgray";

    document.getElementById("fieldsetNameInput").value = "";
    renumberTable();
}

function removeField(button) {
    var row = button.parentNode.parentNode;

    row.parentNode.removeChild(row);

    renumberTable();
}

function renumberTable() {
    var table = document.getElementById("fieldset");

    for (var i = 1; i <= table.rows.length; i++) {
        var row = table.rows[i];

        row.cells[0].innerHTML = i.toString() + ".&nbsp;&nbsp;";
    }
}