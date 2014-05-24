# OpenTok Archiving Sample for Python

This is a simple demo app that shows how you can use the OpenTok Python SDK to archive (or record)
Sessions, list archives that have been created, download the recordings, and delete the recordings.

## Running the App

First, we highly recommend setting up a [virtualenv](http://www.virtualenv.org/en/latest/).

```
$ virtualenv venv
$ source venv/bin/activate
```

Next, download the dependencies using [Pip](http://www.pip-installer.org/en/latest/), from the
current directory:

```
(venv)$ pip install -r requirements.txt
```

Then add your own API Key and API Secret to the environment variables. There are a few ways to do
this but the simplest would be to do it right in your shell.

```
(venv)$ export API_KEY=0000000
(venv)$ export API_SECRET=abcdef1234567890abcdef01234567890abcdef
```

Finally, start the server.

```
(venv)$ python archiving.py
```

Visit <http://localhost:5000/> in your browser. Open it again in a second window. Smile! You've just
set up a group chat.

## Walkthrough

This demo application uses the same frameworks and libraries as the HelloWorld sample. If you have
not already gotten familiar with the code in that project, consider doing so before continuing.

The explanations below are separated by page. Each section will focus on a route handler within the
main application (archiving.py).

### Creating Archives – Host View

Start by visiting the host page at <http://localhost:5000/host> and using the application to record
an archive. Your browser will first ask you to approve permission to use the camera and microphone.
Once you've accepted, your image will appear inside the section titled 'Host'. To start recording
the video stream, press the 'Start Archiving' button. Once archiving has begun the button will turn
green and change to 'Stop Archiving'. You should also see a red blinking indicator that you are
being recorded. Wave and say hello! Stop archiving when you are done.

Next we will see how the host view is implemented on the server. The route handler for this page is
shown below:

```python
@app.route("/host")
def host():
    key = api_key
    session_id = session.session_id
    token = opentok.generate_token(session_id)
    return render_template('host.html', api_key=key, session_id=session_id, token=token)
```

If you've completed the HelloWorld walkthrough, this should look familiar. This handler simply
generates the three strings that the client (JavaScript) needs to connect to the session: `api_key`,
`session_id` and `token`. After the user has connected to the session, they press the
'Start Archiving' button, which sends an XHR (or Ajax) request to the <http://localhost:5000/start>
URL. The route handler for this URL is shown below:

```python
@app.route("/start")
def start():
    archive = opentok.start_archive(session.session_id, name="Python Archiving Sample App")
    return archive.json()
```

In this handler, the `start_archive()` method of the `opentok` instance is called with the `session_id`
for the session that needs to be archived. The optional second argument is `name`, which is stored with
the archive and can be read later. In this case, as in the HelloWorld sample app, there is
only one session created and it is used here and for the participant view. This will trigger the
recording to begin. The response sent back to the client's XHR request will be the JSON
representation of the archive, which is returned from the `json()` method. The client is also
listening for the `archiveStarted` event, and uses that event to change the 'Start Archiving' button
to show 'Stop Archiving' instead. When the user presses the button this time, another XHR request
is sent to the <http://localhost:5000/stop/<archive_id>> URL where `<archive_id>` represents the ID the
client receives in the 'archiveStarted' event. The route handler for this request is shown below:

```python
@app.route("/stop/<archive_id>")
def stop(archive_id):
    archive = opentok.stop_archive(archive_id)
    return archive.json()
```

This handler is very similar to the previous one. Instead of calling the `start_archive()` method,
the `stop_archive()` method is called. This method takes an `archive_id` as its parameter, which
is different for each time a session starts recording. But the client has sent this to the server
as part of the URL, so the `archive_id` argument from the route matcher is used to retrieve it.

Now you have understood the three main routes that are used to create the Host experience of
creating an archive. Much of the functionality is done in the client with JavaScript. That code can
be found in the `public/js/host.js` file. Read about the
[OpenTok.js JavaScript](http://tokbox.com/opentok/libraries/client/js/) library to learn more.

### Past Archives

Start by visiting the history page at <http://localhost:5000/history>. You will see a table that
displays all the archives created with your API Key. If there are more than five, the older ones
can be seen by clicking the "Older →" link. If you click on the name of an archive, your browser
will start downloading the archive file. If you click the "Delete" link in the end of the row
for any archive, that archive will be deleted and no longer available. Some basic information like
when the archive was created, how long it is, and its status is also shown. You should see the
archives you created in the previous sections here.

We begin to see how this page is created by looking at the route handler for this URL:

```python
@app.route("/history")
def history():
    page = int(request.args.get('page', '1'))
    offset = (page - 1) * 5
    archives = opentok.get_archives(offset=offset, count=5)

    show_previous = '/history?page=' + str(page-1) if page > 1 else None
    show_next = '/history?page=' + str(page+1) if archives.count > (offset + 5) else None

    return render_template('history.html', archives=archives, show_previous=show_previous,
                            show_next=show_next)
```

This view is paginated so that we don't potentially show hundreds of rows on the table, which would
be difficult for the user to navigate. So this code starts by figuring out which page needs to be
shown, where each page is a set of 5 archives. The `page` number is read from the request's query
string parameters as a string (defaulting to 1 if its not present) and then casted into an `int`.
The `offset`, which represents how many archives are being skipped is always calculated as five
times as many pages that are less than the current page, which is `(page - 1) * 5`. Now there is
enough information to ask for a list of archives from OpenTok, which we do by calling the
`get_archives()` method of the `opentok` instance. This method optionally takes the offset and count
that was just calculated. If we are not at the first page, we can pass the view a string that
contains the relative URL for the previous page. Similarly, we can also include one for the next
page. Now the application renders the view using that information and the partial list of archives.

At this point the template file `templates/history.html` handles
looping over the array of archives and outputting the proper information for each column in the
table. It also places a link to the download and delete routes around the archive's name and
its delete button, respectively.

The code for the download route handler is shown below:

```python
@app.route("/download/<archive_id>")
def download(archive_id):
    archive = opentok.get_archive(archive_id)
    return redirect(archive.url)
```

The download URL for an archive is available as a property of an `Archive` instance. In order to get
an instance to this archive, the `get_archive()` method of the `opentok` instance is used. The only
parameter it needs is the `archive_id`. We use the same technique as above to read that `archive_id`
from the URL. Lastly, we send a redirect response back to the browser so the download begins.

The code for the delete route handler is shown below:

```python
@app.route("/delete/<archive_id>")
def delete(archive_id):
    opentok.delete_archive(archive_id)
    return redirect(url_for('history'))
```

Once again the `archive_id` is retrieved from the URL of the request. This value is then passed the
`delete_archive()` method of the `opentok` instance. Now that the archive has been deleted, a
redirect response back to the first page of the history is sent back to the browser.

That completes the walkthrough for this Archiving sample application. Feel free to continue to use
this application to browse the archives created for your API Key.
