function collectionSelectBox(userId) {
    var userCollectionsDatasource = {
        store: new DevExpress.data.CustomStore({
            key: "id",
            loadMode: "raw",
            load: function() {
                return $.getJSON("/get_users_collections/" + userId);
            }
        })
    };

    $("#collectionSelectBox").dxSelectBox({
        dataSource: userCollectionsDatasource,
        valueExpr: "id",
        displayExpr: "name",
        placeholder: "Select a collection..."
    }).dxValidator({
        validationRules: [{ type: 'required' }]
    });
}

function uploadFileToServer(fileToSubmit, collection_id, csrf_token) {

    var fd = new FormData();
    fd.append('file', fileToSubmit);
    fd.append('collection_id', collection_id);
    fd.append('csrfmiddlewaretoken', csrf_token);

    $.ajax({
        type: "POST",
        url: "/post_file/",
        data: fd,
        contentType: false,
        processData: false,
        success: function () {
            let progressBar = $("#progressBarContainer").dxProgressBar('instance');
            let progressValue = progressBar.option('value');
            progressBar.option("value", progressValue + 1);
        }
    });
}

function startProgressBar(fileCount) {
    $("#progressBarContainer").dxProgressBar({
        min: 0,
        max: fileCount,
        value: 0,
        onComplete: function(e){
            inProgress = false;  // TODO: remove
            e.element.addClass("complete");
        },
        elementAttr: {
            class: "margin-top"
        },
        statusFormat: function(ratio, value) {
            return (ratio * 100).toFixed(2) + "% (" + value + ")";
        }
    });
}


function submitButton() {
    $("#image-select-form").submit(function () {
        const files = document.querySelector('input[type=file]').files;
        const collection_id = $("#collectionSelectBox").dxSelectBox('instance').option('value');
        const csrf_token = $('#image-select-form input[name=csrfmiddlewaretoken]').attr('value');

        startProgressBar(files.length);

        if(files != null && collection_id != null) {
            let i;
            for (i = 0; i < files.length; i++) {
                uploadFileToServer(
                    files[i],
                    collection_id,
                    csrf_token
                );
            }
        }

        return false;
    });
}

function setUpControls() {
    const current_user_id = document.getElementById("user_id").value;

    collectionSelectBox(current_user_id);
    submitButton();
}

setUpControls();
