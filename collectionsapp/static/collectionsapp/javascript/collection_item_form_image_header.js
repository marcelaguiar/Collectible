window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        document.getElementById("collection-item-ref-img").style.maxHeight = "100px";
    } else {
        // TODO: Replace arbitrary 900 with unset, without breaking transition
        document.getElementById("collection-item-ref-img").style.maxHeight = "900px";
    }
}