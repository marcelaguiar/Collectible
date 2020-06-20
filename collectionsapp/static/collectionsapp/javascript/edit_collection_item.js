window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        document.getElementById("edit-collection-item-ref-img").style.maxHeight = "100px";
        document.getElementById("edit-collection-item-ref-img").style.width = "auto";
    } else {
        document.getElementById("edit-collection-item-ref-img").style.width = "100%";
        document.getElementById("edit-collection-item-ref-img").style.maxHeight = "600px";
    }
}