'use strict';

const applicationServerPublicKey = 'BI4-CWYfOMBYATgjTKspWBIWFr1ONrW1V7nRSJt-UWG0MyBvxFIny_UBmshqnynMVfIAFcieh-GY2F9-5XLLMs0';

const pushButton = document.querySelector('.js-push-btn');

var sub_str = null;
let isSubscribed = false;
let swRegistration = null;

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

if ('serviceWorker' in navigator && 'PushManager' in window) {
  console.log('Service Worker and Push is supported');

  navigator.serviceWorker.register('static/sw.js')
    .then(function (swReg) {
      console.log('Service Worker is registered', swReg);
      swRegistration = swReg;
      Notification.requestPermission(function(status){console.log(status);})
      initializeUI();
    })
    .catch(function (error) {
      console.error('Service Worker Error', error);
    });
} else {
  console.warn('Push messaging is not supported');
  pushButton.textContent = 'Push Not Supported';
}

function initializeUI() {
  pushButton.addEventListener('click', function () {
    pushButton.disabled = true;
    if (isSubscribed) {
      unsubscribeUser();
    } else {
      subscribeUser();
    }
  });

  // Set the initial subscription value
  swRegistration.pushManager.getSubscription()
    .then(function (subscription) {
      isSubscribed = !(subscription === null);

      updateSubscriptionOnServer(subscription);

      if (isSubscribed) {
        console.log('User IS subscribed.');
      } else {
        console.log('User is NOT subscribed.');
      }

      updateBtn();
    });
}
function subscribeUser() {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  swRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  })
    .then(function (subscription) {
      console.log('User is subscribed.');

      updateSubscriptionOnServer(subscription);

      isSubscribed = true;

      updateBtn();
    })
    .catch(function (err) {
      console.log('Failed to subscribe the user: ', err);
      updateBtn();
    });
}
function updateSubscriptionOnServer(subscription) {
  console.log(subscription);
  sub_str=JSON.stringify(subscription);
}
function updateBtn() {
  if (Notification.permission === 'denied') {
    pushButton.textContent = 'Push Messaging Blocked.';
    pushButton.disabled = true;
    updateSubscriptionOnServer(null);
    return;
  }

  if (isSubscribed) {
    pushButton.textContent = 'Disable Push Notifications';
  } else {
    pushButton.textContent = 'Enable Push Notifications';
  }

  pushButton.disabled = false;
}
function unsubscribeUser() {
  swRegistration.pushManager.getSubscription()
    .then(function (subscription) {
      if (subscription) {
        return subscription.unsubscribe();
      }
    })
    .catch(function (error) {
      console.log('Error unsubscribing', error);
    })
    .then(function () {
      updateSubscriptionOnServer(null);

      console.log('User is unsubscribed.');
      isSubscribed = false;

      updateBtn();
    });
}


function register_push() {
  $('#register').prop('disabled', true);
  if(!isSubscribed)
    alert('enable push notifications and register!!');
  else{
    var src_val = $('#src').val();
    var dst_val = $('#dst').val();
    var jdate_val = $('#date').val();
    var cls_val = $('#cls').val();
    var quota = $('#quota').val();
    if (src_val.length == 0 || dst_val.length == 0 || jdate_val.length == 0) {
      window.alert('All fields are mandatory!!');
      $('#register').prop('disabled', false);
    }
    else {
      var cur_date_str = (+new Date())/1000;
      var params = { 
        src: src_val, 
        dst: dst_val, 
        jdate: jdate_val, 
        jclass: cls_val, 
        quota: quota, 
        sub: sub_str, 
        cur_date:cur_date_str
      };
      $.post('register', params, function (res) { alert('registered!!' + res); });
    }
  }
  $('#register').prop('disabled', false);
}