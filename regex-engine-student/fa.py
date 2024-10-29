from regex import parse_regex, RStar, RUnion, RConcat, RSingle, RNoString, RConcat, REmptyString
from collections import deque
import string 

SUPPORTED_SYMBOLS = list(string.ascii_lowercase)
EPSILON = ""
class NFAState:
    _id_counter = 0

    def __init__(self, is_final):
        self.id = NFAState._id_counter
        NFAState._id_counter += 1
        self.is_final = is_final
        self.transitions = dict()

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(state)

class NFA:
    def __init__(self, start_state, states):
        self.start_state = start_state
        self.states = states
        self.transition_table = self._make_transition_table()

    def _make_transition_table(self):
        table = {}
        raise NotImplementedError("Require student implementation")

    def is_final_state(self, state_id):
            for state in self.states:
                if state.id == state_id:
                    return state.is_final
            return False
        
    def accepts(self, input_string):
        queue = deque([(self.start_state.id, input_string)])

        while queue:
            current_state_id, remaining_input = queue.popleft()
            if not remaining_input and self.is_final_state(current_state_id):
                return True

            if remaining_input:
                current_char = remaining_input[0]
                rest_input = remaining_input[1:]

                if current_state_id not in self.transition_table:
                    # state is not listed in the table, implying it has no outgoing transitions
                    # (it is also OK to list a state in the table with an empty dict indicating no outgoing transitions)
                    continue

                if current_char in self.transition_table[current_state_id]:
                    target_states = self.transition_table[current_state_id][current_char]
                    for next_state_id in target_states:
                        queue.append((next_state_id, rest_input))
                # else no valid transition for this character from this state

            if current_state_id in self.transition_table and EPSILON in self.transition_table[current_state_id]:
                target_states = self.transition_table[current_state_id][EPSILON]
                for next_state_id in target_states:
                    queue.append((next_state_id, remaining_input))

        return False

    """
    This function implements the Thompson Construct from the Dragon Book. 
    You should refer to the book and complete the code based on the given function strucuture.
    """
    @classmethod
    def from_regex(cls, regex):
        match regex:
            case REmptyString():
                start = NFAState(False)
                end = NFAState(True)
                start.add_transition(EPSILON, end)
                return cls(start, {start, end})

            case RNoString():
                start = NFAState(False)
                return cls(start, {start})

            case RSingle():
                start = NFAState(False)
                end = NFAState(True)
                start.add_transition(regex.char, end)
                return cls(start, {start, end})

            case RConcat():
                raise NotImplementedError("Require student implementation")

            case RUnion():
                raise NotImplementedError("Require student implementation")

            case RStar():
                raise NotImplementedError("Require student implementation")

        raise ValueError("Unknown regex type")

class DFAState():
    _id_counter = 0

    def __init__(self, is_final, nfa_states):
        self.id = DFAState._id_counter
        DFAState._id_counter += 1
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state

class DFA:
    def __init__(self, start_state, states):
        self.start_state = start_state
        self.states = states
        self.transition_table = self._make_transition_table()

    def _make_transition_table(self):
        raise NotImplementedError("Require student implementation")

    def accepts(self, input_string):
        raise NotImplementedError("Require student implementation")

    @classmethod
    def from_nfa(cls, nfa):
        def epsilon_closure(states):
            raise NotImplementedError("Require student implementation")

        def move(n_states, a):
            raise NotImplementedError("Require student implementation")

        raise NotImplementedError("Require student implementation")

