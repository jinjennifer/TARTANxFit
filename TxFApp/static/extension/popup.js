var options = {
    type: "basic",
    title: "Group X Class Reminder",
    message: "You have a Group X Zumba Class coming up at 5:15PM in UC Studio A, don't forget to go!",
    iconUrl: "round-logo.png",
    buttons: [{title: "OK"}, {title: "Close"}]
}

window.onload = function() {
  window.setTimeout(function hi(){chrome.notifications.create(options)}, 100);
};

chrome.notifications.onButtonClicked.addListener(function(notifId, btnIdx) {
    if (btnIdx === 0) {
        chrome.notifications.clear(notifId);
    } else if (btnIdx === 1) {
        chrome.notifications.clear(notifId);
    }
});