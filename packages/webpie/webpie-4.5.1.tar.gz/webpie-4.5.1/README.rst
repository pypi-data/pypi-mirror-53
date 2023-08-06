WebPie
======

WebPie (another way of spelling web-py) is a web application development framework for Python based on the WSGI standard.
WebPie makes it simple to develop thread-safe object-oriented web applications.

Hello World in WebPie
---------------------

Here is the simplest web application you can write:

.. code-block:: python

	# hello_world.py

	from webpie import WebPieApp, WebPieHandler		
		
	class MyHandler(WebPieHandler):                     # 1
	
	    def hello(self, request, relpath):              # 2
	        return "Hello, World!\n"                    # 3
			
	application = WebPieApp(MyHandler)                  # 4


What did we just write ? Let's go over the code line by line.

1. We created class MyHandler, which will handle HTTP requests. It has to be a subclass of WebPieHandler class.
2. We defined one web method "hello".
3. It will always return text "Hello, World!"
4. Finally, we created a WSGI application as an instance of WebPieApp class, passing it the MyHandler class as an argument.

Now we can plug our application into any WSGI framework such as uWSGI or Apache httpd, e.g.:

.. code-block:: bash

	uwsgi --http :8080 --wsgi-file hello_world.py


and try it:

.. code-block:: bash

	$ curl http://localhost:8080/hello
	Hello world!
	$ 


If you do not want to use uWSGI or similar framework, you can use WebPie's own HTTP server to publich your application on the web:

.. code-block:: python

	# hello_world_server.py
	from webpie import WebPieApp, WebPieHandler, run_server
	import time

	class MyHandler(WebPieHandler):						

		def hello(self, request, relpath):				
			return "Hello, World!\n"					

	application = WebPieApp(MyHandler)
	application.run_server(8080)

URL Structure
-------------
Notice that MyHandler class has single method "hello" and it maps to the URL path "hello". This is general rule in WebPie - methods of handler classes map one to one to the elements of URI path. For example, we can add another method to our server called "time":

.. code-block:: python

	from webpie import WebPieApp, WebPieHandler
	import time

	class MyHandler(WebPieHandler):						

		def hello(self, request, relpath):				
			return "Hello, World!\n"					

		def time(self, request, relpath):
			return time.ctime()+"\n"

	application = WebPieApp(MyHandler)
	application.run_server(8080)

Now our handler can handle 2 types of requests, it can say hello and it can tell local time:

.. code-block:: bash

	$ curl http://localhost:8080/hello
	Hello, World!
	$ curl http://localhost:8080/time
	Sun May  5 06:47:15 2019
	$ 

Notice that handler methods names automatically become parts of the URL path. There is no need (and no other way) to map WebPie methods to URL.

If you want to split your handler into different classes to organize your code better, you can have multiple handler classes in your application. For example, we may want to have one handler which focuses on reporting time and the other which says hello:

.. code-block:: python

	# time_hello_split.py
	from webpie import WebPieApp, WebPieHandler
	import time

	class HelloHandler(WebPieHandler):						

		def hello(self, request, relpath):				
			return "Hello, World!\n"					

	class ClockHandler(WebPieHandler):						

		def time(self, request, relpath):			
			return time.ctime()+"\n", "text/plain"	

	class TopHandler(WebPieHandler):

		def __init__(self, *params, **kv):
			WebPieHandler.__init__(self, *params, **kv)
			self.greet = HelloHandler(*params, **kv)
			self.clock = ClockHandler(*params, **kv)


	application = WebPieApp(TopHandler)
	application.run_server(8080)


WebPie application is given top handler class as an argument. It will create the handler instances one per each
web request. Top handler can create child handlers recursively. This recirsive handler structure maps one-to-one to the URL structure. The URI is simply the path from the top handler through its child handlers to the method of one of them:

.. code-block:: bash

	Sun May  5 07:39:11 2019
	$ curl  http://localhost:8080/greet/hello
	Hello, World!
	$ 

For example, to find the method for URI "/greet/hello", WebPie starts with top handler, finds its child handler "greet" of class Greeter and then calls its "hello" method.

Any handler in the tree can have its own methods. For example:

.. code-block:: python

	# time_hello_split2.py
	from webpie import WebPieApp, WebPieHandler
	import time

	class HelloHandler(WebPieHandler):						

		def hello(self, request, relpath):				
			return "Hello, World!\n"					

	class ClockHandler(WebPieHandler):						

		def time(self, request, relpath):			
			return time.ctime()+"\n", "text/plain"	

	class TopHandler(WebPieHandler):

		def __init__(self, *params, **kv):
			WebPieHandler.__init__(self, *params, **kv)
			self.greet = HelloHandler(*params, **kv)
			self.clock = ClockHandler(*params, **kv)
		
		def version(self, request, relpath):    # non-leaf handler can have a web method
		    return "1.0.3"

	application = WebPieApp(TopHandler)
	application.run_server(8080)


.. code-block:: bash

	$ curl  http://localhost:8080/version
	1.0.2


Application and Handler
-----------------------

The WebPieApp object is created *once* when the web server instance starts and it exists until the server stops whereas WebPieHandler objects are created for each individual HTTP request. When the handler object is created, it receives the pointer to the app object as its constructor argument. Also, for convenience, Handler object's App member always pointt to the app object. This allows the app object to keep some persistent information and let handler objects access it. For example, or clock application can also maintain number of requests it has received:

.. code-block:: python

	# time_count.py
	from webpie import WebPieApp, WebPieHandler
	import time

	class Handler(WebPieHandler):						

		def time(self, request, relpath):		
			self.App.Counter += 1
			return time.ctime()+"\n", "text/plain"
	
		def count(self, request, relpath): 
			return str(self.App.Counter)+"\n"


	class App(WebPieApp):

		def __init__(self, handler_class):
			WebPieApp.__init__(self, handler_class)
			self.Counter = 0

	application = App(Handler)
	application.run_server(8080)


.. code-block:: bash

	$ curl  http://localhost:8080/time
	Sun May  5 08:10:12 2019
	$ curl  http://localhost:8080/time
	Sun May  5 08:10:14 2019
	$ curl  http://localhost:8080/count
	2
	$ curl  http://localhost:8080/time
	Sun May  5 08:10:17 2019
	$ curl  http://localhost:8080/count
	3


Of course the way it is written, our application is not very therad-safe, but we will talk about this later.

Web Methods in Details
----------------------

The web the WebPie server handler method has 2 fixed arguments and optional keyword arguments.

First argiment is the request object, which encapsulates all the information about the HTTP request. Currently WebPie uses WebOb library Request and Response classes to handle HTTP requests and responses.

Arguments
~~~~~~~~~

Most generally, web method looks like this:

.. code-block:: python

    def method(self, request, relpath, **url_args):
        # ...
        return response


Web method arguments are:

request
.......

request is WebOb request object built from the WSGI environment. For convenience, it is also available as the handler's
Request member.

relpath
.......

Sometimes the URI elements are used as web service method arguments and relpath is the tail of the URI remaining unused after the mapping from URI to the method is done. For example, in our clock example, we may want to use URL like this to specify the field of the current time we want to see:

.. code-block::

	http://localhost:8080/time/month    # month only
	http://localhost:8080/time/minute   # minute only
	http://localhost:8080/time          # whole day/time

Here is the code which does this:

.. code-block:: python

	from webpie import WebPieApp, WebPieHandler
	from datetime import datetime

	class MyHandler(WebPieHandler):						

		def time(self, request, relpath):			
			t = datetime.now()
			if not relpath:
				return str(t)+"\n"
			elif relpath == "year":
				return str(t.year)+"\n"
			elif relpath == "month":
				return str(t.month)+"\n"
			elif relpath == "day":
				return str(t.day)+"\n"
			elif relpath == "hour":
				return str(t.hour)+"\n"
			elif relpath == "minute":
				return str(t.minute)+"\n"
			elif relpath == "second":
				return str(t.second)+"\n"

	application = WebPieApp(MyHandler)
	application.run_server(8080)

url_args
........

Typically URL includes so called query parameters, e.g.:

.. code-block::

	http://localhost:8080/time?field=minute

WebPie always parses query parameters and passes them to the handler method using keyword arguments. For example, we can write the method which extracts fields from current time like this:

.. code-block:: python

	# time_args.py
	from webpie import WebPieApp, WebPieHandler
	from datetime import datetime

	class MyHandler(WebPieHandler):						

		def time(self, request, relpath, field="all"):		
			t = datetime.now()
			if field == "all":
				return str(t)+"\n"
			elif field == "year":
				return str(t.year)+"\n"
			elif field == "month":
				return str(t.month)+"\n"
			elif field == "day":
				return str(t.day)+"\n"
			elif field == "hour":
				return str(t.hour)+"\n"
			elif field == "minute":
				return str(t.minute)+"\n"
			elif field == "second":
				return str(t.second)+"\n"

	WebPieApp(MyHandler).run_server(8080)


and then call it like this:

.. code-block:: bash

	$ curl  http://localhost:8080/time
	2019-05-05 08:39:49.593855
	$ curl  "http://localhost:8080/time?field=month"
	5
	$ curl  "http://localhost:8080/time?field=year"
	2019

Return Value
~~~~~~~~~~~~
The output of a web method is a Response object. Conveniently, there is a number of ways to return something from the web method. Ultimately, all of them are used to produce and return the Response object. Here is a list of possibile returns from the web oject and how the framework
converts the output to the Response object:

======================================  =================================== ==================================================================
return                                  example                             equivalent Response object
======================================  =================================== ==================================================================
Response object                         Response("OK")                      same - Response("OK")
text                                    "hello world"                       Response("hello world")
text, content type                      "OK", "text/plain"                  Response("OK", content_type="text/plain")
text, status                            "Error", 500                        Response("Error", status_code=500)
text, status, content type              "Error", 500, "text/plain"          Response("Error", status_code=500, content_type="text/plain")
text, headers                           "OK", {"Content-Type":"text/plain"} Response("OK", headers={"Content-Type":"text/plain"})
list                                    ["Hello","world"]                   Response(app_iter=["Hello","world"])
iterable                                (x for x in ["hi","there"])         Response(app_iter=(x for x in ["hi","there"]))
iterable, content_type
iterable, status, content_type
iterable, status, headers
======================================  =================================== ==================================================================

Static Content
--------------

Sometimes the application needs to serve static content like HTML documents, CSS stylesheets, JavaScript code.
WebPie App can be configured to serve static file from certain directory in the file system.


.. code-block:: python

    class MyHandler(WebPieHandler):
        #...

    class MyApp(WebPieApp):
        #...
        
    application = MyApp(MyHandler, 
            static_enabled = True,
            static_path = "/static", 
            static_location = "./scripts")
            
    application.run_server(8002)
    
    
If you run such an application, a request for URL like "http://..../static/code.js" will result in
delivery of file local file ./scripts/code.js. static_location can be either relative to the working
directory where the application runs or an absolute path.

Because serving files from local file system is a potential security vulnerability, this
functionality must be explicitly enabled with static_enabled=True. static_path and static_locations
have defaults:

.. code-block:: python

    static_path = "/static"
    static_location = "./static"

Threaded Applications
---------------------
WebPie provides several mechanisms to build thread safe applications. When working in multithreaded environment, WebPie Handler
objects are concurrently created in their own threads, one for each request, whereas WebApp object is created only once and it
is shared by all the threads handling the requests. This feature makes it possible to use the App object for inter-handler
synchronization. The App object has its own lock object and threads can use it in 2 different ways:

atomic decorator
~~~~~~~~~~~~~~~~
Decorating a web method with "atomic" decorator makes the web method atomic in the sense that if a handler thread enters such
a method, any other handler thread of the same application will block before entering any atomic method until the first thread returns from the method.

For example:

.. code-block:: python

    from webpie import WebPieApp, WebPieHandler, atomic

    class MyApp(WebPieApp):
    
        def __init__(self, root_class):
            WebPieApp.__init__(self, root_class)
            self.Memory = {}
    
    class Handler(WebPieHandler):
    
        @atomic
        def set(self, req, relpath, name=None, value=None, **args):
            self.App.Memory[name]=value
            return "OK\n"
        
        @atomic
        def get(self, req, relpath, name=None, **args):
            return self.App.Memory.get(name, "(undefined)")+"\n"
        
    application = MyApp(Handler)
    application.run_server(8002)

You can also decorate methods of the App. For example:

.. code-block:: python

	from webpie import WebPieApp, WebPieHandler, atomic

	class MyApp(WebPieApp):
    
	    RecordSize = 10
    
	    def __init__(self, root_class):
	        WebPieApp.__init__(self, root_class)
	        self.Record = []
        
	    @atomic
	    def add(self, value):
	        if value in self.Record:
	            self.Record.remove(value)
	        self.Record.insert(0, value)
	        if len(self.Record) > self.RecordSize:
	            self.Record = self.Record[:self.RecordSize]
        
	    @atomic
	    def find(self, value):
	        try:    i = self.Record.index(value)
	        except ValueError:
	            return "not found"
	        self.Record.pop(i)
	        self.Record.insert(0, value)
	        return str(i)
        
	class Handler(WebPieHandler):
    
	    def add(self, req, relpath, **args):
	        return self.App.add(relpath)
        
	    def find(self, req, relpath, **args):
	        return self.App.find(relpath)
        
	application = MyApp(Handler)
	application.run_server(8002)


App object as a context manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Another to implement a critical section is to use the App object as the context manager:


.. code-block:: python

    from webpie import WebPieApp, WebPieHandler

    class MyApp(WebPieApp):
    
        def __init__(self, root_class):
            WebPieApp.__init__(self, root_class)
            self.Memory = {}
    
    class Handler(WebPieHandler):
    
        def set(self, req, relpath, name=None, value=None, **args):
            with self.App:
                self.App.Memory[name]=value
            return "OK\n"
        
        def get(self, req, relpath, name=None, **args):
            with self.App:
                return self.App.Memory.get(name, "(undefined)") + "\n"
        
    application = MyApp(Handler)
    application.run_server(8002)


