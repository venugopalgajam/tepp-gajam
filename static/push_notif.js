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
function subscribeUserToPush(status) {
    alert(status);
    if(status == 'granted'){
        return navigator.serviceWorker.register('static/sw.js')
            .then(function (registration) {
                // alert(registration)
                const subscribeOptions = {
                    userVisibleOnly: true,
                    applicationServerKey: urlB64ToUint8Array('BI4-CWYfOMBYATgjTKspWBIWFr1ONrW1V7nRSJt-UWG0MyBvxFIny_UBmshqnynMVfIAFcieh-GY2F9-5XLLMs0')
                };
                req_fun(registration.pushManager.subscribe(subscribeOptions));
            })
            .catch(function(err){
                alert(err);
            });
    }
    else {
        alert('permission denied!!')
    }
}
function req_fun(sub_json) {
    if (Notification.permission == 'granted') {
        $('#register').prop('disabled', true);
        src_val = $('#src').val();
        dst_val = $('#dst').val();
        jdate_val = $('#date').val();
        cls_val = $('#cls').val();
        quota = $('#quota').val();
        if (src_val.length == 0 || dst_val.length == 0 || jdate_val.length == 0) {
            window.alert('All fields are mandatory!!')
            $('#register').prop('disabled', false);
        }
        else {
            sub_str=JSON.stringify(sub_json);
            params = { src: src_val, dst: dst_val, jdate: jdate_val, cls: cls_val, quota:quota, sub:sub_str}
            $.post('register', params, function(res){alert('registered!!'+res);});
        }
    }
    else  {
        alert('notifications are blocked!!');
    }
};

function register_push(){
    if ('Notification' in window && navigator.serviceWorker) {
        console.log('notifications are supported!!')
        Notification.requestPermission(subscribeUserToPush)
    }
    else {
        alert('notifications are not supported!!')
    }
}
// if ('Notification' in window && navigator.serviceWorker) {
//     console.log('notifications are supported!!')
//     Notification.requestPermission(req_fun)
// }
// else {
//     alert('notifications are not supported!!')
// }
// function displayNotification() {
//     if (Notification.permission == 'granted') {
//         navigator.serviceWorker.getRegistration().then(function (reg) {
//             var options = {
//                 body: 'Here is a notification body!',
//                 icon: 'static/train.ico',
//                 vibrate: [100, 50, 100],
//                 data: {
//                     dateOfArrival: Date.now(),
//                     primaryKey: 1
//                 },
//                 actions: [
//                     {
//                         action: 'like', title: 'Like It!!',
//                         icon: 'static/like.png'
//                     },
//                     {
//                         action: 'dislike', title: 'DisLike it!!',
//                         icon: 'static/dislike.png'
//                     },
//                 ]
//             };
//             reg.showNotification('Hello world!', options);
//         });
//     }
//     else if (Notification.permission === "blocked") {
//         console.log('notifications are blocked!!')
//     }
//     else {
//         Notification.requestPermission(req_fun);
//         displayNotification();
//     }
// }

