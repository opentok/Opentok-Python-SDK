// Initialize an OpenTok Session object
var session = OT.initSession(apiKey, sessionId);

// Initialize a Publisher, and place it into the element with id="publisher"
var publisher = OT.initPublisher('publisher');

// Attach event handlers
session.on({
  // This function runs when another client publishes a stream (by calling Session.publish())
  streamCreated: function(event) {
    // Create a container for a new Subscriber, assign it an ID using the stream ID, put it inside
    // the DOM element with the ID "subscribers"
    var subContainer = document.createElement('div');
    subContainer.id = 'stream-' + event.stream.streamId;
    document.getElementById('subscribers').appendChild(subContainer);

    // Subscribe to the stream that caused this event, put it inside the container we just made
    session.subscribe(event.stream, subContainer, function(error) {
      if (error) {
        console.error('Failed to subscribe', error);
      }
    });
  }
});

// Connect to the Session using the OpenTok token for permission
session.connect(token, function(error) {
  // This function runs when session.connect() asynchronously completes
  if (error) {
    console.error('Failed to connect', error);
    // Handle connection errors
  } else {
    // Publish the publisher we initialzed earlier (this will trigger 'streamCreated' on other
    // clients)
    session.publish(publisher, function(error) {
      if (error) {
        console.error('Failed to publish', error);
        // Handle publish errors
      }
    });
  }
});
