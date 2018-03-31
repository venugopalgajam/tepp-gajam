
self.addEventListener('notificationclick', function (e) {
    var notification = e.notification;
    var primaryKey = notification.data.primaryKey;
    var action = e.action;
    console.log("action:" + action)
    notification.close();
});

self.addEventListener('push', function (e) {
    var options = {
        body: e.data.text(),
        icon: 'http://www.clker.com/cliparts/h/7/p/F/I/C/hs-train-black-md.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: '2'
        }
    };
    e.waitUntil(
        self.registration.showNotification('Alert!!', options)
    );
});
