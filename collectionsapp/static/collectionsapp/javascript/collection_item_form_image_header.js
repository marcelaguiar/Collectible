window.onscroll = function() { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        document.getElementById("collection-item-ref-img").style.maxHeight = "100px";
    } else {
        document.getElementById("collection-item-ref-img").style.maxHeight = "600px";
    }
}