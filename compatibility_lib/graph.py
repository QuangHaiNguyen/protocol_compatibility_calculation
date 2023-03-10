#!/usr/bin/env python

__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Development"

"""Provide the definitions for graph, state and transition class.
The module parser will read the data from the json files and create graph,
states, and transitions based on this module.
"""

from enum import Enum, auto
import logging

# create logger
logger = logging.getLogger("GRAPH")

logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.WARNING)
#logger.setLevel(logging.ERROR)
#logger.setLevel(logging.CRITICAL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s - %(funcName)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

class TransitionType(Enum):
    TAU = auto()
    EMISSION = auto()
    RECEPTION = auto()

class StateType(Enum):
    INIT = auto()
    FINAL = auto()
    NORMAL = auto()

class Transition():
    def __init__(self, name: str,
                 type: TransitionType,
                 next_state: str,
                 params: list = []) -> None:
        """__init__ constructore for Transition class

        Args:
            name (str): name of the transition
            type (TransitionType): type of the transition
            next_state (str): name of the next state, where the transition going to
            params (list, optional): parameter list of the transiotion.
                                    Defaults to []. For TAU transition, this argument
                                    must be []

        Raises:
            Exception: Tau transition has list of parameters, i.e., params is
                        not empty
        """
          
        self.name = name
        self.type = type
        self.next_state = next_state
        self.params = params
        
        if self.type == TransitionType.TAU and params:
            raise Exception("Illegal transition. tau has no parameters list")

    def get_param_type(self, param_name: str) -> str:
        """Get the data type of a parameter

        Args:
            param_name (str): name of the parameter

        Returns:
            str: data type or None
        """
        data_type = None
        logger.debug("get data type of [parameter = {}]".format(param_name))
        
        if self.params:
            for param in self.params:
                if param_name in param:
                    data_type = param.split(":")[1]
        else:
            logger.warning("parameters list is empty")
            
        return data_type
    
    def get_data_types(self)-> list:
        """Get list of data type of the transition

        Returns:
            list: list of data type or None
        """
        data_types = []
        if self.params:
            for param in self.params:
                # Only get this type if it is not duplicated
                if param.split(":")[1] not in data_types:
                    data_types.append(param.split(":")[1])        
        else:
            logger.warning("parameters list is empty")
        
        return data_types

class State():
    def __init__(self, name: str,
                 type: StateType,
                 incoming: list = None,
                 outgoing: list = None) -> None:
        """Constructor of the State class
        Args:
            name (str): name of the state
            type (StateType): type of the state
            incoming (list, optional): Incoming transition. Defaults to None.
            outgoing (list, optional): Outgoing transition. Defaults to None.

        Raises:
            Exception: Initial state does not have incoming transition
            Exception: Final state does not have outgoing transition
        """
        self._name = name
        self._type = type
        
        if incoming == None:
            self._incoming = []
        else:
            self._incoming = incoming
            
        if outgoing == None:
            self._outgoing = []
        else:
            self._outgoing = outgoing 
        
        if (self._type == StateType.INIT) and (self._incoming != []):
            raise Exception("Initial state does not have incoming transition")
    
        if (self._type == StateType.FINAL) and (self._outgoing != []):
            logger.debug("outgoing transition = {}".format(self._outgoing))
            raise Exception("Final state does not have outgoing transition")

    def add_incoming_transition(self, transition: Transition):
        """Add an incoming transition

        Args:
            transition (Transition): transition to be added

        Raises:
            Exception: Initial state does not have incoming transition
        """
        if transition is None:
            return
        
        self._incoming.append(transition)
        logger.debug("add new incoming transition [name = {}]".format(transition.name))
        
    
    def add_outgoing_transition(self, transition: Transition):
        """Add an outgoing transition

        Args:
            transition (Transition): transition to be added

        Raises:
            Exception: Final state does not have outgoing transition
        """
        if transition is None:
            return
        
        logger.debug("add new outgoing transition [name = {}]".format(transition.name))
        if self._type == StateType.FINAL:
            raise Exception("Final state does not have outgoing transition")
        else:
            self._outgoing.append(transition)
    
    def get_incoming_transtition(self, name: str) -> Transition:
        """Get an incoming transition

        Args:
            name (str): name of the transition

        Returns:
            Transition: incoming transition
        """
        logger.debug("get incoming transition [name = {}]".format(name))
        ret_transition = None
        
        if self._type != StateType.INIT:
            for transition in self._incoming:
                if name == transition.name:
                    ret_transition = transition
                    logger.debug("transition found")
                    break
        else:
            logger.warning("Initial state has no incoming transitions")
        return ret_transition
    
    def get_outgoing_transtition(self, name: str) -> Transition:
        """Get out going transition

        Args:
            name (str): name of the transition

        Returns:
            Transition: outgoing transition
        """
        logger.debug("get outgoing transition [name = {}]".format(name))
        ret_transition = None
        
        if self._type != StateType.FINAL:
            for transition in self._outgoing:
                if name == transition.name:
                    ret_transition = transition
                    logger.debug("transition found")
                    break
        else:
            logger.warning("Final state has no outgoing transitions")
                    
        return ret_transition
    
    def get_incoming_transitions_list(self) -> list:
        """Get the list on incoming transitions

        Returns:
            list: incoming transitions list
        """
        return self._incoming
    
    def get_outgoing_transitions_list(self) -> list:
        """Get the list of outgoing transitions

        Returns:
            list: outgoing transitions list
        """
        return self._outgoing
        
    
    def get_outgoing_emission_list(self) -> list:
        """Return the list of outgoing emission transition

        Returns:
            list: emission transition
        """
        emission = []
        
        for transition in self._outgoing:
            if transition.type == TransitionType.EMISSION:
                emission.append(transition)

        return emission
    
    
    def get_outgoing_reception_list(self) -> list:
        """Return the list of outgoing reception transition

        Returns:
            list: reception transition
        """
        reception = []
        
        for transition in self._outgoing:
            if transition.type == TransitionType.RECEPTION:
                reception.append(transition)

        return reception
    
    
    def get_outgoing_tau_list(self):
        """Return the list of outgoing tau transition

        Returns:
            list: tau transition
        """
        tau = []
        
        for transition in self._outgoing:
            if transition.type == TransitionType.TAU:
                tau.append(transition)

        return tau
    
    
    def get_imcoming_tau_list(self):
        """Return the list of incoming tau transition

        Returns:
            list: tau transition
        """
        tau = []
        
        for transition in self._incoming:
            if transition.type == TransitionType.TAU:
                tau.append(transition)

        return tau

    
    def get_num_of_incoming_transistions(self) -> int:
        """Get number of incoming transition

        Returns:
            int: number of transitions
        """
        return len(self._incoming)
    
    def get_num_of_outgoing_transitions(self) -> int:
        """Get number of outgoing transition

        _extended_summary_

        Returns:
            int: number of transitions
        """
        return len(self._outgoing)
    
    def is_final_state(self) -> bool:
        """Check if state is final state

        Returns:
            bool: True if final state
        """
        if self._type == StateType.FINAL:
            logger.debug("[state = {}] is FINAL state".format(self._name))
            return True
        else:
            logger.debug("[state = {}] is NOT FINAL state".format(self._name))
            return False
    
    def is_initial_state(self) -> bool:
        """check if state is initial state

        Returns:
            bool: True if initial state
        """
        if self._type == StateType.INIT:
            logger.debug("[state = {}] is INIT state".format(self._name))
            return True
        else:
            logger.debug("[state = {}] is NOT INIT state".format(self._name))
            return False
        
    def get_name(self) -> str:
        """Get name of the state

        Returns:
            str: name of the state
        """
        return self._name
    
    def print_state(self):
        print("*************************************************************")
        print("State report")
        print("Name: {}".format(self._name))
        print("Type: {}".format(self._type))
        
        print("Incoming Transitions:")
        for transition in self._incoming:
            print("    ---------------------------------------")
            print("    Name: {}".format(transition.name))
            print("    Type: {}".format(transition.type))
            print("    num of params: {}".format(len(transition.params)))
            print("    params:")
            for param in transition.params:
                print("        {}".format(param))
        
        print("Outgoing Transitions:")
        for transition in self._outgoing:
            print("    ---------------------------------------")
            print("    Name: {}".format(transition.name))
            print("    Type: {}".format(transition.type))
            print("    num of params: {}".format(len(transition.params)))
            print("    params:")
            for param in transition.params:
                print("        {}".format(param))
            
            
class Graph():
    def __init__(self, name: str, states: list = None) -> None:

        """Constructor of Graph class

        Args:
            name (str): name of the graph
            states (list, optional): states of the graph. Defaults to [].
        """
        self._name = name

        if states == None:
            self._states = []
        else:
            self._states = states
        
    def add_state(self, state: State):
        """Add new state to the graph

        Args:
            state (State): new state
        """
        if state != None:
            logger.debug("add [state = {}] to graph".format(state.get_name()))
            self._states.append(state)
        
    def get_state(self, state_name: str) ->State:
        """Get a state

        Args:
            state_name (str): name of the state

        Returns:
            State: state or None
        """
        logger.debug("looking for [state = {}]".format(state_name))
        ret_state = None
    
        for state in self._states:
            if state_name == state.get_name():
                ret_state = state
                logger.debug("state found")
                break
            else:
                pass
        
        if ret_state == None:
            logger.warning("state not found")
        return ret_state
    
    def get_states_list(self) -> list:
        """Get all the states of the graph

        Returns:
            list: state list
        """
        return self._states
    
    def print_graph(self):
        print()
        print("####################################################################################")
        print("#")
        print("# Graph Name: {}".format(self._name))
        print("# Number of states: {}".format(len(self._states)))
        print("#")
        print("####################################################################################")
        print("#")
        for state in self._states:
            state.print_state()
        print("#")
        print("####################################################################################")
        print()

        
    
if __name__ == '__main__':
    pass