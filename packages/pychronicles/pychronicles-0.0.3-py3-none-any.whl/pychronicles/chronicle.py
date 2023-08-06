#!/bin/python3
# -*- coding: utf-8 -*-
"""
Chronicles

@author: Thomas Guyet
@date: 04/2019
@institution: AGROCAMPUS-OUEST/IRISA
"""

import warnings
import numpy as np
import sys, getopt
import warnings
import scipy.sparse.csgraph
from lark import Lark

def resize(l, n, d = None):
    while len(l) < n:
        l.append(d)

      
def reformat_sequence(sequence):
    """
    @author: Issei Harada, Thomas Guyet
    @date: 05/2019
    @institution: INRIA/INRIA
    """  
    """reshape the sequence if the format is [(event,event_time)]
    
    - event_time must be positive, integers (no float available)
    """
    
    for event in sequence:
        try :
            type((event[1])==int)
        except:
            print("reformat_sequence error: wrong input format, timestamps must be integers")
            return None
        if event[1]<0:
            print("reformat_sequence error: wrong input format, timestamps must be positive")
            return None
    #sort events by their timestamps
    sequence.sort(key=lambda e: e[1])
    #generate a sequence with None
    timestamp_max = int(sequence[len(sequence)-1][1])
    sequence_format = [None] * (timestamp_max +1) 
    for event in sequence :
        sequence_format[int(event[1])] = event[0]      
    return sequence_format
        

class EventMapper:
    def __init__(self):
        self.__event_map={}
        self.__rev_event_map={}
        
    def id(self, event):
        """
        return a unique identifier corresponding to the event label
        """
        idv = self.__event_map.setdefault(event, len(self.__event_map))
        self.__rev_event_map[idv]= event
        #print("create "+str(event)+" with id "+str(idv))
        return idv 
        
    def event(self, idv):
        """
        return the name of an event by its identifier
        """
        if not idv in self.__rev_event_map:
            raise KeyError('EventMapper error: unknown event with id '+str(idv)+". Known events: "+str(list(self.__rev_event_map))+".")
        else:
            return self.__rev_event_map[idv]

class Chronicle:
    """Class for a chronicle pattern modeling
    -> enables to have partially defined chronicles 
    
    Attributes
    ----------
    sequence : [int|None]
        a list of events
        if None, the event is not specified but something must happend to be recognize.
        
    tconst: {(int,int):(double,double)}
        a map assigning an temporal constraint (lower and upper bounds) of the delay between the events in the key.
        
    pid : int
        chronicle identifier
        
    inconsistent: bool
        True is the chronicle is inconsistent and had a consistency check (through minimization)
        
    Methods:
    ---------
    
    add_item(self, pos, item)
        Add item at position pos. Replace the existing item if it exists
    
    add_constraint(self, ei, ej, const)
        Add a temporal constraint (couple) from event ei to ej
        
        
    delete(self, pos)
        remove the item at position pos
        
    delete_constr(self, ei, ej)
        destroy the constrains from ei to ej
        
    clean(self)
        destroy useless items and constraints (but does not remove all)
        
    minimize(self)
        minimize the temporal constraints. It applies a Floyd-Warshall algorithm on the 
        
    recognize(self, s)
        return the list of all occurrences of the chronicle in the sequence s
    
    isrecognize(self,s)
        return True whether their is at least one occurrence of the chronicle in the sequence s, and false otherwise.
        This function is faster than the recognize function
        
        
    @author: Thomas Guyet
    @date: 04/2019
    @institution: AGROCAMPUS-OUEST/IRISA
    """
    
    npat = 0
    
    """
    CRS_grammar is a grammar for parsing CRS files
    """
    CRS_grammar=r"""start: chronicle+

chronicle: "chronicle" NAME "()" "{" event+ constraint* "}"

event: "event" "(" NAME "," ID ")"
constraint: ID "-" ID "in" INTERVAL

INTERVAL: "[" NUMBER "," NUMBER "]"
ID: "t" NUMBER
NAME: CNAME ["[]"]
WHITESPACE: (" " | "\t" | "\n")+
%ignore WHITESPACE
%import common.SIGNED_NUMBER    -> NUMBER
%import common.CNAME
"""

    def __init__(self, emapper=None):
        """
        - emapper is an event mapper, if not provided, a new one is created
        """
        
        self.tconst={}  #temporal constraints,
                        # keys: couple (ei,ej) where ei is a index in the item
                        #   in the multiset
                        # values; couple (lb,ub)
        self.inconsistent = False
        self.name = ""
        self.sequence = {}      # description of the pattern events
        self.pid=Chronicle.npat   # pattern id
        Chronicle.npat += 1

        if not emapper:
            self.emapper = EventMapper()
        else:
            self.emapper = emapper

    def add_event(self, pos, event):
        """Add an event to the chronicle multiset
        Contrary to add_item, an integer is not required to denote an event!
        """
        self.__add_item(pos, self.emapper.id(event) )
        
    def __add_item(self, pos, item):
        """Add an item to the chronicle
        The function creates all infinite constraints, without variability
        - the id of the event correspond to the order of added items
        """
        self.sequence[pos] = item
        for i in range(pos):
            if not (i,pos) in self.tconst:
                if i in self.sequence and self.sequence[i]==item:
                    self.tconst[(i,pos)]= (1,float("inf")) #here: 1 means that the same items must occur after!
                else:
                    self.tconst[(i,pos)]= (-float("inf"),float("inf"))
        for i in range(pos+1,max(self.sequence.keys())+1):
            if not (pos,i) in self.tconst:
                if i in self.sequence and self.sequence[i]==item:
                    self.tconst[(pos,i)]= (1,float("inf"))
                else:
                    self.tconst[(pos,i)]= (-float("inf"),float("inf"))
        
    def add_constraint(self, ei, ej, constr):
        """Add a constraint-template to the chronicle pattern
        - ei, ej: index of the events in the multiset
        - constr: a 2-tuple (min,max)
        """
        if not type(constr) is tuple:
            print ("error: constraint must be a tuple (=> constraint not added)")
            return
            
        if len(constr)!=2:
            print ("error: constraint must have 2 values (=> constraint not added)")
            return
            
        try:
            self.tconst[(ei,ej)] = constr
        except IndexError:
            print ("add_constraint: index_error (=> constraint not added)")
        
    def __getitem__(self, i):
        """return the item at position i in the multiset if i is an integer
        and return the constraint between i[0] and i[1] if i is a couple
        """
        if not type(i) is tuple:
            return self.sequence[i]
        else:
            try:
                return self.tconst[(min(i[0],i[1]),max(i[0],i[1]))]
            except KeyError:
                return (-float("inf"),float("inf"))
        
            
    def __len__(self):
        """ Length of the patterns (number of items)
        """
        if not self.sequence:
            return 0
        return max(self.sequence.keys())+1
        
    def __str__(self):
        """
        s = "C"+str(self.pid)+": {"+str(self.sequence) + "}\n"
        s += "\t "+str(self.tconst) + "\n"
        """
        s = "C"+str(self.pid)+"\t {{"+ ','.join([str(self.emapper.event(v)) for k,v in self.sequence.items()]) + "}}\n"
        for i in self.sequence.keys():
            for j in [v for v in self.sequence.keys() if v>i]:
                s += str(i) + "," + str(j) + ": " + str(self.tconst[(i,j)])+"\n"
        return s
        
    def delete(self, itempos):
        self.sequence[ itempos ]=None

    def clean(self):
        for itempos in list(self.sequence.keys()):
            if self.sequence[ itempos ]==None:
                del self.sequence[ itempos ]
        posmax = max(self.sequence.keys())
        for p in list(self.tconst.keys()):
            if p[0]>posmax or p[1]>posmax:
                del self.tconst[p]
            
        
    def delete_constr(self, ei, ej):
        try:
            del self.tconst[(ei,ej)]
        except KeyError:
            pass

    def minimize(self):
        #construction of distance graph
        mat=np.matrix( np.zeros( (max(self.sequence.keys())+1,max(self.sequence.keys())+1) ))
        for i in range(max(self.sequence.keys())+1):
            for j in range(i+1,max(self.sequence.keys())+1):
                if (i,j) in self.tconst:
                    mat[i,j] = self.tconst[ (i,j) ][1]
                    mat[j,i] = -self.tconst[ (i,j) ][0]
                else:
                    mat[i,j] = float("inf")
                    mat[j,i] = -float("inf")
        try:
            matfw = scipy.sparse.csgraph.floyd_warshall( mat )
            #construction of simplified chronicle
            for i in range(max(self.sequence.keys())+1):
                for j in range(i+1,max(self.sequence.keys())+1):
                    self.tconst[ (i,j) ] = (- int(matfw[j,i]), int(matfw[i,j]))
        except:
            warnings.warn("*** Minimisation: Inconsistent chronicle ***")
            self.inconsistent = True
    ################
    
    def __CRS_read_tree(tree, chronicle=None, id_map={}):
        if tree.data =="start":
            return Chronicle.__CRS_read_tree(tree.children[0], chronicle, id_map)
        elif tree.data == "chronicle":
            if not chronicle:
                C = Chronicle()
            else:
                C = chronicle
            print(id_map)
            C.name = str(tree.children[0][:-2]) #remove the last two characters '[]'
            for i in range(1,len(tree.children)):
                Chronicle.__CRS_read_tree(tree.children[i],C, id_map)
            return C
        elif tree.data=="event":
            event = str(tree.children[0])
            event = event.strip("[]") #remove the '[]' if necessary
            eid = id_map.setdefault(str(tree.children[1]), len(id_map))
            chronicle.add_event(eid, event)
        elif tree.data=="constraint":
            eid1=id_map[str(tree.children[0])]
            eid2=id_map[str(tree.children[1])]
            interval=str(tree.children[2]).strip('[]').split(',')
            if eid1<eid2 :
                chronicle.add_constraint(eid1,eid2, (-int(interval[1]), -int(interval[0])))
            else:
                chronicle.add_constraint(eid2,eid1, (int(interval[0]), int(interval[1])))
        
    def load(crs, emapper=None):
        """Load a chronicle from a string in the CRS format.
        Note that the all brackets ("[]" in chronicle or events names; and "()") are assumed to be empty in this function !!!
        
        This is a class-function.
        
        parameters:
        - crs: string describing a string in a CRS format
        - emapper (optional): an external event mapper
        
        return the newly instantiated chronicle
        """
        chro_parser = Lark(Chronicle.CRS_grammar)
        tree= chro_parser.parse(crs)
        if not emapper:
            return Chronicle.__CRS_read_tree(tree, id_map={})
        else:
            C = Chronicle(emapper)
            return Chronicle.__CRS_read_tree(tree, C, {})
            
            
    def to_crs(self):
        """Generate a string representing the chronicle in the CRS format.
        
        Unnamed events (must be figures) are called "E"+str(X) in the event description to avoid events name starting with figures (CNAME conventions)
        Infinite intervals are not printed out, but semi-infinite intervals will generate an description like '[-inf,23]', or '[34,inf]' : do not know whether it is sound or not!
        
        return a string
        """
        s="chronicle "
        if self.name!="":
            s+=str(self.name)
        else:
            s+="C"+str(self.pid)
        s+="[]()\n{\n"

        for pos,e in self.sequence.items():
            if self.emapper:
                evt = self.emapper.event(e)
                if isinstance(evt, str):
                    s+="\tevent("+evt+"[], t{:03d})\n".format(pos)
                else:
                    s+="\tevent(E"+str(evt)+"[], t{:03d})\n".format(pos)
            else:
                s+="\tevent(E"+str(e)+"[], t{:03d})\n".format(pos)
        s+="\n"
        
        for events,interval in self.tconst.items():
            if interval[0]!=float("-inf") or interval[1]!=float("inf"): #infinite intervals are not printed out
                s+="\tt{:03d}-t{:03d} in [{},{}]\n".format(events[0],events[1],interval[0],interval[1])
        s+="}"
        return s 
                
    
    ################
    def __complete_recognition__(self, occurrence, item_index, sequence):
        """
        return a list of occurrences that add the description of the matching of the item_index-th item of the chronicle to the occurrence
        """
        
        if not item_index in self.sequence:
            return [occurrence]
            
        item=self.sequence[item_index]
            
        if occurrence[item_index][0]==occurrence[item_index][1]:
            if occurrence[item_index][0]<len(sequence) and sequence[ occurrence[item_index][0] ]== item:
                return [occurrence]
            else:
                return []
        
        occurrences = []
        
        #assert(occurrence[item_index][1]<len(sequence))
        for p in range( occurrence[item_index][0], occurrence[item_index][1]+1 ):
            if sequence[p]==item:
                #create a new occurrence to be modified
                new_occ = occurrence[:]
                new_occ[item_index] = (p,p)
                
                satisfiable=True
                #propagate chronicle constraints
                for k in self.tconst:
                    v = self.tconst[k]
                    if (k[0]==item_index) and (k[1] in self.sequence):
                        new_occ[ k[1] ] = (max(new_occ[ k[1] ][0], p+v[0]), min(new_occ[ k[1] ][1], p+v[1]))
                        if new_occ[ k[1] ][0]>new_occ[ k[1] ][1]: #if empty interval, it is not satisfiable
                            satisfiable=False
                            break
                        
                if satisfiable:
                    #add the occurrence to the list
                    occurrences.append( new_occ )
        return occurrences
    
    
    def __recrecognize__(self, occurrence, last_item_index, sequence):
        """
        recursive call for occurrence recognition
        return a list of occurrences recognized from the last_item_index of the chronicle until its last item
        """
        chro_size=max( self.sequence.keys() )
        if last_item_index==chro_size:
            return [occurrence]
        
        item_index=last_item_index+1
        
        occurrences = []
        loc_occs = self.__complete_recognition__(occurrence, item_index, sequence)
        for occ in loc_occs:
           reoccs= self. __recrecognize__(occ, item_index, sequence)
           occurrences.extend(reoccs)
        return occurrences
                
    def recognize(self,sequence):
        """
        Method that checks whether the chronicle occurs in the sequence 
        sequence: list of events
        Return a list of occurrences
        """
        return self.__recognize([self.emapper.id(event) if event else None for event in sequence])
    
    def __recognize(self,sequence):
        """
        Method that checks whether the chronicle occurs in the sequence 
        sequence: list of event identifiers
        Return a list of occurrences
        """
        occurrences = [] #list of occurrences
        
        chro_size=max( self.sequence.keys() )+1
        if chro_size==0 :
            return occurrences
        
        item_index = 0
        item=self.sequence[item_index]
        seq_len = len(sequence)
        for p in range(seq_len):
            if sequence[p]==item:
                #create a new occurrence
                new_occ = []
                resize(new_occ, chro_size, (0,seq_len-1))
                new_occ[item_index] = (p,p)

                #propagate chronicle constraints
                for k in self.tconst:
                    v = self.tconst[k]
                    if (k[0]==item_index) and (k[1] in self.sequence):
                        new_occ[ k[1] ] = (max(0,p+v[0]), min(p+v[1],seq_len-1))
                
                #ajouter l'occurrence à la liste des occurrences
                loc_occ = self.__recrecognize__(new_occ, item_index, sequence)
                occurrences.extend( loc_occ )
                
        return occurrences
        
        
    def isrecognize(self,sequence):
        """
        Method that checks whether the chronicle occurs in the sequence 
        sequence: list of events
        Return a list of occurrences
        """
        return self.__isrecognize([self.emapper.id(event) if event else None for event in sequence])
    
    def __isrecognize(self,sequence):
        """
        Method that checks whether the chronicle occurs in the sequence 
        sequence: list of events
        Return boolean
        """        
        if len(self.sequence)==0:
            return [[]]
        
        chro_size=max( self.sequence.keys() )+1
        if chro_size==0 :
            return occurrences
        
        item_index = 0
        try:
            item=self.sequence[item_index]
        except KeyError:
            print(self.sequence)
            exit(0)
        seq_len = len(sequence)
        for p in range(seq_len):
            if item==None or sequence[p]==item:
                #create a new occurrence
                new_occ = []
                resize(new_occ, chro_size, (0,seq_len-1))
                new_occ[item_index] = (p,p)

                #propagate chronicle constraints
                for k in self.tconst:
                    v = self.tconst[k]
                    if (k[0]==item_index) and (k[1] in self.sequence):
                        new_occ[ k[1] ] = (max(0,p+v[0]), min(p+v[1],seq_len-1))
                
                #ajouter l'occurrence à la liste des occurrences
                if self.__is_recrecognize__(new_occ, item_index, sequence):
                    return True
        return False
            
    def __is_complete_recognition__(self, occurrence, item_index, sequence):
        """
        return a list of occurrences that add the description of the matching of the item_index-th item of the chronicle to the occurrence
        """
        
        if not item_index in self.sequence:
            return occurrence
            
        item=self.sequence[item_index]
            
        if occurrence[item_index][0]==occurrence[item_index][1]:
            if occurrence[item_index][0]<len(sequence) and (sequence[ occurrence[item_index][0] ]== item or item==None):
                return occurrence
            else:
                return None
        
        for p in range( occurrence[item_index][0], occurrence[item_index][1]+1 ):
            if item==None or sequence[p]==item:
                #create a new occurrence to be modified
                new_occ = occurrence[:]
                new_occ[item_index] = (p,p)
                
                satisfiable=True
                #propagate chronicle constraints
                for k in self.tconst:
                    v = self.tconst[k]
                    if (k[0]==item_index) and (k[1] in self.sequence):
                        new_occ[ k[1] ] = (max(new_occ[ k[1] ][0], p+v[0]), min(new_occ[ k[1] ][1], p+v[1]))
                        if new_occ[ k[1] ][0]>new_occ[ k[1] ][1]: #if empty interval, it is not satisfiable
                            satisfiable=False
                            break
                        
                if satisfiable:
                    #add the occurrence to the list
                    return new_occ
        return None
    
    
    def __is_recrecognize__(self, occurrence, last_item_index, sequence):
        """
        recursive call for occurrence recognition
        return a boolean whether the events from the last_item_index of the chronicle until its last item have been recognized or not
        """
        chro_size=max( self.sequence.keys() )
        if last_item_index==chro_size:
            return [occurrence]
        
        item_index=last_item_index+1
        
        occurrences = []
        occ = self.__is_complete_recognition__(occurrence, item_index, sequence)
        if ( not (occ is None) ) and self. __is_recrecognize__(occ, item_index, sequence):
            return True
        return False
        

if __name__ == "__main__":

    seq1 = [3,4,'b','a','a',1,3,'c','b','c',5,'c',5]
    seq2 = [(3,1),(4,2),('b',3),('a',14),('a',15),(1,16),(3,27),('c',28),('b',29),('c',50),(5,51),('c',62),(5,73)]

    seq2 = reformat_sequence(seq2)
    seq1 = reformat_sequence(seq1)
    
    seq3 = [('a',1),('a',5),('b',3),('c',14)]
    seq3 = reformat_sequence(seq3)
    print("sorted sequence:" + str(seq3))
    
    #seq = seq1
    seq = seq2
    
    print("sequence: "+str(seq))

    c=Chronicle()
    print(c)
    
    c.add_event(0,'b')
    c.add_event(1,'a')
    
    print(c)
    
    occs=c.recognize(seq)
    print("reco: "+str(occs))
    print("isreco: "+str(c.isrecognize(seq)))
    
    c.add_event(3,'c')
    
    print(c)
    
    occs=c.recognize(seq)
    print("reco: "+str(occs))
    print("isreco: "+str(c.isrecognize(seq)))
    
    c.add_constraint(1,3, (3,45))
    print(c)
    
    occs=c.recognize(seq)
    print("reco: "+str(occs))
    print("isreco: "+str(c.isrecognize(seq)))
    
    c.add_constraint(1,2, (1,1))
    c.add_constraint(0,1, (3,float("inf")))
    c.add_constraint(0,3, (-100,100))
    print(c)
    c.minimize()
    print("minimized")
    print(c)
    
    print(c.to_crs())
    
    occs=c.recognize(seq)
    print("reco: "+str(occs))
    print("isreco: "+str(c.isrecognize(seq)))
    
