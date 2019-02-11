import sys
sys.path.append('../')

from bokeh.io import output_notebook,output_file
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.models.widgets import Panel, Tabs #, DataTable, DateFormatter, TableColumn, Tabs, 
from bokeh.layouts import layout
from bokeh.plotting import figure,show,output_file
from bokeh.models import Div

class Dashboard:
    
    def __init__(self):
        #self.div = Div(width=300)
        #self.pt  = ProcessTableComponent()        
        #self.et  = ExperimentTableComponent()        
        #self.b_kill = KillButton({'tables_to_kill':[self.pt,self.et],'label':'kill'})
        #self.b_show = ShowButton({'label':'show'})
        #self.b_restart = ShowButton({'label':'restart'})
        #self.time_graphic = TimeseriesGraphic()
        self.periodicCallbacks = []
        self.layout = {}
        
        #self.s_adviceSelect = BokehSelect({'title':"Advice On:", 'value':"Auto", 'options':["Yes", "No", "Auto"]})
        #self.s_tradeSelect = BokehSelect({'title':"Trade:", 'value':"Auto", 'options':["Yes", "No", "Auto"]})
        #self.s_autoRestart = BokehSelect({'title':"Autostart:", 'value':"No", 'options':["Yes", "No"]})
        
    def getPeriodicCallbacks(self):
        return self.periodicCallbacks
        
    def addPeriodicCallback(self,callback,speed=500):
        self.periodicCallbacks.append([callback,speed])

    def setLayout(key,layout):
        self.layouts[key] = layout

    def getLayout(self):
        j_tab1 = Panel(child=layout([ Div(text="TAB HTML", width=200, height=100)], sizing_mode='fixed'),title="Test Tab")
        tabs = Tabs(tabs=[ j_tab1], width=700)        
        l = layout([tabs],sizing_mode='fixed')         
        return l

    """
    def getConsole(self):

        self.analytics_div = Div(text="Analytics HTML", width=200, height=100)
        self.console = Div(text="System Out console:, width=200, height=100)
        #(Compute Nodes, Running Experiments, Queue and History, Orders & Advice )
        financePlot = self.time_graphic.getBokehComponent()

        j_tab1 = Panel(child=layout([financePlot], sizing_mode='fixed'),title="Analytics")
        j_tab2 = Panel(child=layout([Div(height=500,width=500)], sizing_mode='fixed'),title="System Out")
        j_tab3 = Panel(child=layout([Div(height=500,width=500)], sizing_mode='fixed'),title="Log Data")
        j_tab4 = Panel(child=layout([Div(height=500,width=500)], sizing_mode='fixed'),title="Job Code")
        j_tabs = Tabs(tabs=[ j_tab1, j_tab2, j_tab3, j_tab4 ], width=700)

        
        l1 = layout([
          [
            [self.pt.getBokehComponent()]         
          ],
           [self.getControlPanel()],
            [self.console]            
        ],sizing_mode='fixed')         
        
        l2 = layout([
          [
            [self.et.getBokehComponent()],
                Spacer(width=20),
           []          
          ],
           [self.getControlPanel(),j_tabs],
            [self.analytics_div]
           ,
        ],sizing_mode='fixed') 
        

        tab1 = Panel(child=l1,title="System Processes")
        tab2 = Panel(child=l2,title="Running Experiments")
        tab3 = Panel(child=Div(height=300,width=600),title="Orders & Integration")
        tabs = Tabs(tabs=[ tab1, tab2, tab3 ])
        return tabs
    """
    def modify_doc(self,doc):

        # Create the main plot
        def create_figure():
            return self.getLayout()

        doc.add_root(create_figure())
        pc_list = self.getPeriodicCallbacks()
        for callback in pc_list:
            doc.add_periodic_callback(callback[0], callback[1])

    def showDashboard(self, notebook_url=None):
        if notebook_url is None:
            raise Exception("No notebook URL defined!")
        output_notebook()
        output_file("data_table.html")

        app = Application( FunctionHandler(self.modify_doc))
        doc = app.create_document()
        show(app, notebook_url=notebook_url)