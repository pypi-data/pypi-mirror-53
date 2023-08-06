#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Supported instruments (identified):
- 
"""

import os
from numpy import savetxt,linspace
import pandas


class Driver():
    
    category = 'Spectrum analyser'
    
    def __init__(self):

        for i in ['A','B','C']:
            setattr(self,f'trace{i}',Traces(self,i))
    
    
    ### User utilities
    def get_data_traces(self,traces=[],single=None):
        """Get all traces or the ones specified"""
        #if single: self.single()
        if traces == []: traces = ['A','B','C']
        for i in traces():
            getattr(self,f'trace{i}').get_data()
        
    def save_data_traces(self,filename,traces=[],FORCE=False):
        if traces == []: traces = ['A','B','C']
        for i in traces():
            getattr(self,f'trace{i}').save_data(filename=filename,FORCE=FORCE)
        
    ### Trigger functions
    def single(self):
        s = self.write("SGL")
        return s
    def run(self):
        self.write('RPT')
        
        
    def getDriverConfig(self):
        config = []
        config.append({'element':'action','name':'run','do':self.run,'help':'Set run mode'})
        config.append({'element':'action','name':'single','do':self.single,'help':'Set single mode'})
        return config
        

#################################################################################
############################## Connections classes ##############################
class Driver_VISA(Driver):
    def __init__(self, address='GPIB0::2::INSTR', **kwargs):
        import visa as v
    
        r          = v.ResourceManager()
        self.scope = r.get_instrument(address)
        Driver.__init__(self, **kwargs)

    def query(self,query,length=1000000):
        self.write(query)
        r = self.read(length=length)
        return r
    def write(self,query):
        self.string = query + '\n'
        self.scope.write(self.string)
    def read(self,length=10000000):
        rep = self.scope.read()
        return rep
        
############################## Connections classes ##############################
#################################################################################


class Traces():
    def __init__(self,dev,trace):
        self.trace     = str(trace)
        self.dev       = dev
        self.data_dict = {}
        
    def get_data(self):
        self.data        = self.query(f"LDAT{self.trace}").split(',')[1:]
        self.data        = [float(self.data[i]) for i in range(len(self.data))]
        self.frequencies = self.get_frequencies(self.data)
        return self.frequencies,self.data
    
    def get_data_dataframe(self):
        frequencies,data              = self.get_data()
        self.data_dict['frequencies'] = self.frequencies
        self.data_dict['amplitude']   = self.data
        return pandas.DataFrame(self.data_dict)
    
    def save_data(self,filename,FORCE=False):
        temp_filename = f'{filename}_AQ6315ATR{self.trace}.txt'
        if os.path.exists(os.path.join(os.getcwd(),temp_filename)) and not(FORCE):
            print('\nFile ', temp_filename, ' already exists, change filename or remove old file\n')
            return
        
        savetxt(temp_filename,(self.frequencies,self.data))

    def set_start_wavelength(self,value):
        self.dev.write(f'STAWL {value}')
    def set_stop_wavelength(self,value):
        self.dev.write(f'STPWL {value}')
    def get_start_frequency(self):
        return float(self.dev.query("STAWL?"))
    def get_stop_frequency(self):
        return float(self.dev.query("STPWL?"))
    def get_frequencies(self,data):
        start = self.get_start_frequency()
        stop  = self.get_stop_frequency()
        return linspace(start,stop,len(data))
    
    def getDriverConfig(self):
        config = []
        config.append({'element':'variable','name':'start_wavelength','write':self.set_start_wavelength,'type':float,'help':'Start wavelength of the window'})
        config.append({'element':'variable','name':'stop_wavelength','write':self.set_stop_wavelength,'type':float,'help':'Stop wavelength of the window'})
        config.append({'element':'variable','name':'start_frequency','read':self.get_start_frequency,'type':float,'help':'Start frequency of the window'})
        config.append({'element':'variable','name':'stop_frequency','read':self.get_stop_frequency,'type':float,'help':'Stop frequency of the window'})
        config.append({'element':'variable','name':'spectrum','read':self.get_data_dataframe,'type':pandas.DataFrame,'help':'Current spectrum'})
        return config
    
if __name__ == '__main__':
    from optparse import OptionParser
    import inspect
    import sys
    
    usage = """usage: %prog [options] arg

               EXAMPLES:
                   get_AQ6315A -o filename A,B,C
               Record the spectrum and create files with two columns lambda,spectral amplitude

               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="com", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="que", default=None, help="Set the query to use." )
    parser.add_option("-i", "--address", type="string", dest="address", default='GPIB::3::INSTR', help="Set ip address." )
    parser.add_option("-l", "--link", type="string", dest="link", default='VISA', help="Set the connection type." )
    parser.add_option("-F", "--force",action = "store_true", dest="force", default=None, help="Allows overwriting file" )
    parser.add_option("-o", "--filename", type="string", dest="filename", default=None, help="Set the name of the output file" )
    #parser.add_option("-t", "--trigger", action="store_true", dest="trigger", default=False, help="Ask the scope to trigger once before acquiring." )    # need is_scope_stopped(self) to enable triggering
    (options, args) = parser.parse_args()
    
    ### Compute traces to acquire ###
    if (len(args) == 0) and (options.com is None) and (options.que is None):
        print('\nYou must provide at least one trace\n')
        sys.exit()
    else:
        chan = [str(a) for a in args[0].split(',') if a in ['A','B','C']]
    ####################################
    
    ### Start the talker ###
    classes = [name for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__]
    assert 'Driver_'+options.link in classes , "Not in " + str([a for a in classes if a.startwith('Driver_')])
    Driver_LINK = getattr(sys.modules[__name__],'Driver_'+options.link)
    I = Driver_LINK(address=options.address)
    
    if options.query:
        print('\nAnswer to query:',options.query)
        rep = I.query(options.query)
        print(rep,'\n')
        sys.exit()
    elif options.command:
        print('\nExecuting command',options.command)
        I.write(options.command)
        print('\n')
        sys.exit()
    
    if options.filename:
        I.get_data_traces(traces=chan) #,single=options.trigger)
        I.save_data_traces(options.filename,FORCE=options.force)

    
    sys.exit()
