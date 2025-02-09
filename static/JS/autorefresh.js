function refresh()
{
    var iframe = document.getElementById('FrameID');
    iframe.contentWindow.location.reload();
    //iframe.src = iframe.src;
}

window.setInterval(refresh, 2000);
