function refresh()
{
    //var iframe = document.getElementById('FrameID');
    //iframe.contentWindow.location.reload();
    //iframe.src = iframe.src;
    var loc = window.location;
    window.location = loc.protocol + '//' + loc.host + loc.pathname + loc.search;
}

//window.setInterval(refresh, 20000);
