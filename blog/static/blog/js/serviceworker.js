/**
 * Created by grace7 on 1/21/2017.
 */
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    var payload = event.data ? event.data.text() : {"head": "No Content", "Body": "No Content"},
        data = JSON.parse(payload),
        head = data.head,
        options = data.options;

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        // Show a notification with title 'ServiceWorker Cookbook' and use the payload
        // as the body.
        self.registration.showNotification(head, options)
    );
});

self.addEventListener('notificationclick', function(event) {
  console.log('On notification click: ', event.notification.tag);
  // Android doesn’t close the notification when you click on it
  // See: http://crbug.com/463146
  event.notification.close();

  event.waitUntil(clients.matchAll({
    type: 'window'
  }).then(function(clientList) {
    var url = event.notification.data.url;
    if (clientList.length){
      var client = clientList[0];
      client.navigate(url);
      return client.focus();
    } else {
      return clients.openWindow(url);
    }
  }));
});
