#fa.py
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
        for state in self.states:
            transitions = {}
            for symbol, target_states in state.transitions.items():
                transitions[symbol] = {s.id for s in target_states}
            if transitions:
                table[state.id] = transitions
            else:
                table[state.id] = {}  # Empty dict if no transitions

        return table
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

            # Implement the concatenation case, aligning with Fig. 3.41 in the Dragon Book
            case RConcat(left=left, right=right):
                # Recursively create NFA for each part (N(s) and N(t))
                nfa_left = cls.from_regex(left)
                nfa_right = cls.from_regex(right)

                # Find and deactivate the final state of N(s)
                nfa_left_accept_state = next(state for state in nfa_left.states if state.is_final)
                nfa_left_accept_state.is_final = False

                # Connect N(s)'s final state to the start of N(t) with epsilon transition
                nfa_left_accept_state.add_transition(EPSILON, nfa_right.start_state)

                # Combine all states and return the full NFA
                all_states = nfa_left.states.union(nfa_right.states)
                return cls(nfa_left.start_state, all_states)

            # Implement the union case, aligning with Fig. 3.40 in the Dragon Book
            case RUnion(left=left, right=right):
                # Recursively create NFA for each part (N(s) and N(t))
                nfa_left = cls.from_regex(left)
                nfa_right = cls.from_regex(right)

                # Create new start and accept states for the union
                new_start = NFAState(False)
                new_accept = NFAState(True)

                # Epsilon transitions from new start to both N(s) and N(t) start states
                new_start.add_transition(EPSILON, nfa_left.start_state)
                new_start.add_transition(EPSILON, nfa_right.start_state)

                # Connect each NFA's final state to the new accept state with epsilon transitions
                nfa_left_accept_state = next(state for state in nfa_left.states if state.is_final)
                nfa_right_accept_state = next(state for state in nfa_right.states if state.is_final)

                nfa_left_accept_state.is_final = False
                nfa_right_accept_state.is_final = False

                # Add epsilon transitions from each sub-NFA’s accept state to the new accept
                nfa_left_accept_state.add_transition(EPSILON, new_accept)
                nfa_right_accept_state.add_transition(EPSILON, new_accept)

                # Combine all states and return the full NFA
                all_states = {new_start, new_accept}.union(nfa_left.states).union(nfa_right.states)
                return cls(new_start, all_states)

            # Implement the star case, aligning with Fig. 3.42 in the Dragon Book
            case RStar(expr=expr):
                # Recursively create NFA for the inner expression (N(s))
                nfa_expr = cls.from_regex(expr)

                # Create new start and accept states for the star operation
                new_start = NFAState(False)
                new_accept = NFAState(True)

                # Epsilon transition from new start state to both N(s) start and new accept state
                new_start.add_transition(EPSILON, nfa_expr.start_state)
                new_start.add_transition(EPSILON, new_accept)

                # Deactivate the final state of N(s) and create loops back to start
                nfa_expr_accept_state = next(state for state in nfa_expr.states if state.is_final)
                nfa_expr_accept_state.is_final = False

                # Loop back from N(s)'s final state to its start, and to the new accept state
                nfa_expr_accept_state.add_transition(EPSILON, nfa_expr.start_state)
                nfa_expr_accept_state.add_transition(EPSILON, new_accept)

                # Combine all states and return the full NFA
                all_states = {new_start, new_accept}.union(nfa_expr.states)
                return cls(new_start, all_states)

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

