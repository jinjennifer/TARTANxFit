var facebook_friends;
var facebook_id;
var facebook_name;
var facebook_email;

// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
  console.log(response);
  // The response object is returned with a status field that lets the
  // app know the current login status of the person.
  // Full docs on the response object can be found in the documentation
  // for FB.getLoginStatus().
  if (response.status === 'connected') {
    // Logged into your app and Facebook.
    testAPI();

    // Redirect only if you are on the login page but are already logged in
    if (window.location == "http://localhost:8000/login" || 
        window.location == "http://localhost:8000/" ||
        window.location == "http://tartanxfit.herokuapp.com/login" || 
        window.location == "http://tartanxfit.herokuapp.com/" ||
        window.location == "https://tartanxfit.herokuapp.com/login" ||
        window.location == "https://tartanxfit.herokuapp.com") {
      FB.api('/me?fields=id,name,email', function(response) {
        console.log('Successful login for: ' + response.name);
        console.log(response);
        facebook_id = response.id;
        facebook_name = response.name;
        facebook_email = response.email;
        var accountURL = "/account/" + facebook_email;
        window.location = accountURL;
      });
    }
  } else if (response.status === 'not_authorized') {
    // The person is logged into Facebook, but not your app.
    console.log("not authorized");
  } else {
    // The person is not logged into Facebook, so we're not sure if
    // they are logged into this app or not.
    console.log("not logged in");
  }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

window.fbAsyncInit = function() {
  FB.init({
    appId      : '355051971506326',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.5
  });

  // Now that we've initialized the JavaScript SDK, we call 
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

  // Redirect after login
  FB.Event.subscribe('auth.login', function(){
    // Redirect only if you are on the login page and just logged in
    if (window.location == "http://localhost:8000/login" || 
        window.location == "http://localhost:8000/" ||
        window.location == "http://tartanxfit.herokuapp.com/login" || 
        window.location == "http://tartanxfit.herokuapp.com/" ||
        window.location == "https://tartanxfit.herokuapp.com/login" ||
        window.location == "https://tartanxfit.herokuapp.com") {
      FB.api('/me?fields=id,name,email', function(response) {
        console.log('Successful login for: ' + response.name);
        console.log(response);
        facebook_id = response.id;
        facebook_name = response.name;
        facebook_email = response.email;
        var accountURL = "/account/" + facebook_email;
        window.location = accountURL;
      });
    }
  });

};

// Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function testAPI() {
  console.log('Welcome!  Fetching your information.... ');
  FB.api('/me?fields=id,name,email', function(response) {
    console.log('Successful login for: ' + response.name);
    console.log(response);
    facebook_id = response.id;
    facebook_name = response.name;
    facebook_email = response.email;
  });

  // Display Facebook friends on the class details page only
  if (window.location.href.indexOf("classes") != -1) {
    displayFriends();
  }
}

// Log out of Facebook when user clicks log out button
function facebookLogout() {
  FB.logout(function(response) {
    console.log("Facebook logged out");
  });
}

function facebookShare() {
  FB.ui({
    method: 'share',
    href: window.location,
  }, function(response){});
}

function getFacebookUserAccount() {
  var accountURL = "/account/" + facebook_email;
  window.location = accountURL;
}

function displayFriends() {
  FB.api('/me/friends', function(response) {
    facebook_friends = response.data;

    for (i = 0; i < facebook_friends.length; i++) {
      name = response.data[i].name;
      id = response.data[i].id;

      FB.api('/' + id + '/picture?type=large', function(response) {
        $("#friends-attending").append('<div class="col-xs-3" id="friend-0">\
            <img alt="user" class="user-pictures" src="' + response.data.url + '">\
            <a href="https://www.facebook.com/' + id + '" class="center">' + name + '</p>\
          </div>');
      });
    }
  });
}