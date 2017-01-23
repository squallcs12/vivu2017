/**
 * Created by grace7 on 1/21/2017.
 */
// Based On https://github.com/chrisdavidmills/push-api-demo/blob/283df97baf49a9e67705ed08354238b83ba7e9d3/main.js

var isPushEnabled = false,
    subBtn,
    unsubBtn,
    messageBox,
    registration,
    cookie_name = window.WEBPUSH_COOKIE_NAME || 'webpush_notification',
    serviceWorker,
    btn;

window.addEventListener('load', function () {
        subBtn = jQuery('#webpush-subscribe-button');
        messageBox = jQuery('.webpush-message');
        unsubBtn = jQuery('#webpush-unsubscribe-button');
        serviceWorker = document.getElementById('service-worker-js').src;

        btn = subBtn.size() ? subBtn : unsubBtn;

        navigator.serviceWorker.register(serviceWorker)
            .then(
                function (reg) {
                    registration = reg;
                }
            );

        unsubBtn.on('click', function (e) {
            e.preventDefault();
            return unsubscribe();
        });

        subBtn.on('click',
            function (e) {
                e.preventDefault();
                subBtn.prop('disabled', true);
                if (isPushEnabled) {
                    return unsubscribe();
                }

                // Do everything if the Browser Supports Service Worker
                if ('serviceWorker' in navigator) {
                    navigator.serviceWorker.register(serviceWorker)
                        .then(
                            function (reg) {
                                jQuery(btn).text('Loading....');
                                registration = reg;
                                initialiseState(reg);
                            }
                        );
                }
                // If service worker not supported, show warning to the message box
                else {
                    messageBox.text('Your browser doesn\'t support this feature. Please try Chrome.');
                }
            }
        );

        if (jQuery.cookie(cookie_name)) {
            subBtn.hide();
        } else {
            unsubBtn.hide();
        }

        // Once the service worker is registered set the initial state
        function initialiseState(reg) {
            // Are Notifications supported in the service worker?
            if (!(reg.showNotification)) {
                // Show a message and activate the button
                messageBox.text('Showing Notification is not supported in your browser');
                return;
            }

            // Check the current Notification permission.
            // If its denied, it's a permanent block until the
            // user changes the permission
            if (Notification.permission === 'denied') {
                // Show a message and activate the button
                messageBox.text('The Push Notification is blocked from your browser.');
                return;
            }

            // Check if push messaging is supported
            if (!('PushManager' in window)) {
                // Show a message and activate the button
                messageBox.text('Push Notification is not available in the browser');
                return;
            }

            // We need to subscribe for push notification and send the information to server
            subscribe(reg)
        }
    }
);


function subscribe(reg) {
    // Get the Subscription or register one
    getSubscription(reg)
        .then(
            function (subscription) {
                postSubscribeObj('subscribe', subscription);
            }
        )
        .catch(
            function (error) {
                console.log('Subscription error.', error)
            }
        )
}

function getSubscription(reg) {
    return reg.pushManager.getSubscription()
        .then(
            function (subscription) {
                // Check if Subscription is available
                if (subscription) {
                    return subscription;
                }
                // If not, register one
                return registration.pushManager.subscribe({userVisibleOnly: true});
            }
        )
}

function unsubscribe() {
    registration.pushManager.getSubscription()
        .then(
            function (subscription) {

                // Check we have a subscription to unsubscribe
                if (!subscription) {
                    // No subscription object, so set the state
                    // to allow the user to subscribe to push
                    messageBox.text('Subscription is not available');
                    return;
                }
                postSubscribeObj('unsubscribe', subscription);
            }
        );
}

function postSubscribeObj(statusType, subscription) {
    // Send the information to the server with fetch API.
    // the type of the request, the name of the user subscribing,
    // and the push subscription endpoint + key the server needs
    // to send push messages

    var browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase(),
        data = {
            status_type: statusType,
            subscription: subscription.toJSON(),
            browser: browser,
            group: btn.data('group')
        };

    fetch(btn.data('url'), {
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
        credentials: 'include'
    })
        .then(
            function (response) {
                // Check the information is saved successfully into server
                if ((response.status == 201) && (statusType == 'subscribe')) {
                    // Show unsubscribe button instead
                    messageBox.text('You\'ll be received notification when this website have new post');
                    jQuery(btn).hide();
                    jQuery.cookie(cookie_name, '1', {
                        path: '/'
                    });
                }

                // Check if the information is deleted from server
                if ((response.status == 202) && (statusType == 'unsubscribe')) {
                    // Get the Subscription
                    getSubscription(registration)
                        .then(
                            function (subscription) {
                                // Remove the subscription
                                subscription.unsubscribe()
                                    .then(
                                        function (response) {
                                            jQuery(btn).hide();
                                            jQuery.cookie(cookie_name, '', {
                                                path: '/'
                                            });
                                            messageBox.text('Thank you.');
                                        }
                                    )
                            }
                        )
                        .catch(
                            function (error) {
                                messageBox.text('Error during unsubscribe from Push Notification');
                            }
                        );
                }
            }
        )
}
