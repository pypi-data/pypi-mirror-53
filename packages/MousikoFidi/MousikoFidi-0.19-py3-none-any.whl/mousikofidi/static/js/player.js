/*
  MousikóFídi
  Copyright (C) 2019  Hristos N. Triantafillou

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

var audio = document.getElementById("audio");
var audioNowPlayingTextP = document.getElementById("now-playing");
var videoNowPlayingTextP = document.getElementById("video-now-playing");
var nowPlayingNumDiv = document.getElementById("now-playing-num");
var audioPlaybackEndedDiv = document.getElementById("audio-playback-ended");
var videoPlaybackEndedDiv = document.getElementById("video-playback-ended");
var videoNowPlayingNumDiv = document.getElementById("video-now-playing-num");
var pageTitle = document.getElementById("title");
var playArrows = document.getElementsByClassName("play-arrow");
var playingTitleSpan = document.getElementById("playing-title");
var videoPlayingTitleSpan = document.getElementById("video-playing-title");
var playlist = document.getElementById("playlist");
if (playlist)
    var tracks = playlist.getElementsByClassName("title");
var video = document.getElementById("video");
var videoArrows = document.getElementsByClassName("video-arrow");
var videoPlaylist = document.getElementById("video-playlist");
if (videoPlaylist) {
    var videoTracks = videoPlaylist.getElementsByClassName("video-title");
} else if (playlist) {
    var videoTracks = playlist.getElementsByClassName("video-title");
}
var prevBtn = document.getElementById("prev");
var nextBtn = document.getElementById("next");
var repeatBtn = document.getElementById("repeat");
var shuffleBtn = document.getElementById("shuffle");
var prevBtnMobile = document.getElementById("mobile-prev");
var nextBtnMobile = document.getElementById("mobile-next");
var repeatBtnMobile = document.getElementById("mobile-repeat");
var shuffleBtnMobile = document.getElementById("mobile-shuffle");
var randomOrderHolder = document.getElementById("randorder");
var videoPrevBtn = document.getElementById("vid-prev");
var videoNextBtn = document.getElementById("vid-next");
var videoRepeatBtn = document.getElementById("vid-repeat");
var videoShuffleBtn = document.getElementById("vid-shuffle");
var videoPrevBtnMobile = document.getElementById("mobile-vid-prev");
var videoNextBtnMobile = document.getElementById("mobile-vid-next");
var videoRepeatBtnMobile = document.getElementById("mobile-vid-repeat");
var videoShuffleBtnMobile = document.getElementById("mobile-vid-shuffle");
var videoRandomOrderHolder = document.getElementById("vid-randorder");
var params = new URLSearchParams(window.location.search);
var single = document.getElementById("single");
var singleLinkButton = document.getElementById("time-link");
var audioLinkButton = document.getElementById("audio-time-link");
var videoLinkButton = document.getElementById("video-time-link");
var iconsEnabled = document.getElementById("icons-enabled");
var theaterViewButton = document.getElementById("video-theater-view");
var audioFollowCheckbox = document.getElementById("follow-track");
var audioFollowCheckboxMobile = document.getElementById("mobile-follow-track");

function playAudio(targetArrow, dontPlay) {
    /*
      Play the selected track.
    */
    if (targetArrow) {
        var browse = targetArrow.getAttribute("data-browse");
    } else {
        return false;
    }
    var serve = browse.replace("browse", "serve");
    var siteName = pageTitle.getAttribute("data-sitename");
    var thisTrackNum = targetArrow.getAttribute("data-num");
    var title = targetArrow.getAttribute("data-title");
    var playingTextTitle = "Now Playing: " + title + " | " + siteName;
    var shuffle = shuffleBtn.getAttribute("data-stat");
    var shuffleMobile = shuffleBtnMobile.getAttribute("data-stat");
    var mobileHidden = window.getComputedStyle(document.getElementsByClassName("mobile-hide")[0])["display"] === "none";
    var followTrack;

    if (audio.src.endsWith(serve) !== true)
        audio.src = serve;

    if (typeof dontPlay === 'undefined')
        audio.play();

    nowPlayingNumDiv.setAttribute("data-nowplaying-num", thisTrackNum);

    if (mobileHidden === false) {
        followTrack = audioFollowCheckbox.checked === true;
    } else {
        followTrack = audioFollowCheckboxMobile.checked === true;
    }

    if (followTrack) {
        var scrollTarget = document.getElementById(targetArrow.id + "-target");
        scrollTarget.scrollIntoView({block: 'start', behavior: 'smooth'});
    }

    if ((shuffle === "on") || (shuffleMobile === "on")) {
        setRandomOrder("audio");
    }
}

function playAudioClickListener() {
    audioPlaybackEndedDiv.setAttribute("data-playback-ended", "false");
    playAudio(this);
}

function playVideo(targetArrow, dontPlay) {
    /*
      Play the selected track.
    */
    if (targetArrow) {
        var browse = targetArrow.getAttribute("data-browse");
    } else {
        return false;
    }
    var serve = browse.replace("browse", "serve");
    var shuffle = videoShuffleBtn.getAttribute("data-stat");
    var shuffleMobile = videoShuffleBtnMobile.getAttribute("data-stat");
    var thisTrackNum = targetArrow.getAttribute("data-num");

    if (typeof dontPlay === 'undefined') {
        video.src = serve;
        video.play();
    }
    videoNowPlayingNumDiv.setAttribute("data-nowplaying-num", thisTrackNum);
    video.scrollIntoView({block: 'start', behavior: 'smooth'});

    if ((shuffle === "on") || (shuffleMobile === "on")) {
        setRandomOrder("video");
    }
}

function playVideoClickListener() {
    videoPlaybackEndedDiv.setAttribute("data-playback-ended", "false");
    playVideo(this);
}

function randInt(max) {
    // Thank you MDN
    return Math.floor(Math.random() * max);
}

function setRandomOrder(trackType) {
    if (trackType === "audio") {
        var arrows = playArrows;
        var oldRandString = randomOrderHolder.getAttribute("data-randorder");
        var orderHolder = randomOrderHolder;

    } else if (trackType === "video") {
        var arrows = videoArrows;
        var oldRandString = videoRandomOrderHolder.getAttribute("data-randorder");
        var orderHolder = videoRandomOrderHolder;
    }

    var newRandArray = randomizeTrackOrder(arrows.length, trackType);
    var newRandString = randomStringFromArray(newRandArray);

    if (oldRandString === "none") {
        orderHolder.setAttribute("data-randorder", newRandString);

    } else if (oldRandString === newRandString) {
        while (oldRandString === newRandString) {
            var newArray = randomizeTrackOrder(arrows.length, trackType);
            newRandString = randomStringFromArray(newArray);
        }

    } else {
        orderHolder.setAttribute("data-randorder", newRandString);
    }
}

function endedTrackListener(_, trackType) {
    if (trackType === "audio") {
        var arrows = playArrows;
        var currentTrack = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
        var orderHolder = randomOrderHolder;
        var playbackEndedDiv = audioPlaybackEndedDiv;
        var playFn = playAudio;
        var repeatNormal = repeatBtn.getAttribute("data-stat");
        var repeatMobile = repeatBtnMobile.getAttribute("data-stat");
        var repeatOne = ((repeatNormal == "one") || (repeatMobile == "one"));
        var repeatAll = ((repeatNormal == "all") || (repeatMobile == "all"));
        var shuffleNormal = shuffleBtn.getAttribute("data-stat");
        var shuffleMobile = shuffleBtnMobile.getAttribute("data-stat");
        var shuffle = ((shuffleNormal == "on") || (shuffleMobile == "on"));

    } else if (trackType === "video") {
        var arrows = videoArrows;
        var currentTrack = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");
        var orderHolder = videoRandomOrderHolder;
        var playbackEndedDiv = videoPlaybackEndedDiv;
        var playFn = playVideo;
        var repeatNormal = videoRepeatBtn.getAttribute("data-stat");
        var repeatMobile = videoRepeatBtnMobile.getAttribute("data-stat");
        var repeat = ((repeatNormal == "on") || (repeatMobile == "on"));
        var shuffleNormal = videoShuffleBtn.getAttribute("data-stat");
        var shuffleMobile = videoShuffleBtnMobile.getAttribute("data-stat");
        var shuffle = ((shuffleNormal == "on") || (shuffleMobile == "on"));
    }

    var playbackEnded = (playbackEndedDiv.getAttribute("data-playback-ended") === "true");
    var trackCount = arrows.length - 1;

    if (repeatOne) {
        playFn(arrows[currentTrack]);

    } else {
        if (shuffle) {

            if (playbackEnded) {
                // console.log("Playback is ended...");
                return;

            } else {
                var randOrderString = orderHolder.getAttribute("data-randorder");
                var randOrderArray = randOrderString.split(",");
                var nextTrack = randOrderArray.shift();

                if ((randOrderArray != "") && (nextTrack !== 'undefined')) {
                    playFn(arrows[nextTrack]);

                    var newOrderString = randomStringFromArray(randOrderArray);
                    orderHolder.setAttribute("data-randorder", newOrderString);

                } else if ((repeatAll) && (nextTrack === 'undefined')) {
                    var newStartTrack = randInt(trackCount);

                    playFn(arrows[newStartTrack]);

                    setRandomOrder(trackType);

                } else {
                    var _play = playFn(arrows[nextTrack]);

                    if (repeatAll) {
                        // console.log("Shuffled playlist is empty and will be recalculated...");
                        setRandomOrder(trackType);

                        var _randOrderString = orderHolder.getAttribute("data-randorder");
                        var _randOrderArray = _randOrderString.split(",");

                        playFn(arrows[_randOrderArray[0]]);

                    } else {
                        // console.log("Shuffled playlist is empty, playback will stop...");
                        playbackEndedDiv.setAttribute("data-playback-ended", "true");
                    }
                }
            }

        } else if (shuffle === false) {
            if (currentTrack < trackCount) {
                currentTrack++;
                playFn(arrows[currentTrack]);

            } else if (repeatAll) {
                playFn(arrows[0]);

            } else if ((repeatOne === false) && repeatAll === false) {
                // console.log("Playback has ended.");
            }
        }
    }
}

function endedAudioListener() {
    endedTrackListener(this, "audio")
}

function endedVideoListener() {
    endedTrackListener(this, "video")
}

function skipTrack(target, mediaType) {
    var cmd = target.getAttribute("data-cmd");

    if (mediaType === "audio") {
        var arrows = playArrows;
        var currentTrack = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
        var orderHolder = randomOrderHolder;
        var playFn = playAudio;
        var shuffle = shuffleBtn.getAttribute("data-stat");
        var shuffleMobile = shuffleBtnMobile.getAttribute("data-stat");
        var t = tracks;

    } else if (mediaType === "video") {
        var arrows = videoArrows;
        var currentTrack = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");
        var orderHolder = videoRandomOrderHolder;
        var playFn = playVideo;
        var shuffle = videoShuffleBtn.getAttribute("data-stat");
        var shuffleMobile = videoShuffleBtnMobile.getAttribute("data-stat");
        var t = videoTracks;

    }

    var trackTotal = t.length - 1;

    if ((shuffle === "on") || (shuffleMobile === "on")) {
        var randOrderString = orderHolder.getAttribute("data-randorder");
        var randOrderArray = randOrderString.split(",");

        if (randOrderArray.length > 0) {
            var nextTrack = randOrderArray.shift();
            var nt = arrows[nextTrack]

            if (typeof(nt) === "undefined") {
                var newStartTrack = randInt(t.length);
                playFn(arrows[newStartTrack]);
                setRandomOrder(mediaType);

            } else {
                playFn(nt);
                var newOrderString = randomStringFromArray(randOrderArray);
                orderHolder.setAttribute("data-randorder", newOrderString);
            }

        } else if (repeat === "all") {
            var newStartTrack = randInt(t.length);
            playFn(arrows[newStartTrack]);
            setRandomOrder(mediaType);
        }

    } else if (shuffle === "off") {

        if (cmd === "fwd") {
            if (currentTrack < trackTotal) {
                currentTrack++;
                playFn(arrows[currentTrack]);
            } else {
                playFn(arrows[0]);
            }

        } else if (cmd === "prev") {
            if (currentTrack > 0) {
                currentTrack--;
                playFn(arrows[currentTrack]);
            } else {
                playFn(arrows[trackTotal]);
            }
        }
    }
}

function skipAudioListener() {
    skipTrack(this, "audio");
}

function skipVideoListener() {
    skipTrack(this, "video");
}

function toggleRepeat(target) {
    var stat = target.getAttribute("data-stat");
    if (stat === "off") {
        target.setAttribute("data-stat", "one");

        target.textContent = "Repeat One ";

        if (iconsEnabled) {
            target.appendChild(document.createElement("i"));
            target.childNodes[1].classList.add("fas", "fa-redo");

            target.style.paddingTop = "9px";
            target.style.paddingRight = "15px";
            target.style.paddingBottom = "9px";
            target.style.paddingLeft = "15px";
        }

    } else if (stat === "one") {
        target.setAttribute("data-stat", "all");
        target.textContent = "Repeat All";

        if (iconsEnabled) {
            target.appendChild(document.createElement("span"));
            target.childNodes[1].classList.add("fa-stack");
            target.childNodes[1].appendChild(document.createElement("i"));
            target.childNodes[1].appendChild(document.createElement("i"));

            target.childNodes[1].childNodes[0].classList.add("fas", "fa-redo", "fa-stack-1x");
            target.childNodes[1].childNodes[1].classList.add("fas", "fa-infinity", "fa-stack-1x");
            target.childNodes[1].childNodes[1].style.fontSize = "0.4em";

            target.style.marginBottom = "0";
            target.style.paddingTop = "5px";
            target.style.paddingRight = "5px";
            target.style.paddingBottom = "5px";
            target.style.paddingLeft = "15px";
        }

    } else if (stat === "all") {
        target.setAttribute("data-stat", "off");
        target.textContent = "No Repeat";

        if (iconsEnabled) {
            target.appendChild(document.createElement("span"));
            target.childNodes[1].classList.add("fa-stack");
            target.childNodes[1].appendChild(document.createElement("i"));
            target.childNodes[1].appendChild(document.createElement("i"));

            target.childNodes[1].childNodes[0].classList.add("fas", "fa-redo", "fa-stack-1x");
            target.childNodes[1].childNodes[1].classList.add("fas", "fa-slash", "fa-stack-1x");

            target.style.marginBottom = "0";
            target.style.paddingTop = "5px";
            target.style.paddingRight = "5px";
            target.style.paddingBottom = "5px";
            target.style.paddingLeft = "15px";
        }
    }
}

function toggleRepeatListener() {
    toggleRepeat(this);
}

function randomizeTrackOrder(totalCount, trackType) {

    if (trackType === "audio") {
        var nowPlayingTrackNum = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
    } else if (trackType === "video") {
        var nowPlayingTrackNum = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");
    }

    var randCount = 0;
    var trackList = [];

    while (trackList.length < totalCount - 1) {
        var rand = randInt(totalCount);

        while (rand == nowPlayingTrackNum)
            rand = randInt(totalCount);

        if (trackList.indexOf(rand) === -1)
            trackList.push(rand);
    }

    return trackList;
}

function randomStringFromArray(array) {
    if (array === "none")
        return
    var randString = "";
    for (c = 0; c < array.length; c++) {
        randString += array[c];
        if (c < array.length - 1) {
            randString += ",";
        }
    }
    return randString;
}

function toggleShuffle(target, trackType) {
    var shuffle = target.getAttribute("data-stat");
    if (shuffle === "off") {
        setRandomOrder(trackType);
        target.setAttribute("data-stat", "on");
        target.textContent = "Shuffle On ";

        if (iconsEnabled) {
            target.appendChild(document.createElement("i"));
            target.childNodes[1].classList.add("fas", "fa-random");

            target.style.paddingTop = "9px";
            target.style.paddingRight = "15px";
            target.style.paddingBottom = "9px";
            target.style.paddingLeft = "15px";
        }

    } else if (shuffle === "on") {
        target.setAttribute("data-stat", "off");
        target.textContent = "Shuffle Off";

        if (iconsEnabled) {
            target.appendChild(document.createElement("span"));
            target.childNodes[1].classList.add("fa-stack");
            target.childNodes[1].appendChild(document.createElement("i"));
            target.childNodes[1].appendChild(document.createElement("i"));

            target.childNodes[1].childNodes[0].classList.add("fas", "fa-random", "fa-stack-1x");
            target.childNodes[1].childNodes[1].classList.add("fas", "fa-slash", "fa-stack-1x");

            target.style.marginBottom = "0";
            target.style.paddingTop = "5px";
            target.style.paddingRight = "5px";
            target.style.paddingBottom = "5px";
            target.style.paddingLeft = "15px";
        }

    }
}

function toggleShuffleAudioListener() {
    toggleShuffle(this, "audio");
}

function toggleShuffleVideoListener() {
    toggleShuffle(this, "video");
}

function paused(_, event, trackType) {
    if (trackType === "audio") {
        var nowPlayingTextP = audioNowPlayingTextP;
        var nowPlayingTrackNum = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
        var playingText = playArrows[nowPlayingTrackNum].getAttribute("data-title");
        var siteName = pageTitle.getAttribute("data-sitename");

    } else if (trackType === "video") {
        var nowPlayingTextP = videoNowPlayingTextP;
        var nowPlayingTrackNum = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");
        var playingText = videoArrows[nowPlayingTrackNum].getAttribute("data-title");
    }

    if (event === "playing") {
        if (trackType === "audio")
            pageTitle.textContent = "Now Playing: " + playingText + " | " + siteName;

        nowPlayingTextP.textContent = "Now Playing: ";

        // The inner span gets wiped out when the outer p's text is set.  Recreate and set it.
        nowPlayingTextP.appendChild(document.createElement("span"));
        nowPlayingTextP.childNodes[1].onclick = function() {
            var scrollTarget = document.getElementById(playArrows[nowPlayingTrackNum].id + "-target");
            scrollTarget.scrollIntoView({block: 'start', behavior: 'smooth'});
        };
        nowPlayingTextP.childNodes[1].style.fontWeight = "bold";
        nowPlayingTextP.childNodes[1].textContent = playingText;

    } else if (event === "paused") {
        if (trackType === "audio")
            pageTitle.textContent = "Paused: " + playingText + " | " + siteName;

        nowPlayingTextP.textContent = "Paused: ";

        // The inner span gets wiped out when the outer p's text is set.  Recreate and set it.
        nowPlayingTextP.appendChild(document.createElement("span"));
        nowPlayingTextP.childNodes[1].onclick = function() {
            var scrollTarget = document.getElementById(playArrows[nowPlayingTrackNum].id + "-target");
            scrollTarget.scrollIntoView({block: 'start', behavior: 'smooth'});
        };
        nowPlayingTextP.childNodes[1].style.fontWeight = "bold";
        nowPlayingTextP.childNodes[1].textContent = playingText;
    }
}

function playingAudioHandler() {
    paused(this, "playing", "audio");
}

function pausedAudioHandler() {
    paused(this, "paused", "audio");
}

function playingVideoHandler() {
    paused(this, "playing", "video");
}

function pausedVideoHandler() {
    paused(this, "paused", "video");
}

function giveLink(playerType) {
    /*
      Create a link to the current track at the current time,
      and put it into the user's clipboard.
     */
    var arrows;
    var nowPlayingNum;
    var pre;
    var _player;

    if (playerType === "audio") {
        _player = audio;
    } else if (playerType === "video") {
        _player = video;
    } else if (playerType === "single") {
        _player = single;
    }

    var urlToGive = window.location.protocol
        + "//"
        + window.location.host
        // + "/"
        + window.location.pathname
        + "?t="
        + Math.floor(_player.currentTime);

    if (playerType === "audio") {
        arrows = playArrows;
        nowPlayingNum = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
        pre = "&a="

    } else if (playerType === "video") {
        arrows = videoArrows;
        nowPlayingNum = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");
        pre = "&v="
    }

    if (arrows) {
        var slug = arrows[nowPlayingNum].getAttribute("id");
        urlToGive += pre + slug;
    }

    // Link direct to the player for videos
    if (playerType === "video") {
        urlToGive += "#videoplayer";
    }

    // Create an ad hoc text area
    var textArea = document.createElement("textarea");

    // Set the value of the ad hoc text area to the URL we are giving
    textArea.value = urlToGive;

    // Append the ad hoc text area to the document's body
    document.body.appendChild(textArea);

    // Select the text (e.g. highlight, mark it)
    textArea.select();

    // Copy it to the user's clipboard
    document.execCommand("copy");

    // Clean up the ad hoc text area
    document.body.removeChild(textArea);

    return urlToGive;
}

function singleLinkListener() {
    giveLink("single");
}

function audioLinkListener() {
    giveLink("audio");
}

function videoLinkListener() {
    giveLink("video");
}

function seekTrack() {
    var audioTrack = params.get("a");
    var videoTrack = params.get("v");
    var time = params.get("t");

    if ((audioTrack === null) && (videoTrack === null)) {
        // This is a single track on a file detail page.
        single.currentTime = time;
        single.autoplay = true;

    } else {
        // This is a playlist page, or directory detail, with several tracks listed.

        if (audioTrack) {
            playAudio(playArrows.namedItem(audioTrack));
            audio.currentTime = time;
            audio.autoplay = true;
        }

        if (videoTrack) {
            playVideo(videoArrows.namedItem(videoTrack));
            video.currentTime = time;
            video.autoplay = true;
        }
    }
}

function toggletheaterView(targetButton) {
    var body = document.getElementsByTagName("body")[0];
    // Don't try to set the body width for the NES or Terminal themes;
    // only the water themes limit the body width enough to make this do anything.
    var setBody = (
        (document.getElementById("current-theme").getAttribute("data-theme") === "/css/water/light.standalone")
            || (document.getElementById("current-theme").getAttribute("data-theme") === "/css/water/dark.standalone")
    );
    var tvStat = targetButton.getAttribute("data-stat") === "on";

    if (tvStat) {
        // console.log("Disabling Theater View!");
        targetButton.setAttribute("data-stat", "off");
        targetButton.textContent = "Theater View: Off";

        if (setBody)
            body.style.maxWidth = "800px";

        if (iconsEnabled) {
            targetButton.appendChild(document.createElement("span"));
            targetButton.childNodes[1].classList.add("fa-stack");
            targetButton.childNodes[1].appendChild(document.createElement("i"));
            targetButton.childNodes[1].appendChild(document.createElement("i"));

            targetButton.childNodes[1].childNodes[0].classList.add("fas", "fa-theater-masks", "fa-stack-1x");
            targetButton.childNodes[1].childNodes[1].classList.add("fas", "fa-slash", "fa-stack-1x");

            targetButton.style.marginBottom = "0";
            targetButton.style.paddingTop = "5px";
            targetButton.style.paddingRight = "5px";
            targetButton.style.paddingBottom = "5px";
            targetButton.style.paddingLeft = "15px";
        }

    } else {
        // console.log("Enabling Theater View!");
        targetButton.setAttribute("data-stat", "on");
        targetButton.textContent = "Theater View: On ";

        if (setBody)
            body.style.maxWidth = "100%";

        if (iconsEnabled) {
            targetButton.appendChild(document.createElement("i"));
            targetButton.childNodes[1].classList.add("fas", "fa-theater-masks");

            targetButton.style.paddingTop = "9px";
            targetButton.style.paddingRight = "15px";
            targetButton.style.paddingBottom = "9px";
            targetButton.style.paddingLeft = "15px";
        }
    }
    window.location.href = "#videoplayer";
}

function theaterViewListener() {
    toggletheaterView(this);
}


function setUp() {
    /*
      MousikóFídi playlist player main entry point.
    */
    var currentTrack = 0;
    if (nowPlayingNumDiv)
        var nowPlayingTrackNum = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
    var siteName = pageTitle.getAttribute("data-sitename");
    if (playArrows.length > 0) {
        var playingText = playArrows[0].getAttribute("data-title");
        var playingTextTitle = "Paused: " + playingText + " | " + siteName;
    }

    if (tracks) {
        // Add click listeners to all play buttons
        for (c = 0; c < playArrows.length; c++) {
            var arrow = playArrows.item(c);
            arrow.addEventListener("click", playAudioClickListener);
            arrow.setAttribute("data-num", c);
        }
    }

    if (audio) {
        // Load up the first track
        audio.src = playArrows[currentTrack].getAttribute("data-browse").replace("browse", "serve");
        playingTitleSpan.onclick = function() {
            var scrollTarget = document.getElementById(playArrows[currentTrack].id + "-target");
            scrollTarget.scrollIntoView({block: 'start', behavior: 'smooth'});
        };
        playingTitleSpan.textContent = playingText;
        title.textContent = playingTextTitle;

        // Finally, add the ended listener to continue playback
        audio.addEventListener('ended', endedAudioListener);
        audio.addEventListener("playing", playingAudioHandler);
        audio.addEventListener("pause", pausedAudioHandler);

        // Set listeners on player control buttons
        prevBtn.addEventListener("click", skipAudioListener);
        nextBtn.addEventListener("click", skipAudioListener);
        repeatBtn.addEventListener("click", toggleRepeatListener);
        shuffleBtn.addEventListener("click", toggleShuffleAudioListener);
        prevBtnMobile.addEventListener("click", skipAudioListener);
        nextBtnMobile.addEventListener("click", skipAudioListener);
        repeatBtnMobile.addEventListener("click", toggleRepeatListener);
        shuffleBtnMobile.addEventListener("click", toggleShuffleAudioListener);
    }

    if (videoTracks) {
        // Now, do videos if there are any: add click listeners to all play buttons
        for (c = 0; c < videoArrows.length; c++) {
            var varrow = videoArrows.item(c);
            varrow.addEventListener("click", playVideoClickListener);
            varrow.setAttribute("data-num", c);
        }
    }

    if (videoArrows.length > 0) {
        var videoPlayingText = videoArrows[0].getAttribute("data-title");
    }

    if (video) {
        video.src = videoArrows[currentTrack].getAttribute("data-browse").replace("browse", "serve");
        videoPlayingTitleSpan.textContent = videoPlayingText;
        video.addEventListener('ended', endedVideoListener);
        video.addEventListener("playing", playingVideoHandler);
        video.addEventListener("pause", pausedVideoHandler);

        // Set listeners on player control buttons
        videoPrevBtn.addEventListener("click", skipVideoListener);
        videoNextBtn.addEventListener("click", skipVideoListener);
        videoRepeatBtn.addEventListener("click", toggleRepeatListener);
        videoShuffleBtn.addEventListener("click", toggleShuffleVideoListener);
        videoPrevBtnMobile.addEventListener("click", skipVideoListener);
        videoNextBtnMobile.addEventListener("click", skipVideoListener);
        videoRepeatBtnMobile.addEventListener("click", toggleRepeatListener);
        videoShuffleBtnMobile.addEventListener("click", toggleShuffleVideoListener);
    }

    if (singleLinkButton)
        singleLinkButton.addEventListener("click", singleLinkListener);

    if (audioLinkButton)
        audioLinkButton.addEventListener("click", audioLinkListener);

    if (videoLinkButton)
        videoLinkButton.addEventListener("click", videoLinkListener);

    if (params.has("t"))
        seekTrack();

    if (theaterViewButton)
        theaterViewButton.addEventListener("click", theaterViewListener);

}

window.onload = setUp();
