let currentTab = 0;
showTab(currentTab);

function showTab(n) {
  let x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
}

function goToPopulateFields() {
  let x = document.getElementsByClassName("tab");
  x[0].style.display = "none";

  currentTab = 1;

  showTab(currentTab);
}

function goToSelectImage() {
  let x = document.getElementsByClassName("tab");
  x[1].style.display = "none";

  currentTab = 0;

  showTab(currentTab);
}

function readURL(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
            $('#collection-item-ref-img').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);

        document.getElementById("btn-go-to-populate-fields").disabled = false;
    }
}

$("#id_image").change(function(){
    readURL(this);
});