#!/usr/bin/env node

var args = process.argv.slice(2);  // Strip out first 2 parameters (script path, workdir)
var username = args[0];
var password = args[1];
var video = args[2];
var thumbnail = args[3];
var caption = args[4];  // TODO: Get all parameters after this or use quoted?

var Client = require('instagram-private-api').V1;
var device = new Client.Device('landekamera');
var storage = new Client.CookieFileStorage(__dirname + '/data/'+username+'-cookie.json');

Client.Session.create(device, storage, username, password)
    .then(function(session) {
   	// Now you have a session, we can follow / unfollow, anything...
        // MP4 is the only supported format now, pull request for any other format welcomed!
        console.log("node: Logged in. Starting upload.");
        console.log("Video: " + video + " Thumbnail: " + thumbnail);
        console.log("Caption: " + caption);
        Client.Upload.video(session, video, thumbnail)
            .then(function(upload) {
                return Client.Media.configureVideo(session, upload.uploadId, caption, upload.durationms);
            })
            .then(function(medium) {
                // we configure medium, it is now visible with caption 
                console.log(medium.params);
            });
    });
