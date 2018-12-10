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
4. [How to make a custom graph](roughNotebooks/CustomGraphExample.ipynb)
5. [How to show a data source grid, and handle the select method](roughNotebooks/DataGridExample.ipynb)
6. [How to handle button events (delete, refresh)](roughNotebooks/ButtonExample.ipynb)
7. [Consolidation: How to create a basic static dashboard.](roughNotebooks/BasicDashboardWithoutEvents.ipynb)
8. [Consolidation: How to create an integrated dashboard with append and delete](roughNotebooks/BasicDashboardWithEvents.ipynb)

# Section 2: Fully Functional Bokeh
Status: In Development, (not published)
Comments: I am  currently extracting and structuring the following examples, and building them into bokehComponents

# Section 3: Web applications 

