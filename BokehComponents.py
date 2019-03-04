from datetime import date,datetime,timedelta
from random import randint
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, Spacer
from bokeh.models import ColumnDataSource,CustomJS,Div
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Tabs, Panel
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider
from bokeh.models.widgets import TextAreaInput
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
        if 'hide' not in self._settings:
            self._settings['hide'] = []
        [data,id_field] = self.initData()
        self.id_field = id_field
        self.data = data
        for h in self._settings['hide']:
            self.data.pop(h, None)
        self.date_keys =[]
        #print(self._settings)
        if 'date_keys' in self._settings: 
            self.date_keys = self._settings['date_keys']
            #print(self.date_keys)
        #self.hooks= {'select':[],'delete':[],''}
    
    def setDataAndRefresh(self,data):
        print("refreshing table!!!!!!!!!!!", data)
        self.data = data
        print(self.data)
        for h in self._settings['hide']:
            self.data.pop(h, None)

        assert len(data.keys()) > 0
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
            if k in self.date_keys:
                #print(k)
                columns.append(TableColumn(field=k, title=k, formatter=DateFormatter(format="%m/%d/%Y %H:%M:%S")))
            else:
                columns.append(TableColumn(field=k, title=k))
        if 'height' in self._settings:
            data_table = DataTable(source=source, columns=columns, width=self._settings['width'], height=self._settings['height'])
        else:
            data_table = DataTable(source=source, columns=columns, width=self._settings['width'])
            
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
        try:
            indices = [self.data[self.id_field][i] for i in new ]
            self.source.selected.indices = new
            self.do_handle_select(attr,old,new)
        except   Exception as e:
            import traceback
            traceback.print_exc()
            print (str(e))            
            print("self.id_field: ",self.id_field)
            print("len(self.data): ",len(self.data))
            print("len(self.data[self.id_field]): ",len(self.data[self.id_field]))
            print("new: ",new)
            print("self.data: ",self.data) 
            raise e
    
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

    def getSelectedIds(self):
        s = self.source.selected.indices
        try: 
            ids = [self.data[self.id_field][i] for i in s ]
        except   Exception as e:
            import traceback
            traceback.print_exc()
            print("CRITICAL ERROR in BokehTableComponent.getSelectedIds")
            print(self.id_field)
            print(self.data[self.id_field])
            print(s)
            raise e
        return ids

    def removeSelected(self):
        try: 
            l = len(self.source.selected.indices)
        except   Exception as e:
            import traceback
            traceback.print_exc()
            print("CRITICAL ERROR in BokehTableComponent.removeSelected")
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
    def setDataAndRefresh(self,data):
        pass #Process any updates from your data soruce
    def getBokehComponent(self):
        #Return the componentt
        pass
        #self.bk = Button(label=self._settings['label'])
        #self.bk.on_event(ButtonClick, self.handle_click)
        #return self.bk

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
        if 'q_key' in self._settings:
            data = self.pi.QueryData(query={'key':self._settings['q_key'],
                                            'value':self._settings['q_value'],
                                            'operator':self._settings['q_operator']})
        else:
            data = self.pi.QueryData()

        id_field = self._settings['id_field']
        return [data,id_field]
    
    __instance = None
    
    def doRemoveIndices(self,index):
        idval = self.data[self.id_field][index]
        self.pi.DoAction(action_id = 'kill', query={'key':self.id_field,'value':idval} )
        return True


    def setDataAndRefresh(self,data_discard):
        
        if 'q_key' in self._settings:
            self.data = self.pi.QueryData(query={'key':self._settings['q_key'],
                                            'value':self._settings['q_value'],
                                            'operator':self._settings['q_operator']})
        else:
            self.data = self.pi.QueryData()        #for k in self.data.keys():        
        
        #    print(len(self.data[k]))
        for h in self._settings['hide']:
            self.data.pop(h, None)

        assert len(self.data.keys()) > 0
        if( self.source):
            self.source.data = self.data
        
    def doDataUpdate(self):
        self.setDataAndRefresh(None)

        return True    



import pandas as pd
from enum import Enum


class BufferedQueryInterface():
    class Parameter(Enum):
        BLANK = 1
        KEY_VALUE = 2
        INDICES = 3
        
    '''
    TODO: Add meta information to register action, such as parameters. This will enforce "discoverable" query interfaces
    QueryTableComponent(BokehTableComponent) ----> BufferedQueryInterface
    The buffered Query Interface can be used by a BokehTableComponent to handle data. The BokehTable handles events, and front-end concerns. The Query Interface handles data, and all query concerns. It is possible to inherit from, and oveerride the Buffered Query Interface to support a wide variety of queries. These can be to MongoDB, to SQLite, to flat files.
    '''
    def __init__(self,settings = None):
        self._settings = {}
        if settings:
            self._settings = settings
        self.componentsToNotify = []
        self.actions = {}
        self._settings['filters'] = {}
        self._settings['ids'] = {}

        self.do_init()
        if len(self._settings['ids']) == 0:
            raise Exception ("No Keys Created for ", str(self), ". Keys (id fields) tell all objects how to index and manage values. within do_init() call self.registerId(key,description) to register a key. ")
        if len(self._settings['ids']) > 1:
            raise Exception ("This version of BufferedQueryInterface only supports single key values. This will change in later versions.")

        self.registerAction('refresh',self.refresh,"Refresh the object")
        self.registerAction('set_filter',self.set_filter, "Set any filter values with new values")

    def registerFilter(self,filter_id ,default=None ,description = ""):
        self._settings['filters'][filter_id ] = {'value':default,'description':description }

    def registerId(self,id_id ,description = ""):
        self._settings['ids'][id_id] = {'description':description }

    def get_filter_keys(self):
        return self._settings['filters'].keys()

    def get_filter_value(self,key):
        if key in self._settings['filters']:
            return self._settings['filters'][key]['value']
        else:
            raise Exception("KEY ",key," NOT FOUND IN get_filter_value ",str(self))

    def get_filters(self):
        return self._settings['filters'].copy()

    def get_id_fields(self):
        return list(self._settings['ids'].keys())

    def get_actions(self):
        return self.actions.copy()
    
    def QueryIndices(self,query=None):
        '''
        Find the indices that result from executing any query.
        '''
        #self.load_data_buffer()
        if len(self.data.keys()) ==0:
            return []

        if query:
            if 'key' in query and 'value' in query and query['operator']=='=':
                lst = self.data[query['key']]
                indices = [i for i, x in enumerate(lst) if x == query['value']]
                return indices
            elif 'key' in query and 'value' in query and query['operator']=='>':
                lst = self.data[query['key']]
                indices = [i for i, x in enumerate(lst) if x > query['value']]
                return indices
            elif 'key' in query and 'value' in query and query['operator']=='<':
                lst = self.data[query['key']]
                indices = [i for i, x in enumerate(lst) if x < query['value']]
                return indices
            elif 'key' in query and 'value' in query and query['operator']=='~':
                lst = self.data[query['key']]
                indices = [i for i, x in enumerate(lst) if x < query['value']+0.01 and x > query['value']-0.01]
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
        #self.load_data_buffer()
        indices = self.QueryIndices(query)
        if indices:
            ret_data = {}
            for k in self.data:
                #ret_data[k] = [self.data[k][i] for i in indices]
                ret_data[k] = []
                for i in indices:
                    if len(self.data[k]) > i:
                        ret_data[k].append(self.data[k][i])
            return ret_data
        
        # Return an empty set with just the data definition
        ret_data = {}
        for k in self.data:
            ret_data[k] = []
        return ret_data

    def registerAction(self,action_id ,functionPointer,description = "",parameters=None):
        self.actions[action_id ] = {'pointer':functionPointer,'description':description,'parameters':None }
        pass

    def registerNotify(self,componentsToNotify):
        for c in componentsToNotify:
            self.componentsToNotify.append(c)

    def DoAction(self,action_id = None,query=None,indicesIn = None,argument=None):
        '''
        Try to execute any user defined action.
        '''  
        if action_id not in self.actions.keys():
            raise Exception("Encountered illegial action request in " + str(self) + " with action " + action_id )
        try:
            action_func = self.actions[action_id]['pointer']
            if indicesIn or query == None:
                indices = indicesIn
            else:
                indices = self.QueryIndices(query)
            if argument:
                # Something funky happens with inheritence which causes the context of self to be passed, or not passed. We just try both
                try:
                    action_func(argumentIn=argument )
                except TypeError as e:
                    action_func(self=self,argumentIn=argument )
            else:
                try:
                    action_func(indicesIn =indices)
                except TypeError as e:
                    action_func(self=self,indicesIn =indices)
            self.update_data_buffer()
        except   Exception as e:
            import traceback
            traceback.print_exc()
            print (str(e))

    def refresh(self,indicesIn=None):
        self.load_data_buffer()
        self.update_data_buffer()
        self.dataNotify()

    def set_filter(self,indicesIn =None,argumentIn=None):
        if argumentIn and isinstance(argumentIn, dict):
            for key in argumentIn.keys():
                if key in self._settings['filters']:
                    self._settings['filters'][key]['value'] = argumentIn[key]
        self.refresh()

    def dataNotify(self):
        for c in self.componentsToNotify:
            c.setDataAndRefresh(self.data.copy())


    #### Interface below -- Should be overriden by data sources
    #
    #
    #
    #
    def update_data_buffer(self):
        pass

    def do_init(self):
        pass
    

    def load_data_buffer(self):
        self.data = {
            'process_id':[str(i) for i in range(100)],
            'file':['jobStatrer_'+ str(i%3) for i in range(100)],
            'memory':[ i for i in range(100)],
            'cpu':[ i for i in range(100)],
            }
    
    
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
                    data_dict = dict(x=data[dd['x']], y=data[dd['y']])### THIS LINE OF CODE BREAKS
                    dd['column_data_source'] = ColumnDataSource(data_dict)
                    self.sources[dd['key']] = dd

            except Exception as e:
                print(e)

        try:

            if self.init_plot_data == 1:
                for dd in data_defs:
                    ds = self.sources[dd['key']]
                    ds = ds['column_data_source']
                    data_dict = dict(x=data[dd['x']], y=data[dd['y']])

                
                for dd in data_defs:
                    #if 'stream' in self._settings and self._settings['stream'] == True:
                    #    datIndex = len(data_dict[dd['x']])-1
                    #    #ds.stream(dict(x=data_dict[dd['x']][datIndex],
                    #    #                     y=data_dict[dd['y']][datIndex]),1000)
                    #    #ds.stream(dict(x=data_dict[dd['x']],
                    #    #                     y=data_dict[dd['y']]),1000)
                    #    ds.trigger('data', None, ds.data)
                    #else:
                    ds.data = data_dict
                    ds = self.sources[dd['key']]
                    ds = ds['column_data_source']
                    ds.trigger('data', None, ds.data)

        except Exception as e:
            print(e)

    def createPlotElement(self,p,dd):
        return p.line(x='x',y='y',legend=dd['label'],color=dd['color'], alpha=0.5,source = dd['column_data_source'])

    def createBokehComponent(self):

        if 'x_range' not in self._settings:
            self._settings['x_range'] = None
        if 'y_range' not in self._settings:
            self._settings['y_range'] = None

        p=figure(x_axis_type='datetime',plot_width=self._settings['width'],
        plot_height=self._settings['height'],
        title=self._settings['title']
        ,x_range=self._settings['x_range'],
        y_range=self._settings['y_range'])
        #,tools=""
        #,toolbar_location=None)
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
        


import pandas as pd
#
#
# Visual Design of the Running Process Table
#
class BokehDiv(BokehControl):
    def doInit(self):
        self.div = Div(text="test", width=self._settings['width'], height=300)
        pass
    def setDataAndRefresh(self,data):
        self.div.text = ""
        if 'print' not  in data:
            return
        if len(data['print'])<=0:
            return
        textList = data['print'][0]
        if len(textList )<=0:
            return
        textStr = ""
        for t in range(len(textList)-10,len(textList)):
            textStr = textStr + "\n<br>" + textList[t]
        self.div.text = textStr

    def getBokehComponent(self):
        return self.div

class BokehLogDiv(BokehControl):
    def doInit(self):
        if 'type' in self._settings and self._settings['type'] == 'textarea':
            self.div = TextAreaInput(value=".",cols = int(self._settings['width']/10),height=int(300/10))
        else:
            self.div = Div(text=".", width=self._settings['width'], height=300)
        assert 'data_field' in self._settings
        assert 'display_range' in self._settings
        pass

    def setVal(self,val):
        if 'type' in self._settings and self._settings['type'] == 'textarea':
            self.div.value = val
        else:
            self.div.text = val

    def setDataAndRefresh(self,data):
        self.setVal( "loading")
        fld = self._settings['data_field']
        if fld not  in data:
            return
        if len(data[fld])<=0:
            return
        textList = data[fld]
        if len(textList )<=0:
            return
        textStr = "<pre>"
        start = len(textList)-self._settings['display_range']
        if start < 0:
            start = 0
        end = len(textList)
        for t in range(start,end):
            textStr = textStr +  textList[t]
        textStr = textStr +  "</pre>"
        self.setVal( textStr )

    def getBokehComponent(self):
        return self.div

class ExperimentTable(QueryTableComponent):
    def do_handle_select(self,attr,old,new):
        pass


class ActionButton(BokehButton):
    def handle_click(self,event):
        #import pprint
        #pprint.pprint(self._settings )
        try:
            query = self._settings['query']
            if 'selection' in self._settings and self._settings['selection']==True:
                # 1. Get the experiment ids from the table
                ids = []
                for tab in self._settings['tables']: 
                    ids = ids + tab.getSelectedIds()
                # 2. Ask the query to do the action on those ids
                idfields = query.get_id_fields()
                #print("2")
                #print(idfields )
                self.handle_selection(event,ids,idfields)
            else:
                self.handle_no_selection(event)

        except   Exception as e:
            import traceback
            traceback.print_exc()
            print (str(e))

    def handle_selection(self,event,ids,idfields):
        if len(idfields )> 0:
            for anId in ids:
                query = self._settings['query']
                query.DoAction(action_id = self._settings['action'],query ={'key':idfields[0],
                                                                          'value':str(anId),
                                                                          'operator':'='})

    def handle_no_selection(self,event):
            query = self._settings['query']
            query.DoAction(action_id = self._settings['action'])

class LoadButton(BokehButton):
    def handle_click(self,event):
        try:

            # 1. Get the experiment ids from the table
            ids = []
            for tab in self._settings['tables']: 
                ids = ids + tab.getSelectedIds()
            # 2. Ask the query to do the action on those ids
            query = self._settings['query']
            for anId in ids:
                print (anId)
                print (self._settings['action'])
                print (self._settings['id_field'])
                print (self._settings['datasource_targets'])
                arg = {self._settings['id_field']:anId}
                act = self._settings['action']
                for trg in self._settings['datasource_targets']:
                    ## The id we are using must match one of the published filters for the target datasoruce
                    trgKey = trg
                    print(self._settings['id_field'])
                    print(trg.get_filter_keys())
                    assert self._settings['id_field'] in trg.get_filter_keys()
                    trg.DoAction(action_id = 'set_filter',argument=arg)
                break
                #query.DoAction(action_id = self._settings['action'],query ={'key':self._settings['id_field'],
                #                                                         'value':str(anId),
                #                                                          'operator':'='})
        except   Exception as e:
            import traceback
            traceback.print_exc()
            print (str(e))
class InteractiveDataGroup:
    '''
        An InteractiveDataGroup brings together a datasource, controls, and visualizations as a collective. The goal is to handle all tracability between datasources, controls, 
        and visualzations so that the controls can remain "dumb".
    '''
    def refresh(self):
        for ds in self.datasources.values():
            ds.refresh()

    def __init__(self,settings):
        self.datasources = {}
        self._settings = settings
        assert 'datasources' in settings
        assert 'visuals' in settings
        assert 'commands' in settings
        
        
        self.running_tables = {} 
        ds_visuals = {}
        #
        #
        # Create all data sources
        for ds in self._settings['datasources']:
            self.datasources[ds['datasource_id']]= ds['class'](ds)
            self.datasources[ds['datasource_id']].refresh()
            ds_visuals[ds['datasource_id']] = []
            self.running_tables [ds['datasource_id']] = []
                    

        self.target_datasoruces = []        #
        if 'datasource_targets' in settings:
            for ds_key in settings['datasource_targets']:
                ds = settings['datasource_targets'][ds_key]
                if isinstance(ds,str):
                    self.target_datasoruces.append(   self.datasources[ds_key]) #we have the class already
                else:
                    self.target_datasoruces.append(ds) #otherwise its an object
        #
        # Create all visuals
        self.visuals = []
        if settings['visuals']:
            for visual_settings in settings['visuals']:
                visual_settings['buffered_query_interface'] = self.datasources[visual_settings['datasource_id']]
                visual_settings['query'] = self.datasources[visual_settings['datasource_id']]
                visual_settings['id_field'] = self.datasources[visual_settings['datasource_id']].get_id_fields()[0]
                visInstance = visual_settings['class'](visual_settings)
                ds_visuals[visual_settings['datasource_id']].append(visInstance)
                self.visuals.append(visInstance)
                if visual_settings['class'] == ExperimentTable or  issubclass(visual_settings['class'],ExperimentTable):
                    self.running_tables[visual_settings['datasource_id']].append(visInstance)
                    

        #
        #
        # Append all the for each datasoruce
        for vis in self._settings['datasources']:
            self.datasources[vis['datasource_id']].registerNotify(ds_visuals[vis['datasource_id']])
        #
        #
        self.buttons = []
        if settings['commands']:
            #for tab_id in button['tables']:
            #    
            for button in settings['commands']:
                sett ={'action':button['action'],
                                          'label':button['label'],
                                          'id_field':self.datasources[button['datasource_id']].get_id_fields()[0],
                                          'query':self.datasources[button['datasource_id']],
                                          'tables': self.running_tables[button['datasource_id']],
                                          'datasource_targets': self.target_datasoruces,
                                            }
                for k in button:
                    sett[k] = button[k]


                buttInstance = button['class'](sett)
                self.buttons.append(buttInstance)
    
    def getVisuals(self):
        return self.visuals.copy()

    def getDatasources(self):
        return self.datasources.copy()
        
    def getControls(self):
        return self.buttons.copy()