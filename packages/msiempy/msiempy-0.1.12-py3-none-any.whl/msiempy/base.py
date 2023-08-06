import abc
import collections
import json
import tqdm
import copy
import csv
import prettytable
import datetime
import functools
import logging
import requests
log = logging.getLogger('msiempy')

from .session import NitroSession
from .error import NitroError
from .utils import regex_match

class NitroObject(abc.ABC):
    """
    Base class for all nitro objects. All objects have a reference the single 
    NitroSession object that handle the esm requests
    """

    class NitroJSONEncoder(json.JSONEncoder):
        """
        Custom JSON encoder that will use the approprtiate propertie depending of the type of NitroObject.
        #TODO return meta info about the Manager. Maybe create a section `manager` and `data`.
        #TODO support json json dumping of QueryFilers, may be by making them inherits from Item.
        """
        def default(self, obj): # pylint: disable=E0202
            if isinstance(obj,(Item, Manager)):
                return obj.data
            #elif isinstance(obj, (QueryFilter)):
                #return obj.config_dict
            else:
                return json.JSONEncoder.default(self, obj) 

    @abc.abstractmethod
    def __init__(self):
        """
        self.nitro.request('esm-get-times')
        """
        self.nitro=NitroSession()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.json

    @abc.abstractproperty
    def text(self):
        """
        Returns str
        """
        pass

    @abc.abstractproperty
    def json(self):
        """
        Returns json representation
        """
        pass

    @abc.abstractmethod
    def refresh(self):
        """
        Refresh the state of the object
        """
        pass

    @staticmethod
    def action_refresh(ntiro_object):
        """
        Refrech callable to use with perform()
        """
        return(ntiro_object.refresh())

class Item(collections.UserDict, NitroObject):
    """
    Base class that represent any SIEM data that can be represented as a item of a manager.
    Exemple : Event, Alarm, etc...
    Inherits from dict
    """
    def __init__(self, adict=None):
        NitroObject.__init__(self)
        collections.UserDict.__init__(self, adict)
        
        for key in self.data :
            if isinstance(self.data[key], list):
                self.data[key]=Manager(alist=self.data[key])
                
        self.selected=False

    @property
    def json(self):
        return(json.dumps(dict(self), indent=4, cls=NitroObject.NitroJSONEncoder))

    @property
    def text(self):
        return(', '.join([str(val) for val in self.values()]))

    def refresh(self):
        log.debug('Refreshing item :'+str(self))

    '''This code has been commented cause it adds unecessary complexity.
    But it's a good example of how we could perform() method to do anything

    def select(self):
        self.selected=False

    def unselect(self):
        self.selected=True

    @staticmethod
    def action_select(item):
        item.select()

    @staticmethod
    def action_unselect(item):
        item.unselect()'''

class Manager(collections.UserList, NitroObject):
    """
    Base class for Managers objects. 
    Inherits from list
    """

    SELECTED='b8c0a7c5b307eeee30039343e6f23e9e4f1d325bbc2ffaf1c2b7b583af160124'
    """
    Random constant represents all selected items to avoid regex matching interference.
    """

    def __init__(self, alist=None):
        """
        Ignore nested lists. Meaning that if alist if a list of lists 
            it will we be ignored.
        Nevertheless, if a list is present as a key value in a dict, 
            it will be added as such.
        """
        NitroObject.__init__(self)
        if alist is None:
            alist=[]
        if isinstance(alist , (list, Manager)):
            collections.UserList.__init__(
                self, [Item(adict=item) for item in alist if isinstance(item, (dict, Item))])
        else :
            raise ValueError('Manager can only be initiated based on a list')
        
        #Unique set of keys for all dict
        #If new fields are added it won't show on text repr. Only json.
        
        self.keys=set()

        #Normalizing the list of dict
        #Finding the unique set
        for item in self.data :
            if item is not None :
                self.keys=self.keys.union(dict(item).keys())
            else :
                log.warning('Having trouble with listing dicts')
        #This means that all dict have the same set of keys
        #Creating keys in dicts
        for item in self.data :
            if isinstance(item, NitroObject):
                for key in self.keys :
                    if key not in item :
                        item[key]=None


    @property
    def text(self):
        text=str()
        for item in self.data :
            text=text+str(item)+'\n' 
        return text


    @property
    def table(self):
        """
        Returns a nice string table made with prettytable.
        It's an expesive thing to do on big ammount of data
        """
        table = prettytable.PrettyTable()
        fields=sorted(self.keys)
        table.field_names=fields
        [table.add_row([str(item[field]) for field in fields]) for item in self.data]
        return table.get_string()

    @property
    def json(self):
        return(json.dumps([dict(item) for item in self.data], indent=4, cls=NitroObject.NitroJSONEncoder))

    def search(self, pattern=None, invert=False, match_prop='json'):
        """
        Return a list of elements that matches regex pattern
        See https://docs.python.org/3/library/re.html#re.Pattern.search
        """
        if isinstance(pattern, str):
            try :
                matching_items=list()
                for item in self.data :
                    if regex_match(pattern, getattr(item, match_prop)) is not invert :
                        matching_items.append(item)
                return Manager(alist=matching_items)

            except Exception as err:
                raise err
        elif pattern is None :
            return self
        else:
            raise ValueError('pattern must be str or None')

    ''' This code has been commented cause it adds unecessary complexity.
    But it's a good example of how we could perform() method to do anything

    def select(self, data_or_pattern, **search):
        """
        Select the rows that match the pattern.
        The patterm could be a index, list of index or list of rows
        """
        self.perform(Item.action_select, data_or_pattern, **search)

    def unselect(self, data_or_pattern, **search):
        """
        Unselect the rows that match the pattern.
        The patterm could be a index, list of index or list of rows
        """
        self.perform(Item.action_unselect, data_or_pattern, **search)
        '''
    
    def clear(self):
        """
        Unselect all items.
        """
        for item in self.data :
            item.selected=False
        #self.perform(Item.action_unselect, '.*') : 

    def refresh(self):
        """
        Execute refresh function on all items.
        """
        self.perform(Item.action_refresh)

    def perform(self, func, pattern_or_list=None, func_args=None, search_args=None,
                    confirm=False, asynch=False, progress=False, message=None ):
        """
        Wrapper arround executable and group of object.
        Will execute the callable on specfied data (by `pattern`) and return a list of results

            Params
            ======
            func : callable stateless function
                funs is going to be called like func(item, **func_args) on all items in data patern
            if pattern_or_list stays None, will perform the action on the seleted rows,
                if no rows are selected, wil perform on all rows
            pattern_or_list can be :
                - string regex pattern match using search method
                - a list of objets
                    However, only list of dict can be passed if asynch=True
                - Manager.SELECTED
            func_args : dict that will be passed by default to func in all calls
            search_args : dict passed as extra arguments to search method
                i.e :
                    {invert=True, match_func='text'} or 
            
            confirm : will ask interactively confirmation 
            asynch : execute the task asynchronously with NitroSession executor 
            progress : to show progress bar with ETA (tqdm) 
            message : To show to the user

        Returns a list of returned results
        """

        log.debug('Calling perform func='+str(func)+
            ' pattern_or_list='+str(pattern_or_list)[:100]+'...'+
            ' func_args='+str(func_args)+
            ' search_args='+str(search_args)+
            ' confirm='+str(confirm)+
            ' asynch='+str(asynch)+
            ' progress='+str(progress))

        if not callable(func) :
            raise ValueError('func must be callable')

        if pattern_or_list is not None and not isinstance(pattern_or_list, (str, list,)):
            raise ValueError('pattern_or_list can only be : (str, list or None) not '+str(type(pattern_or_list)))

        #Actual list of element the function is going to be called on
        elements=list()
        
        # If pattern_or_list is left None, apply the action to everything
        if pattern_or_list is None :
            elements=list(self)

        #pattern_or_list is a string
        elif isinstance(pattern_or_list, str) :

            # Apply the action to selected items
            if pattern_or_list == self.SELECTED :
                elements=self.selected_items

            else:
                # Regex search when pattern is String.
                # search method returns a list 
                elements=self.search(pattern_or_list, **(search_args if search_args is not None else {}))
        
        #A list of elements is already passed
        elif isinstance(pattern_or_list, list) :
            elements = pattern_or_list

        #Confirming with user if asked
        if confirm : self._confirm_func(func, elements)

        #Setting the arguments on the function
        func = functools.partial(func, **(func_args if func_args is not None else {}))
        
        #The data returned by function
        returned=list()

        #Printing message if specified.
        #The message will appear on loading bar if progress is True
        if message is not None:
            if not progress:
                log.info(message)
            else:
                tqdm_args=dict(desc=message, total=len(elements))

        #Runs the callable on list on executor or by iterating
        if asynch == True :
            
            if progress==True:
                returned=list(tqdm.tqdm(self.nitro.executor.map(
                    func, elements), **tqdm_args))
            else:
                log.info()
                returned=list(self.nitro.executor.map(
                    func, elements))
        else :

            if progress==True:
                elements=tqdm.tqdm(elements, **tqdm_args)

            for index_or_item in elements:
                returned.append(func(index_or_item))

        return(returned)

    @staticmethod
    def _confirm_func(func, elements):
        """
        Ask user inut to confirm the calling of `func` on `elements`.
        """
        if not 'y' in input('Are you sure you want to do this '+str(func)+' on '+
        ('\n'+str(elements) if elements is not None else 'all elements')+'? [y/n]: '):
            raise InterruptedError("The action was cancelled by the user.")

    @property
    def selected_items(self):
        """
        Selected items only.
        Returns a Manager
        """
        return(Manager(alist=[item for item in self.data if item.selected]))

    @staticmethod
    def download_testing_data():
        """
        Terrestrial Climate Change Resilience - ACE [ds2738]

        California Department of Natural Resources — For more information, 
        see the Terrestrial Climate Change Resilience Factsheet 
        at http://nrm.dfg.ca.gov/FileHandler.ashx?DocumentID=150836.
        
        The California Department...
        """
        url='http://data-cdfw.opendata.arcgis.com/datasets/7c55dd27cb6b4f739091edfb1c681e70_0.csv'

        with requests.Session() as s:
            download = s.get(url)
            content = download.content.decode('utf-8')
            data = list(csv.DictReader(content.splitlines(), delimiter=','))
            return data