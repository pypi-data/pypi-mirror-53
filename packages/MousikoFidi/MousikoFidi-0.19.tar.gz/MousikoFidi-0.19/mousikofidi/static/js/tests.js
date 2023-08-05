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

var failed = document.getElementById("__failed");
var passed = document.getElementById("__passed");
var results = document.getElementById("__results");

var audioRandomOrderHolder = document.getElementById("randorder");
var videoRandomOrderHolder = document.getElementById("vid-randorder");

var audioArrows = document.getElementsByClassName("play-arrow");
var audioShuffleButton = document.getElementById("shuffle");
var audioShuffleButtonMobile = document.getElementById("mobile-shuffle");
var playlist = document.getElementById("playlist");
var audioTracks = playlist.getElementsByClassName("title");

var videoArrows = document.getElementsByClassName("video-arrow");
var videoShuffleButton = document.getElementById("vid-shuffle");
var videoShuffleButtonMobile = document.getElementById("mobile-vid-shuffle");
var videoPlaylist = document.getElementById("video-playlist");
if (videoPlaylist) {
    var videoTracks = videoPlaylist.getElementsByClassName("video-title");
} else if (playlist) {
    var videoTracks = playlist.getElementsByClassName("video-title");
}

var repeatButton = document.getElementById("repeat");

var nowPlayingAudioNum = nowPlayingNumDiv.getAttribute("data-nowplaying-num");
var nowPlayingVideoNum = nowPlayingNumDiv.getAttribute("data-nowplaying-num");

function testSetRandomOrderAudio() {
    console.log("Begin: testSetRandomOrderAudio()");

    var trackCount = audioArrows.length;
    var startOrder = audioRandomOrderHolder.getAttribute("data-randorder")
    setRandomOrder("audio");

    if (startOrder != "none") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    var randOrder1 = audioRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen1 = randOrder1.split(",").length + 1;

    setRandomOrder("audio");

    var randOrder2 = audioRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen2 = randOrder2.split(",").length + 1;

    var n1_1 = Number(randOrder1.split(",")[0])
    var n1_2 = Number(randOrder1.split(",")[1])

    var n2_1 = Number(randOrder2.split(",")[0])
    var n2_2 = Number(randOrder2.split(",")[1])

    console.log("trackCount: " + trackCount);

    console.log("startOrder: " + startOrder);

    console.log("randOrder1: " + randOrder1);
    console.log("randLen1: " + randLen1);
    console.log("randOrder2: " + randOrder2);
    console.log("randLen2: " + randLen2);

    console.log("typeof(randOrder1): " + typeof(randOrder1));
    console.log("typeof(randOrder2): " + typeof(randOrder2));

    console.log("n1_1: " + n1_1);
    console.log("n1_2: " + n1_2);
    console.log("n2_1: " + n2_1);
    console.log("n2_2: " + n2_2);

    console.log("typeof n1_1: " + typeof n1_1);
    console.log("typeof n1_2: " + typeof n1_2);
    console.log("typeof n2_1: " + typeof n2_1);
    console.log("typeof n2_2: " + typeof n2_2);

    if (randLen1 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen1 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (randLen2 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen2 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof(randOrder1) != "string") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof(randOrder2) != "string") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof n1_1 != "number") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof n1_2 != "number") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof n2_1 != "number") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof n2_2 != "number") {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (randOrder1 === randOrder2) {
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    console.log("End: testSetRandomOrderAudio()");
    return true;
}

function testSetRandomOrderAudioNotZeroStart() {
    console.log("Begin: testSetRandomOrderAudioNotZeroStart()");

    var trackCount = audioArrows.length;
    var startOrder = audioRandomOrderHolder.getAttribute("data-randorder")

    var newStart = randInt(trackCount);

    while (newStart === 0)
        newStart = randInt(trackCount);

    nowPlayingNumDiv.setAttribute("data-nowplaying-num", newStart);
    setRandomOrder("audio");

    var randOrder1 = audioRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen1 = randOrder1.split(",").length + 1;

    setRandomOrder("audio");

    var randOrder2 = audioRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen2 = randOrder2.split(",").length + 1;

    var n1_1 = Number(randOrder1.split(",")[0])
    var n1_2 = Number(randOrder1.split(",")[1])

    var n2_1 = Number(randOrder2.split(",")[0])
    var n2_2 = Number(randOrder2.split(",")[1])

    console.log("trackCount: " + trackCount);

    console.log("startOrder: " + startOrder);

    console.log("newStart: " + newStart);

    console.log("randOrder1: " + randOrder1);
    console.log("randLen1: " + randLen1);
    console.log("randOrder2: " + randOrder2);
    console.log("randLen2: " + randLen2);

    console.log("typeof(randOrder1): " + typeof(randOrder1));
    console.log("typeof(randOrder2): " + typeof(randOrder2));

    console.log("n1_1: " + n1_1);
    console.log("n1_2: " + n1_2);
    console.log("n2_1: " + n2_1);
    console.log("n2_2: " + n2_2);

    console.log("typeof n1_1: " + typeof n1_1);
    console.log("typeof n1_2: " + typeof n1_2);
    console.log("typeof n2_1: " + typeof n2_1);
    console.log("typeof n2_2: " + typeof n2_2);

    if (randLen1 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen1 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (randLen2 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen2 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (typeof(randOrder1) != "string") {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (typeof(randOrder2) != "string") {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (typeof n1_1 != "number") {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (typeof n1_2 != "number") {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (typeof n2_1 != "number") {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (typeof n2_2 != "number") {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    if (randOrder1 === randOrder2) {
        console.log("End: testSetRandomOrderAudioNotZeroStart()");
        return false;
    }

    console.log("End: testSetRandomOrderAudioNotZeroStart()");
    return true;
}

function testSetRandomOrderVideo() {
    console.log("Begin: testSetRandomOrderVideo()");

    var trackCount = videoArrows.length;
    var startOrder = videoRandomOrderHolder.getAttribute("data-randorder")
    setRandomOrder("video");

    if (startOrder != "none") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    var randOrder1 = videoRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen1 = randOrder1.split(",").length + 1;

    setRandomOrder("video");

    var randOrder2 = videoRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen2 = randOrder2.split(",").length + 1;

    console.log("trackCount: " + trackCount);

    console.log("startOrder: " + startOrder);

    console.log("randOrder1: " + randOrder1);
    console.log("randLen1: " + randLen1);
    console.log("randOrder2: " + randOrder2);
    console.log("randLen2: " + randLen2);

    console.log("typeof(randOrder1): " + typeof(randOrder1));
    console.log("typeof(randOrder2): " + typeof(randOrder2));

    console.log("n1_1: " + n1_1);
    console.log("n1_2: " + n1_2);
    console.log("n2_1: " + n2_1);
    console.log("n2_2: " + n2_2);

    console.log("typeof n1_1: " + typeof n1_1);
    console.log("typeof n1_2: " + typeof n1_2);
    console.log("typeof n2_1: " + typeof n2_1);
    console.log("typeof n2_2: " + typeof n2_2);

    if (randLen1 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen1 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (randLen2 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen2 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof(randOrder1) != "string") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    if (typeof(randOrder2) != "string") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    var n1_1 = Number(randOrder1.split(",")[0])
    var n1_2 = Number(randOrder1.split(",")[1])

    var n2_1 = Number(randOrder2.split(",")[0])
    var n2_2 = Number(randOrder2.split(",")[1])

    if (typeof n1_1 != "number") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    if (typeof n1_2 != "number") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    if (typeof n2_1 != "number") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    if (typeof n2_2 != "number") {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    if (randOrder1 === randOrder2) {
        console.log("End: testSetRandomOrderVideo()");
        return false;
    }

    console.log("End: testSetRandomOrderVideo()");
    return true;
}

function testSetRandomOrderVideoNotZeroStart() {
    console.log("Begin: testSetRandomOrderVideoNotZeroStart()");

    var trackCount = videoArrows.length;
    var startOrder = videoRandomOrderHolder.getAttribute("data-randorder")
    setRandomOrder("video");

    var newStart = randInt(trackCount);

    while (newStart === 0)
        newStart = randInt(trackCount);

    videoNowPlayingNumDiv.setAttribute("data-nowplaying-num", newStart);
    setRandomOrder("audio");

    var randOrder1 = videoRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen1 = randOrder1.split(",").length + 1;

    setRandomOrder("video");

    var randOrder2 = videoRandomOrderHolder.getAttribute("data-randorder")
    // +1 below because the start track isn't in the order
    var randLen2 = randOrder2.split(",").length + 1;

    console.log("trackCount: " + trackCount);

    console.log("startOrder: " + startOrder);

    console.log("randOrder1: " + randOrder1);
    console.log("randLen1: " + randLen1);
    console.log("randOrder2: " + randOrder2);
    console.log("randLen2: " + randLen2);

    console.log("typeof(randOrder1): " + typeof(randOrder1));
    console.log("typeof(randOrder2): " + typeof(randOrder2));

    console.log("n1_1: " + n1_1);
    console.log("n1_2: " + n1_2);
    console.log("n2_1: " + n2_1);
    console.log("n2_2: " + n2_2);

    console.log("typeof n1_1: " + typeof n1_1);
    console.log("typeof n1_2: " + typeof n1_2);
    console.log("typeof n2_1: " + typeof n2_1);
    console.log("typeof n2_2: " + typeof n2_2);

    if (randLen1 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen1 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (randLen2 !== trackCount) {
        console.log("TEST FAILED");
        console.log("randLen2 did not equal trackCount!!");
        console.log("End: testSetRandomOrderAudio()");
        return false;
    }

    if (typeof(randOrder1) != "string") {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    if (typeof(randOrder2) != "string") {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    var n1_1 = Number(randOrder1.split(",")[0])
    var n1_2 = Number(randOrder1.split(",")[1])

    var n2_1 = Number(randOrder2.split(",")[0])
    var n2_2 = Number(randOrder2.split(",")[1])

    if (typeof n1_1 != "number") {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    if (typeof n1_2 != "number") {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    if (typeof n2_1 != "number") {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    if (typeof n2_2 != "number") {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    if (randOrder1 === randOrder2) {
        console.log("End: testSetRandomOrderVideoNotZeroStart()");
        return false;
    }

    console.log("End: testSetRandomOrderVideoNotZeroStart()");
    return true;
}

function testTogggleRepeat() {
    console.log("Begin: testEndedTrackListenerVideo()");

    var repeatValue1 = repeatButton.getAttribute("data-stat");

    toggleRepeat(repeatButton);

    var repeatValue2 = repeatButton.getAttribute("data-stat");

    toggleRepeat(repeatButton);

    var repeatValue3 = repeatButton.getAttribute("data-stat");

    toggleRepeat(repeatButton);

    var repeatValue4 = repeatButton.getAttribute("data-stat");

    console.log("repeatValue1: " + repeatValue1);
    console.log("repeatValue2: " + repeatValue2);
    console.log("repeatValue3: " + repeatValue3);
    console.log("repeatValue4: " + repeatValue4);

    if (repeatValue1 != "off") {
        console.log("End: testEndedTrackListenerVideo()");
        return false;
    }

    if (repeatValue2 != "one") {
        console.log("End: testEndedTrackListenerVideo()");
        return false;
    }

    if (repeatValue3 != "all") {
        console.log("End: testEndedTrackListenerVideo()");
        return false;
    }

    if (repeatValue4 != "off") {
        console.log("End: testEndedTrackListenerVideo()");
        return false;
    }

    console.log("End: testEndedTrackListenerVideo()");
    return true;
}

function testRandomizeTrackOrderAudio() {
    console.log("Begin: testRandomizeTrackOrderAudio()");

    var list1 = randomizeTrackOrder(audioTracks.length, "audio");
    var list2 = randomizeTrackOrder(audioTracks.length, "audio");

    if (list1 == list2) {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if ((list1.constructor != Array) && (typeof list1 != "object")) {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if ((list2.constructor != Array) && (typeof list2 != "object")) {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    console.log("list1: " + list1);
    console.log("list2: " + list2);

    console.log("list1.constructor: " + list1.constructor);
    console.log("list2.constructor: " + list2.constructor);

    console.log("typeof list1: " + typeof list1);
    console.log("typeof list2: " + typeof list2);

    console.log("End: testRandomizeTrackOrderAudio()");
    return true;
}

function testRandomizeTrackOrderVideo() {
    console.log("Begin: testRandomizeTrackOrderVideo()");

    var list1 = randomizeTrackOrder(videoTracks.length, "video");
    var list2 = randomizeTrackOrder(videoTracks.length, "video");

    if (list1 == list2) {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if ((list1.constructor != Array) && (typeof list1 != "object")) {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if ((list2.constructor != Array) && (typeof list2 != "object")) {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if (typeof list1[0] != "number") {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if (typeof list1[2] != "number") {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if (typeof list2[1] != "number") {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    if (typeof list2[2] != "number") {
        console.log("End: testRandomizeTrackOrderAudio()");
        return false;
    }

    console.log("list1: " + list1);
    console.log("list2: " + list2);

    console.log("list1.constructor: " + list1.constructor);
    console.log("list2.constructor: " + list2.constructor);

    console.log("typeof list1: " + typeof list1);
    console.log("typeof list2: " + typeof list2);

    console.log("typeof list1[1]: " + typeof list1[1]);
    console.log("typeof list2[1]: " + typeof list2[1]);

    console.log("typeof list1[2]: " + typeof list1[2]);
    console.log("typeof list2[2] " + typeof list2[2]);

    console.log("End: testRandomizeTrackOrderVideo()");
    return true;
}

function testRandomStringFromArray() {
    console.log("Begin: testRandomStringFromArray()");

    var list1 = randomizeTrackOrder(videoTracks.length, "video");
    var list2 = randomizeTrackOrder(videoTracks.length, "video");

    var str1 = randomStringFromArray(list1);
    var str2 = randomStringFromArray(list2);

    if (typeof str1 != "string") {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    if (typeof Number(str1.split(",")[0]) != "number") {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    if (typeof Number(str1.split(",")[1]) != "number") {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    if (typeof str2 != "string") {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    if (typeof Number(str2.split(",")[0]) != "number") {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    if (typeof Number(str2.split(",")[1]) != "number") {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    if (str1 === str2) {
        console.log("End: testRandomStringFromArray()");
        return false;
    }

    console.log("list1: " + list1);
    console.log("list2: " + list2);

    console.log("str1: " + str1);
    console.log("str2: " + str2);

    console.log("typeof str1: " + typeof str1);
    console.log("typeof str2: " + typeof str2);

    console.log("typeof Number(str1.split(\",\")[0]): " + typeof Number(str1.split(",")[0]));
    console.log("typeof Number(str1.split(\",\")[1]): " + typeof Number(str1.split(",")[1]));

    console.log("typeof Number(str2.split(\",\")[0]): " + typeof Number(str2.split(",")[0]));
    console.log("typeof Number(str2.split(\",\")[1]): " + typeof Number(str2.split(",")[1]));

    console.log("End: testRandomStringFromArray()");
    return true;
}

function testToggleShuffleAudio() {
    console.log("Begin: testToggleShuffleAudio()");

    var rand1 = audioRandomOrderHolder.getAttribute("data-randorder");
    var stat1 = audioShuffleButton.getAttribute("data-stat");

    toggleShuffle(audioShuffleButton, "audio");

    var rand2 = audioRandomOrderHolder.getAttribute("data-randorder");
    var stat2 = audioShuffleButton.getAttribute("data-stat");

    toggleShuffle(audioShuffleButton, "audio");

    var stat3 = audioShuffleButton.getAttribute("data-stat");

    toggleShuffle(audioShuffleButton, "audio");

    var rand3 = audioRandomOrderHolder.getAttribute("data-randorder");

    if (stat1 != "off") {
        console.log("End: testToggleShuffleAudio()");
        return false;
    }

    if (stat2 != "on") {
        console.log("End: testToggleShuffleAudio()");
        return false;
    }

    if (stat3 != "off") {
        console.log("End: testToggleShuffleAudio()");
        return false;
    }

    if ((rand1 === rand2) || (rand1 === rand3) || (rand2 === rand3)) {
        console.log("End: testToggleShuffleAudio()");
        return false;
    }

    console.log("rand1: " + rand1);
    console.log("rand2: " + rand2);
    console.log("rand3: " + rand3);

    console.log("stat1: " + stat1);
    console.log("stat2: " + stat2);
    console.log("stat3: " + stat3);

    console.log("End: testToggleShuffleAudio()");
    return true;
}

function testToggleShuffleAudioMobile() {
    console.log("Begin: testToggleShuffleAudioMobile()");

    var rand1 = audioRandomOrderHolder.getAttribute("data-randorder");
    var stat1 = audioShuffleButtonMobile.getAttribute("data-stat");

    toggleShuffle(audioShuffleButtonMobile, "audio");

    var rand2 = audioRandomOrderHolder.getAttribute("data-randorder");
    var stat2 = audioShuffleButtonMobile.getAttribute("data-stat");

    toggleShuffle(audioShuffleButtonMobile, "audio");

    var stat3 = audioShuffleButtonMobile.getAttribute("data-stat");

    toggleShuffle(audioShuffleButtonMobile, "audio");

    var rand3 = audioRandomOrderHolder.getAttribute("data-randorder");

    if (stat1 != "off") {
        console.log("TEST FAILED");
        console.log("stat1 did not equal 'off'!!");
        console.log("End: testToggleShuffleAudioMobile()");
        return false;
    }

    if (stat2 != "on") {
        console.log("TEST FAILED");
        console.log("stat2 did not equal 'on'!!");
        console.log("End: testToggleShuffleAudioMobile()");
        return false;
    }

    if (stat3 != "off") {
        console.log("TEST FAILED");
        console.log("stat3 did not equal 'off'!!");
        console.log("End: testToggleShuffleAudioMobile()");
        return false;
    }

    if ((rand1 === rand2) || (rand1 === rand3) || (rand2 === rand3)) {
        console.log("TEST FAILED");
        console.log("rand1 did not equal rand2, or rand1 did not equal rand3, or rand2 did not equal rand3!!");
        console.log("End: testToggleShuffleAudioMobile()");
        return false;
    }

    console.log("rand1: " + rand1);
    console.log("rand2: " + rand2);
    console.log("rand3: " + rand3);

    console.log("stat1: " + stat1);
    console.log("stat2: " + stat2);
    console.log("stat3: " + stat3);

    console.log("End: testToggleShuffleAudioMobile()");
    return true;
}

function testToggleShuffleVideo() {
    console.log("Begin: testToggleShuffleVideo()");

    var rand1 = videoRandomOrderHolder.getAttribute("data-randorder");
    var stat1 = videoShuffleButton.getAttribute("data-stat");

    toggleShuffle(videoShuffleButton, "video");

    var rand2 = videoRandomOrderHolder.getAttribute("data-randorder");
    var stat2 = videoShuffleButton.getAttribute("data-stat");

    toggleShuffle(videoShuffleButton, "video");

    var stat3 = videoShuffleButton.getAttribute("data-stat");

    toggleShuffle(videoShuffleButton, "video");

    var rand3 = videoRandomOrderHolder.getAttribute("data-randorder");

    if (stat1 != "off") {
        console.log("End: testToggleShuffleVideo()");
        return false;
    }

    if (stat2 != "on") {
        console.log("End: testToggleShuffleVideo()");
        return false;
    }

    if (stat3 != "off") {
        console.log("End: testToggleShuffleVideo()");
        return false;
    }

    if ((rand1 === rand2) || (rand1 === rand3) || (rand2 === rand3)) {
        console.log("End: testToggleShuffleVideo()");
        return false;
    }

    console.log("rand1: " + rand1);
    console.log("rand2: " + rand2);
    console.log("rand3: " + rand3);

    console.log("stat1: " + stat1);
    console.log("stat2: " + stat2);
    console.log("stat3: " + stat3);

    console.log("End: testToggleShuffleVideo()");
    return true;
}

function testToggleShuffleVideoMobile() {
    console.log("Begin: testToggleShuffleVideoMobile()");

    var rand1 = videoRandomOrderHolder.getAttribute("data-randorder");
    var stat1 = videoShuffleButtonMobile.getAttribute("data-stat");

    toggleShuffle(videoShuffleButtonMobile, "video");

    var rand2 = videoRandomOrderHolder.getAttribute("data-randorder");
    var stat2 = videoShuffleButtonMobile.getAttribute("data-stat");

    toggleShuffle(videoShuffleButtonMobile, "video");

    var stat3 = videoShuffleButtonMobile.getAttribute("data-stat");

    toggleShuffle(videoShuffleButtonMobile, "video");

    var rand3 = videoRandomOrderHolder.getAttribute("data-randorder");

    if (stat1 != "off") {
        console.log("TEST FAILED");
        console.log("stat1 did not equal 'off'!!");
        console.log("End: testToggleShuffleVideoMobile()");
        return false;
    }

    if (stat2 != "on") {
        console.log("TEST FAILED");
        console.log("stat2 did not equal 'on'!!");
        console.log("End: testToggleShuffleVideoMobile()");
        return false;
    }

    if (stat3 != "off") {
        console.log("TEST FAILED");
        console.log("stat3 did not equal 'off'!!");
        console.log("End: testToggleShuffleVideoMobile()");
        return false;
    }

    if ((rand1 === rand2) || (rand1 === rand3) || (rand2 === rand3)) {
        console.log("TEST FAILED");
        console.log("rand1 did not equal rand2, or rand1 did not equal rand3, or rand2 did not equal rand3!!");
        console.log("End: testToggleShuffleVideoMobile()");
        return false;
    }

    console.log("rand1: " + rand1);
    console.log("rand2: " + rand2);
    console.log("rand3: " + rand3);

    console.log("stat1: " + stat1);
    console.log("stat2: " + stat2);
    console.log("stat3: " + stat3);

    console.log("End: testToggleShuffleVideoMobile()");
    return true;
}

function testPlayAudio() {
    console.log("Begin: testPlayAudio()");

    var realFlac = audioArrows[6];
    var realMp3 = audioArrows[8];
    var realOgg = audioArrows[10];

    playAudio(realFlac, "Don't play!");

    var nowPlaying1 = nowPlayingNumDiv.getAttribute("data-nowplaying-num");

    playAudio(realMp3, "Don't play!");

    var nowPlaying2 = nowPlayingNumDiv.getAttribute("data-nowplaying-num");

    playAudio(realOgg, "Don't play!");

    var nowPlaying3 = nowPlayingNumDiv.getAttribute("data-nowplaying-num");

    console.log("nowPlaying1: " + nowPlaying1);
    console.log("nowPlaying2: " + nowPlaying2);
    console.log("nowPlaying3: " + nowPlaying3);

    if (nowPlaying1 != 6) {
        console.log("TEST FAILED");
        console.log("nowPlaying1 did equal '6'!!");
        console.log("End: testPlayAudio()");
        return false;
    }

    if (nowPlaying2 != 8) {
        console.log("TEST FAILED");
        console.log("nowPlaying2 did equal '8'!!");
        console.log("End: testPlayAudio()");
        return false;
    }

    if (nowPlaying3 != 10) {
        console.log("TEST FAILED");
        console.log("nowPlaying3 did equal '10'!!");
        console.log("End: testPlayAudio()");
        return false;
    }

    console.log("End: testPlayAudio()");
    return true;
}

function testPlayVideo() {
    console.log("Begin: testPlayVideo()");

    var realMp4 = audioArrows[4];
    var realWebm = audioArrows[6];

    playVideo(realMp4, "Don't play!");

    var nowPlaying1 = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");

    playVideo(realWebm, "Don't play!");

    var nowPlaying2 = videoNowPlayingNumDiv.getAttribute("data-nowplaying-num");

    console.log("nowPlaying1: " + nowPlaying1);
    console.log("nowPlaying2: " + nowPlaying2);

    if (nowPlaying1 != 4) {
        console.log("TEST FAILED");
        console.log("nowPlaying1 did equal '4'!!");
        console.log("End: testPlayAudio()");
        return false;
    }

    if (nowPlaying2 != 6) {
        console.log("TEST FAILED");
        console.log("nowPlaying2 did equal '6'!!");
        console.log("End: testPlayAudio()");
        return false;
    }

    console.log("End: testPlayVideo()");
    return true;
}

function testGiveLinkAudio() {
    console.log("Begin: testGiveLinkAudio()");

    var audioLink = giveLink("audio");

    console.log("audioLink: " + audioLink);

    if (audioLink.endsWith("?t=0&a=mousikófíditestogg0") === false) {
        console.log("TEST FAILED");
        console.log("audioLink.endsWith(\"?t=0&a=mousikófíditestogg0\") did not equal 'true'!!");
        console.log("End: testGiveLinkAudio()");
        return false;
    }

    console.log("End: testGiveLinkAudio()");
    return true;
}

function testGiveLinkVideo() {
    console.log("Begin: testGiveLinkVideo()");

    var videoLink = giveLink("video");

    console.log("videoLink: " + videoLink);

    if (videoLink.endsWith("?t=0&v=realwebm0#videoplayer") === false) {
        console.log("TEST FAILED");
        console.log("videoLink.endsWith(\"?t=0&v=realwebm0#videoplayer\") did not equal 'true'!!");
        console.log("End: testGiveLinkVideo()");
        return false;
    }

    console.log("End: testGiveLinkVideo()");
    return true;
}

function testGiveLinkSingle() {
    console.log("Begin: testGiveLinkSingle()");

    var singleLink = giveLink("single");

    console.log("singleLink: " + singleLink);

    if (singleLink.endsWith("?t=0") === false) {
        console.log("TEST FAILED");
        console.log("singleLink.endsWith(\"?t=0\") did not equal 'true'!!");
        console.log("End: testGiveLinkSingle()");
        return false;
    }

    console.log("End: testGiveLinkSingle()");
    return true;
}

//
// Test Entrypoint
//
function testFidiJs() {
    console.log("BEGIN: MousikóFídi Javascript Test Suite");

    failed.style.color = "red";
    failed.style.fontSize = "1.5em";
    failed.style.fontWeight = "bolder";
    failed.style.textAlign = "center";

    passed.style.color = "green";
    passed.style.fontSize = "1.1em";
    passed.style.fontWeight = "bolder";
    passed.style.textAlign = "center";

    results.style.color = "blue";
    results.style.fontSize = "2em";
    results.style.fontWeight = "bolder";
    results.style.textAlign = "center";

    var fail = 0;
    var pass = 0;

    var result1 = testSetRandomOrderAudio();
    if (result1) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testSetRandomOrderAudio()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testSetRandomOrderAudio()";
        fail += 1;
    }

    var result2 = testSetRandomOrderVideo();
    if (result2) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testSetRandomOrderVideo()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testSetRandomOrderVideo()";
        fail += 1;
    }

    var result3 = testTogggleRepeat();
    if (result3) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testTogggleRepeat()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testTogggleRepeat()";
        fail += 1;
    }

    var result4 = testRandomizeTrackOrderAudio();
    if (result4) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testRandomizeTrackOrderAudio()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testRandomizeTrackOrderAudio()";
        fail += 1;
    }

    var result5 = testRandomizeTrackOrderVideo();
    if (result5) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testRandomizeTrackOrderVideo()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testRandomizeTrackOrderVideo()";
        fail += 1;
    }

    var result6 = testRandomStringFromArray();
    if (result6) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testRandomStringFromArray()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testRandomStringFromArray()";
        fail += 1;
    }

    var result7 = testToggleShuffleAudio();
    if (result7) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testToggleShuffleAudio()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testToggleShuffleAudio()";
        fail += 1;
    }

    var result8 = testToggleShuffleVideo();
    if (result8) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testToggleShuffleVideo()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testToggleShuffleVideo()";
        fail += 1;
    }

    var result9 = testPlayAudio();
    if (result9) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testPlayAudio()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testPlayAudio()";
        fail += 1;
    }

    var result10 = testPlayVideo();
    if (result10) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testPlayVideo()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testPlayVideo()";
        fail += 1;
    }

    var result11 = testGiveLinkAudio();
    if (result11) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testGiveLinkAudio()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testGiveLinkAudio()";
        fail += 1;
    }

    var result12 = testGiveLinkVideo();
    if (result12) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testGiveLinkVideo()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testGiveLinkVideo()";
        fail += 1;
    }

    var result13 = testGiveLinkSingle();
    if (result13) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testGiveLinkSingle()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testGiveLinkSingle()";
        fail += 1;
    }

    var result14 = testToggleShuffleAudioMobile();
    if (result14) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testToggleShuffleAudioMobile()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testToggleShuffleAudioMobile()";
        fail += 1;
    }

    var result15 = testToggleShuffleVideoMobile();
    if (result15) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testToggleShuffleVideoMobile()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testToggleShuffleVideoMobile()";
        fail += 1;
    }

    var result16 = testSetRandomOrderAudioNotZeroStart();
    if (result16) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testSetRandomOrderAudioNotZeroStart()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testSetRandomOrderAudioNotZeroStart()";
        fail += 1;
    }

    var result17 = testSetRandomOrderVideoNotZeroStart();
    if (result17) {
        passed.appendChild(document.createElement("div"));
        passed.childNodes[pass].textContent = "PASS: testSetRandomOrderVideoNotZeroStart()";
        pass += 1;

    } else {
        failed.appendChild(document.createElement("div"));
        failed.childNodes[fail].textContent = "FAIL: testSetRandomOrderVideoNotZeroStart()";
        fail += 1;
    }

    results.textContent = "--  Passed: " + pass + ", Failed: " + fail + " --";
    console.log("END: MousikóFídi Javascript Test Suite");
}

window.onload = testFidiJs();
