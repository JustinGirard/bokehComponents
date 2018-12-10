from datetime import date,datetime,timedelta
from random import randint
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, Spacer
from bokeh.models import ColumnDataSource,CustomJS,Div
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Tabs, Panel
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.layouts import layout
from bokeh.events import ButtonClick
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
import pandas as pd
import pandas_datareader as pdr
from bokeh.plotting import figure,show,output_file

class BokehTableComponent():
    def __init__(self,settings=None):
        self._settings = {}
        if settings:
            self._settings = settings

        [data,id_field] = self.initData()
        self.id_field = id_field
        self.data = data
        #self.hooks= {'select':[],'delete':[],''}
    
    def setDataAndRefresh(self,data):
        self.data = data
        if( self.source):
            self.source.data = data
            
    def getData(self):
        return self.data
    
    
    def getBokehComponent(self):
        ## First, we construct the data source
        source = ColumnDataSource(self.data)
        source.selected.on_change('indices', self.getCallback())        
        #source.on_change('selected', callback_in)
        columns = []
        for k in self.data.keys():
            columns.append(TableColumn(field=k, title=k))
            #TableColumn(field="dates", title="StartDate", formatter=DateFormatter()),
        data_table = DataTable(source=source, columns=columns, width=self._settings['width'], height=self._settings['height'])
        
        # assign class variables
        self.data_table = data_table
        self.source = source
        return self.data_table
    

    def doRemoveIndices(self,selected_index):
        for k in self.data.keys():
            self.data[k].pop(selected_index)
        return True

    def doDataUpdate(self):
        return True

    def __removeIndices(self,selected_index):
        if self.doRemoveIndices(selected_index):
            return True
        return False


    ## Event Handles
    # Call me when you get a selection event on the resulting table
    def handle_select_callback(self,attr, old, new):

        indices = [self.data[self.id_field][i] for i in new ]
        self.source.selected.indices = new
        self.do_handle_select(attr,old,new)

    
    def Class(self):
        classobj= globals()[self.__class__.__name__]
        return classobj

    def getCallback(self):
        return self.handle_select_callback

    def registerHook(action,function):
        pass

    def getSelected(self):
        s = self.source.selected.indices
        return s

    def removeSelected(self):
        try: 
            l = len(self.source.selected.indices)
        except:
            print("CRITICAL ERROR in removeSelected")
            print(self._settings)
            display(self.source)
            display(self.source.selected)
            display(self.source.selected.indices)

        if l == 0:
            self.source.selected.indices = []
            return
        indicesIn = self.source.selected.indices.copy()
        indicesIn.sort(reverse=True)
        for i in indicesIn:
            self.__removeIndices(i)
        self.doDataUpdate()
        self.setDataAndRefresh(self.data)
        self.source.selected.indices = []

    def removeSelected(self,indicesIn=None):
        try: 
            l = len(self.source.selected.indices)
        except:
            print("CRITICAL ERROR in removeSelected")
            print(self._settings)
            display(self.source)
            display(self.source.selected)
            display(self.source.selected.indices)

        if l == 0:
            self.source.selected.indices = []
            return
        selected_index = self.source.selected.indices[0]
        self.__removeIndices(selected_index)
        self.doDataUpdate()
        self.setDataAndRefresh(self.data)
        self.source.selected.indices = []

    def do_handle_select(self,attr,old,new):
        pass
    
    
    ####### 
    # Global Interface that needs to be updated whenever inheritance happens
    #
    #
    #
    def initData(self):
        data = {
            'theid':['demo_'+str(i) for i in range(10)],
            'dat':['data data ' for i in range(10)],
            }
        id_field = 'theid'
        return [data,id_field]
    


class BokehControl():
    def __init__(self,settings=None):
        self._settings = settings
        if settings == None:
            self._settings = {}
        self.doInit()
    def doInit(self):
        pass
    def regiserHooks(self):
        pass

class BokehButton(BokehControl):
        
    def getBokehComponent(self):
        self.bk = Button(label=self._settings['label'])
        self.bk.on_event(ButtonClick, self.handle_click)
        return self.bk
    
    def handle_click(self,event):
        raise Exception ("Should not be creating a general button")



class BokehSelect(BokehControl):
        
    def getBokehComponent(self):
        self.select = Select(title=self._settings['title'], 
                             value=self._settings["value"], 
                             options=self._settings['options'])

        return self.select
    
    def handle_select(self,event):
        raise Exception ("Should not be creating a general button")


class QueryTableComponent(BokehTableComponent):
    def initData(self):
        self.pi = self._settings['buffered_query_interface']
        data = self.pi.QueryData()
        id_field = self._settings['id_field']
        return [data,id_field]
    
    __instance = None
    
    def doRemoveIndices(self,index):
        idval = self.data[self.id_field][index]
        self.pi.DoAction(action_id = 'kill', query={'key':self.id_field,'value':idval} )
        return True

    def doDataUpdate(self):
        self.data = self.pi.QueryData()
        #for k in self.data.keys():        
        #    print(len(self.data[k]))
        self.setDataAndRefresh(self.data)

        return True    



import pandas as pd

class BufferedQueryInterface():
    '''
    QueryTableComponent(BokehTableComponent) ----> BufferedQueryInterface
    The buffered Query Interface can be used by a BokehTableComponent to handle data. The BokehTable handles events, and front-end concerns. The Query Interface handles data, and all query concerns. It is possible to inherit from, and oveerride the Buffered Query Interface to support a wide variety of queries. These can be to MongoDB, to SQLite, to flat files.
    '''
    def __init__(self,settings = None):
        self._settings = {}
        if settings:
            self._settings = settings
        
        self.componentsToNotify = []
        self.actions = {}
        self.load_data_buffer()
        self.dataNotify()
    def QueryIndices(self,query=None):
        '''
        Find the indices that result from executing any query.
        '''
        self.load_data_buffer()
        if query:
            if 'key' in query and 'value' in query:
                lst = self.data[query['key']]
                indices = [i for i, x in enumerate(lst) if x == query['value']]
                return indices
            else:
                k = list(self.data.keys())[0]
                return [i for i in range(0,len(self.data[k]))]
        else:
            k = list(self.data.keys())[0]
            return [i for i in range(0,len(self.data[k]))]
    
    def QueryData(self,query=None):
        '''
        Find the data rows that corrispond with any query.
        '''
        self.load_data_buffer()
        indices = self.QueryIndices(query)
        if indices:
            ret_data = {}
            for k in self.data:
                ret_data[k] = [self.data[k][i] for i in indices]
            return ret_data
        return None

    def registerAction(self,action_id ,functionPointer):
        self.actions[action_id ] = functionPointer
        pass

    def registerNotify(self,componentsToNotify):
        for c in componentsToNotify:
            self.componentsToNotify.append(c)

    def DoAction(self,action_id = None,query=None,indicesIn = None):
        '''
        Try to execute any user defined action.
        '''        
        if action_id not in self.actions.keys():
            raise Exception("Encountered illegial action request in " + str(self) + " with action " + action_id )
        action_func = self.actions[action_id]
        if indicesIn:
            indices = indicesIn
        else:
            indices = self.QueryIndices(query)
        action_func(self,indices)
        self.load_data_buffer()
        self.dataNotify()


    def dataNotify(self):
        for c in self.componentsToNotify:
            c.setDataAndRefresh(self.data)

    #### Interface below -- Should be overriden by data sources
    #
    #
    #
    #
    def load_data_buffer(self):
        self.data = {
            'process_id':[str(i) for i in range(100)],
            'file':['jobStatrer_'+ str(i%3) for i in range(100)],
            'memory':[ i for i in range(100)],
            'cpu':[ i for i in range(100)],
            }
        self.actions = {'kill':self.action_kill}
    
    
    def action_kill(self,ids):
        for k in self.data.keys(): 
            for selected_index in reversed(ids):
                self.data[k].pop(selected_index)

#
# BokehTimeseriesGraphic && ExampleQuery shows easy line graphs, and 
#
#
class ExampleQuery(BufferedQueryInterface):
    '''
    An example of a data query that produces a compatible lookup table.
    '''
    
    #### Interface below -- Should be overriden by data sources
    #
    #
    #
    #
    def load_data_buffer(self):
        start_init=self._settings['start_date']
        end_init=self._settings['end_date']     

        # Grab data
        start=start_init
        end=end_init 

        data=pdr.get_data_yahoo('AAPL',start,end)
        data_sorted=data.sort_index(axis=0,ascending=True)
        date_list=list(data_sorted.index)

        # Save the data elements
        open_list=list(data_sorted['Open'])
        close_list=list(data_sorted['Close'])
        date_time=[datetime.strptime(str(d),'%Y-%m-%d %H:%M:%S').date() for d in date_list]
        
        self.data = {
            'open_list':open_list,
            'close_list':close_list,
            'date_time':date_time,
            }

class BokehTimeseriesGraphic(BokehControl):
    
    def getBokehComponent(self):
        self.setPlotData()
        return self.createBokehComponent()
    def doDataUpdate(self):
        self.setPlotData()
    def setDataAndRefresh(self,dataIn):
        self.setPlotData()


    def setPlotData(self):
        data_defs = self._settings['data_defs']
        try:
            self.day_increment = self.day_increment +1
        except:
            self.day_increment = 0
        
        data = self._settings['query'].QueryData()
        
        try:
            if (self.init_plot_data):
                pass
        except:
            self.init_plot_data=1
            try:
                self.sources = {}
                for dd in data_defs:
                    data_dict = dict(x=data[dd['x']], y=data[dd['y']])
                    dd['column_data_source'] = ColumnDataSource(data_dict)
                    self.sources[dd['key']] = dd
            except Exception as e:
                print(e)
            
        if self.init_plot_data == 1:
            for dd in data_defs:
                ds = self.sources[dd['key']]
                ds = ds['column_data_source']
                data_dict = dict(x=data[dd['x']], y=data[dd['y']])
                ds.data = data_dict
            for dd in data_defs:
                ds = self.sources[dd['key']]
                ds = ds['column_data_source']
                ds.trigger('data', None, ds.data)

    def createPlotElement(self,p,dd):
        return p.line(x='x',y='y',legend=dd['label'],color=dd['color'], alpha=0.5,source = dd['column_data_source'])

    def createBokehComponent(self):
        p=figure(x_axis_type='datetime',plot_width=self._settings['width'],plot_height=self._settings['height'],title=self._settings['title'],tools="",
                      toolbar_location=None)
        for dd in self.sources.values():
            self.createPlotElement(p,dd)
        p.legend.location = "bottom_right"
        return(p) 

    # Interface -- Overload, or set, these settings to configure the graph
    #
    #
    #
    #
    def doInit(self):
        pass      