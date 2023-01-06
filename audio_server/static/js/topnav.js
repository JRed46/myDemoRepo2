function narrowTopnav(){
    document.getElementById("webname").style.display = "none";
}

function largeTopnav(){
    document.getElementById("webname").style.display = "flex";
}


function checkNarrowTopnav(){
    var topnav = document.getElementById("topnav");
    var widthThreshold = localStorage['widthThreshold'];
    var delta = topnav.offsetWidth - widthThreshold;
    if (delta <0 ){
        narrowTopnav();
    }else{
        largeTopnav();
    }
}


window.addEventListener("load", function() {
    var sum = document.getElementById('logoAndTitleContainer').offsetWidth 
        + document.getElementById('listen').offsetWidth 
        + document.getElementById('upload').offsetWidth
        + document.getElementById('chatbot').offsetWidth
        + document.getElementById('auth').offsetWidth
        + 40;
    try{ //if user is admin has extra icon
        sum = sum + document.getElementById('admin').offsetWidth + 10;
    }catch{}
    localStorage['widthThreshold'] = sum ;
    checkNarrowTopnav();
});

window.addEventListener('resize', checkNarrowTopnav);