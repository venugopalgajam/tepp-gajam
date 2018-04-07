
self.addEventListener('notificationclick', function (e) {
    // var notification = e.notification;
    // var primaryKey = notification.data.primaryKey;
    // var action = e.action;
    // console.log("action:" + action)
    notification.close();
});

self.addEventListener('push', function (e) {
    
    var data_obj = JSON.parse(e.data.text());
    var title = data_obj['avail'];
    var options = {
        body: data_obj['train']+' from '+data_obj['src']+' to '+data_obj['dst'],
        icon: 'http://www.clker.com/cliparts/h/7/p/F/I/C/hs-train-black-md.png'
    };
    e.waitUntil(self.registration.showNotification(title, options));
});
