let activeIndex = 0;
var activeAudio;


/* DO WHEN CONTENT IS LOADED */
window.addEventListener('DOMContentLoaded', (event) => {
    var currTrackTimer = document.getElementById('currTrackTimer');
    let playListItems = document.querySelectorAll(".playlistItemContainer");

    /* ACTIVATE FIRST TRACK */
    var prevPos = localStorage.getItem(prevTrackHashKey + '_index') || 0; // store index
    var prevTime = localStorage.getItem(prevTrackHashKey + '_time') || 0; // store time
    if (prevPos < playListItems.length && playListItems.length > 0){
        activeIndex = prevPos;
        playListItems[activeIndex].scrollIntoView();
    }else{
        prevTime = 0
    }
    document.getElementById('playlistItemContainer-' + activeIndex).classList.add("active");
    document.getElementById('activeAudioSource').src = document.getElementById('file-url-' + activeIndex).innerHTML;
    document.getElementById('currTrackTitle').innerHTML = document.getElementById('file-title-' + activeIndex).innerHTML;
    activeAudio = document.getElementById("activeAudio");
    activeAudio.load();
    activeAudio.onloadedmetadata = function() {
            document.getElementById('currTrackDuration').innerHTML = formatMinutes(activeAudio.duration);
    }
    activeAudio.currentTime = prevTime;

    /* MAKE THE PLAYLIST ITEMS CLICKABLE AND FORMAT DURATION*/
    for (let i = 0; i < playListItems.length; i++){
        playListItems[i].addEventListener("click", handleItemClick);
        playListItems[i].children[3].innerHTML = formatMinutes(playListItems[i].children[3].innerHTML);
    }

    /* MAKE PROGRESS BAR ABLE TO SELECT TIME IN TRACK */
    /* NGINX SERVES FILES DIFFERENTLY THAN THE LOCAL DEV MODE, THERE ARE ISSUES WITH THIS IN LOCAL DEV BUT IN WORKS OVER NGINX */
    var progressbar = document.getElementById('progressBar');
    progressbar.addEventListener("click", function(event){
        var percent = event.offsetX / progressbar.offsetWidth;
        activeAudio.currentTime = percent * activeAudio.duration;
        var barProgress = document.getElementById("currentProgress");
        barProgress.style.width = percent*100 + "%";
    });
});


/* HANDLE PLAYLIST ITEM CLICK */
function handleItemClick(event) {
    var clickedIndex = event.target.getAttribute("data-index");
    if (clickedIndex == activeIndex ) {
        toggleActiveAudio();
    }else{
        loadNewAudio(clickedIndex);
    }
}


/* LOAD NEW ITEM AND PLAY IT */
function loadNewAudio(index){
    var player = document.getElementById('activeAudioSource');
    player.src = document.getElementById('file-url-' + index).innerHTML;
    document.getElementById('currTrackTitle').innerHTML = document.getElementById('file-title-' + index).innerHTML;
    activeAudio = document.getElementById("activeAudio");
    activeAudio.load();
    toggleActiveAudio();
    updateStylePlaylist(activeIndex,index);
    activeIndex = index;
    localStorage[prevTrackHashKey + '_index'] = index;
}


/* PAUSE IF PLAYING, PLAY IF PAUSED */
function toggleActiveAudio() {
    if (activeAudio.paused) {
        document.getElementById('playControl').style.display = 'none';
        document.getElementById('pauseControl').style.display = 'block';
        playlistItemPauseIcon(activeIndex);
        activeAudio.play();
    }else{
        document.getElementById('playControl').style.display = 'block';
        document.getElementById('pauseControl').style.display = 'none';
        playlistItemPlayIcon(activeIndex);
        activeAudio.pause();
    }
}


/* UPDATE TIME, PROGRESS BAR, CHECK IF ENDED */
function timeUpdateHandler() {
    var t = activeAudio.currentTime;
    localStorage[prevTrackHashKey + '_time'] = t;
    currTrackTimer.innerHTML = formatMinutes(t);
    var progress = (activeAudio.currentTime/activeAudio.duration)*100;
    document.getElementById("currentProgress").style.width = progress + "%";
    if (activeAudio.ended) {
        document.getElementById('playControl').style.display = 'block';
        document.getElementById('pauseControl').style.display = 'none';
        playlistItemPlayIcon(activeIndex);
        if (activeIndex < document.getElementById('playlistContainer').children.length-1) {
            var index = parseInt(activeIndex)+1;
            loadNewAudio(index);
        }
    }
 }


/* FORMAT TOTAL SECONDS INTO MM:SS  */
function formatMinutes(t){
    var min = parseInt(parseInt(t)/60);
    var sec = parseInt(t%60);
    if (sec < 10) {
        sec = "0"+sec;
    }
    if (min < 10) {
        min = "0"+min;
    }
    return min+":"+sec;
}


/* MOVE TO NEXT FILE */
function nextFile(){
    if (activeIndex <document.getElementById('playlistContainer').children.length-1) {
        var oldIndex = activeIndex;
        activeIndex++;
        updateStylePlaylist(oldIndex,activeIndex);
        loadNewAudio(activeIndex);
    }
}


/* MOVE TO PREVIOUS FILE */
function previousFile(){
    if (activeIndex>0) {
        var oldIndex = activeIndex;
        activeIndex--;
        updateStylePlaylist(oldIndex,activeIndex);
        loadNewAudio(activeIndex);
    }
}


/* INDEX CHANGE STYLE UPDATE */
function updateStylePlaylist(oldIndex,newIndex){
    document.getElementById('playlistItemContainer-'+oldIndex).classList.remove("active");
    playlistItemPlayIcon(oldIndex);
    document.getElementById('playlistItemContainer-'+newIndex).classList.add("active");
    playlistItemPauseIcon(newIndex);
}


/* PAUSE A PLAYING TRACK */
function playlistItemPauseIcon(index){
    let icon = document.getElementById('playlistItemIcon-'+index);
    icon.classList.remove("fa-play");
    icon.classList.add("fa-pause");
}


/* PLAY A PAUSED TRACK */
function playlistItemPlayIcon(index){
    let icon = document.getElementById('playlistItemIcon-'+index);
    icon.classList.remove("fa-pause");
    icon.classList.add("fa-play");
}