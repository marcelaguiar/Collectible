let today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
$('#id_date_acquired').datepicker({
    uiLibrary: 'bootstrap4',
    iconsLibrary: 'materialicons',
    format: 'yyyy-mm-dd',
    maxDate: today
});