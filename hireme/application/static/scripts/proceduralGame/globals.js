//
// Globals
//
'use strict';
var canvas = document.getElementById("game_layer");
var context = canvas.getContext("2d");
var NATIVEWIDTH = 500;
var NATIVEHEIGHT = 500;
var mapOffset;
var chunkSize = 100;

function randomInt(max) {
	return Math.floor(Math.random()*Math.floor(max));
}