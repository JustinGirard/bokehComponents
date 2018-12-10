# bokehAnalytics
A platform used to rapidly develop bokeh interactive elements. Included are several illustrative examples

Bokeh is a very powerful rapid development library for python. Unfortunately, it is very code intensive, and unstructured. This means the only people that can leverage it understand how to wrap up complexity into abstracted modules. bokehAnalytics does exactly this; bokehAnalytics wraps up many common tasks within bokeh into standard components which play nice together. The goal is to provide both a high level interface for begineers, with many independent hooks and functionality for those that understand bokeh well.

bokehAnalytics is in active development, and is shared under the MIT license; you can create work with bokehAnalytics, and build it into a product if you like. You can not sell the code, or claim that the work is your own.

TODO:
1. Unit tests. Run all notebooks as part of testing procedure. Internally validate all components
2. Clean up event handling and speed up events
3. Finish Section 2: Advanced bokehComponent examples, production and mass data experimentation
4. Finish Section 3: Creating full python web applications in bokeh

# Section 1: Basic Bokeh Components
If you want to make a basic admin interface, data screen, or share information, the basic bokehComponent notebooks will probably give you all the depth you need. It covers making tabbed dashboards, using buttons, sharing data sources, propagating events, all using a component based object-oriented methodology.
Status: In Alpha, usable
Comments: Functional, needs deeper examples and comments

1. [How to use Tabs](roughNotebooks/TabExample.ipynb)

How to create a dashboard, and how to use tabs, is explained. A tabbed interface within jupyter notebooks is extremely useful for breaking information up without forcing the user to scroll around. It makes jupyter useful.

2. [How to show a basic graph](roughNotebooks/BasicGraphExample.ipynb)

There are a few ways to create graphs. I show how to use a basic graph with a dashboard, and how to leverage the timeseries graphic.

3. [How to load a basic custom data soruce](roughNotebooks/CustomDataSourceExample.ipynb)

Data sources and data management / buffering is a key activity in bokeh. We have created data buffers to simplify this process.

4. [How to make a custom graph](roughNotebooks/CustomGraphExample.ipynb)

This is how you create and custom a graph. 

5. [How to show a data source grid, and handle the select method](roughNotebooks/DataGridExample.ipynb)

How to create and use the data-grid bokehComponent. It makes displaying tabular data sorurces very direct.

6. [How to handle button events (delete, refresh)](roughNotebooks/ButtonExample.ipynb)

Buttons are the most simple interface that can be used. Here I create a button and handle the event in python.

7. [Consolidation: How to create a basic static dashboard.](roughNotebooks/BasicDashboardWithoutEvents.ipynb)

Given all of the other components, a very simple static dashboard is created. No effort is made to use events.

8. [Consolidation: How to create an integrated dashboard with append and delete](roughNotebooks/BasicDashboardWithEvents.ipynb)

Given all of the other components, a simple dynamic dashboard is created. It loads data from the pandas data reader, and manages a synchronized data buffer in memory.

# Section 2: Fully Functional bokehComponents
Status: In Development, (not published)
Comments: I am  currently extracting and structuring the following examples, and building them into bokehComponents

1. How to use pseudo real-time data updates 
2. Custon Data source: How to use connect to mongodb 
3. Custon Data source: How to use google sheets 
4. Custon Data source: How to use json storage
5. Custon Data source: How to use json storage
6. How to host through flask as a native application 
7. How to use a select control
8. How to create a covariance plot (Custom Graph)
9. How to edit a table and update a data buffer / push data
10. How to use an input box with events
11. How to create a search box
12. Consolidation: How to create a live dashboard with stepss (1-11)


# Thanks
I hope you find the work useful, and any comments / questions are welcome.

[Justin Girard](https://www.linkedin.com/in/justin-girard/)
