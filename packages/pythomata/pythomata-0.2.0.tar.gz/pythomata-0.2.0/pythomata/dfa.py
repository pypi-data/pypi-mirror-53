# -*- coding: utf-8 -*-
"""This module contains the implementation of the DFA object and related components."""
import itertools
from copy import copy, deepcopy
from typing import List, Set, Tuple, Iterable, Optional, FrozenSet, Hashable, cast, Dict

import graphviz
import queue

from pythomata._internal_utils import (
    _check_initial_state_in_states,
    _check_accepting_states_in_states,
    _check_transition_function_is_valid_wrt_states_and_alphabet,
    _check_reserved_state_names_not_used,
    _check_reserved_symbol_names_not_used,
    _generate_sink_name,
    _check_at_least_one_state,
    greatest_fixpoint,
    least_fixpoint,
    _extract_states_from_transition_function,
    _check_no_none_states,
)
from pythomata.base import State, TransitionFunction, Symbol


class DFA(object):
    """This class implements a DFA."""

    def __init__(
        self,
        states: Set[State],
        alphabet: Set[Symbol],
        initial_state: State,
        accepting_states: Set[State],
        transition_function: TransitionFunction,
    ):
        """
        Initialize a DFA.

        :param states: the set of states.
        :param alphabet: the alphabet
        :param initial_state: the initial state
        :param accepting_states: the set of accepting states
        :param transition_function: the transition function
        """
        self._check_input(
            states, alphabet, initial_state, accepting_states, transition_function
        )

        self._states = frozenset(states)  # type: FrozenSet[State]
        self._alphabet = frozenset(alphabet)  # type: FrozenSet[Symbol]
        self._initial_state = initial_state  # type: State
        self._accepting_states = frozenset(accepting_states)  # type: FrozenSet[State]
        self._transition_function = transition_function  # type: TransitionFunction

        self._build_indexes()

    @property
    def states(self) -> FrozenSet[State]:
        """Get the set of states.."""
        return self._states

    @property
    def alphabet(self) -> FrozenSet[Symbol]:
        """Get the alphabet."""
        return self._alphabet

    @property
    def initial_state(self) -> State:
        """Get the initial state."""
        return self._initial_state

    @property
    def accepting_states(self) -> FrozenSet[State]:
        """Get the set of accepting states."""
        return self._accepting_states

    @property
    def transition_function(self) -> TransitionFunction:
        """Get the transition function."""
        return self._transition_function

    @staticmethod
    def from_transitions(initial_state, accepting_states, transition_function):
        # type: (State, Set[State], TransitionFunction) -> DFA
        """
        Initialize a DFA without explicitly specifying the set of states and the alphabet.

        :param initial_state: the initial state.
        :param accepting_states: the accepting state.
        :param transition_function: the transition function.
        :return: the DFA.
        """
        states, alphabet = _extract_states_from_transition_function(transition_function)

        return DFA(
            states, alphabet, initial_state, accepting_states, transition_function
        )

    @classmethod
    def _check_input(
        cls,
        states: Set[State],
        alphabet: Set[Symbol],
        initial_state: State,
        accepting_states: Set[State],
        transition_function: TransitionFunction,
    ):
        """
        Check the consistency of the constructor parameters.

        :return: None
        :raises ValueError: if some consistency check fails.
        """
        _check_at_least_one_state(states)
        _check_no_none_states(states)
        _check_reserved_state_names_not_used(states)
        _check_reserved_symbol_names_not_used(alphabet)
        _check_initial_state_in_states(initial_state, states)
        _check_accepting_states_in_states(accepting_states, states)
        _check_transition_function_is_valid_wrt_states_and_alphabet(
            transition_function, states, alphabet
        )

    def _build_indexes(self):
        """Build indexes for several components of the object."""
        self._idx_to_state = list(self._states)
        self._state_to_idx = dict(map(reversed, enumerate(self._idx_to_state)))
        self._idx_to_symbol = list(self._alphabet)
        self._symbol_to_idx = dict(map(reversed, enumerate(self._idx_to_symbol)))

        # state -> action -> state
        self._idx_transition_function = {
            self._state_to_idx[state]: {
                self._symbol_to_idx[symbol]: self._state_to_idx[
                    self._transition_function[state][symbol]
                ]
                for symbol in self._transition_function.get(state, {})
            }
            for state in self._states
        }

        # state -> (action, state)
        self._idx_delta_by_state = {}
        for s in self._idx_transition_function:
            self._idx_delta_by_state[s] = set(
                list(self._idx_transition_function[s].items())
            )

        self._idx_initial_state = self._state_to_idx[self._initial_state]
        self._idx_accepting_states = frozenset(
            self._state_to_idx[s] for s in self._accepting_states
        )

    def is_complete(self) -> bool:
        """
        Check whether the automaton is complete.

        :return: True if the automaton is complete, False otherwise.
        """
        complete_number_of_transitions = len(self._states) * len(self._alphabet)
        current_number_of_transitions = sum(
            len(self._transition_function[state]) for state in self._transition_function
        )
        return complete_number_of_transitions == current_number_of_transitions

    def complete(self) -> "DFA":
        """
        Complete the DFA.

        :return: the completed DFA, if it's not already complete.
               | Otherwise, return the caller instance.
        """
        if self.is_complete():
            return self
        else:
            return self._complete()

    def _complete(self) -> "DFA":
        """
        Complete the DFA.

        :return: the completed DFA.
        """
        sink_state = _generate_sink_name(self._states)
        transitions = deepcopy(self._transition_function)

        # for every missing transition, add a transition towards the sink state.
        for state in self._states:
            for action in self._alphabet:
                cur_transitions = self._transition_function.get(state, {})
                end_state = cur_transitions.get(action, None)  # type: ignore
                if end_state is None:
                    transitions.setdefault(state, {})[action] = sink_state

        # for every action, add a transition from the sink state to the sink state
        for action in self._alphabet:
            transitions.setdefault(sink_state, {})[action] = sink_state

        return DFA(
            set(self._states.union({sink_state})),
            set(self._alphabet),
            self._initial_state,
            set(self._accepting_states),
            dict(transitions),
        )

    def minimize(self) -> 'DFA':
        """
        Minimize the DFA.

        :return: the minimized DFA.
        """
        dfa = self
        dfa = dfa.complete()

        def greatest_fixpoint_condition(el: Tuple[int, int], current_set: Set):
            """Condition to say whether the pair must be removed from the bisimulation relation."""
            s, t = el
            s_is_final = s in dfa._idx_accepting_states
            t_is_final = t in dfa._idx_accepting_states
            if s_is_final and not t_is_final or not s_is_final and t_is_final:
                return True

            s_transitions = dfa._idx_transition_function.get(s, {})
            t_transitions = dfa._idx_transition_function.get(t, {})

            for a, s_prime in s_transitions.items():
                t_prime = t_transitions.get(a, None)
                if t_prime is not None and (s_prime, t_prime) in current_set:
                    continue
                else:
                    return True

            for a, t_prime in t_transitions.items():
                s_prime = s_transitions.get(a, None)
                if s_prime is not None and (s_prime, t_prime) in current_set:
                    continue
                else:
                    return True

            return False

        result = greatest_fixpoint(
            set(
                itertools.product(
                    range(len(dfa._idx_to_state)), range(len(dfa._idx_to_state))
                )
            ),
            condition=greatest_fixpoint_condition,
        )

        state2equiv_class = {}  # type: Dict[int, FrozenSet[int]]
        for (s, t) in result:
            state2equiv_class.setdefault(s, frozenset())
            state2equiv_class[s] = state2equiv_class[s].union(frozenset({t}))
        equivalence_classes = set(map(lambda x: frozenset(x), state2equiv_class.values()))
        equiv_class2new_state = dict(
            (ec, i) for i, ec in enumerate(equivalence_classes)
        )

        new_transition_function = {}  # type: TransitionFunction
        for state in dfa._idx_delta_by_state:
            new_state = equiv_class2new_state[state2equiv_class[state]]
            for action, next_state in dfa._idx_delta_by_state[state]:
                new_next_state = equiv_class2new_state[state2equiv_class[next_state]]

                new_transition_function.setdefault(new_state, {})[
                    dfa._idx_to_symbol[action]
                ] = new_next_state

        new_states = frozenset(equiv_class2new_state.values())
        new_initial_state = equiv_class2new_state[
            state2equiv_class[dfa._idx_initial_state]
        ]
        new_final_states = frozenset(
            s
            for s in set(
                equiv_class2new_state[state2equiv_class[old_state]]
                for old_state in dfa._idx_accepting_states
            )
        )

        new_dfa = DFA(
            set(new_states),
            set(dfa._alphabet),
            new_initial_state,
            set(new_final_states),
            new_transition_function,
        )
        return new_dfa

    def reachable(self):
        """
        Get the equivalent reachable automaton.

        :return: the reachable DFA.
        """
        def reachable_fixpoint_rule(current_set: Set) -> Iterable:
            result = set()
            for el in current_set:
                for a in self._idx_transition_function.get(el, {}):
                    result.add(self._idx_transition_function[el][a])
            return result

        result = least_fixpoint({self._idx_initial_state}, reachable_fixpoint_rule)

        idx_new_states = result
        new_transition_function = {}
        for s in idx_new_states:
            for a in self._idx_transition_function.get(s, {}):
                next_state = self._idx_transition_function[s][a]
                if next_state in idx_new_states:
                    new_transition_function.setdefault(self._idx_to_state[s], {})
                    state = self._idx_to_state[s]
                    new_transition_function[state][
                        self._idx_to_symbol[a]
                    ] = self._idx_to_state[next_state]

        new_states = set(map(lambda x: self._idx_to_state[x], idx_new_states))
        new_final_states = new_states.intersection(self._accepting_states)

        return DFA(
            new_states,
            set(self._alphabet),
            self._initial_state,
            new_final_states,
            new_transition_function,
        )

    def coreachable(self) -> 'DFA':
        """
        Get the equivalent co-reachable automaton.

        :return: the co-reachable DFA.
        """
        # least fixpoint

        def coreachable_fixpoint_rule(current_set: Set) -> Iterable:
            result = set()
            for s in range(len(self._states)):
                for a in self._idx_transition_function.get(s, {}):
                    next_state = self._idx_transition_function[s][a]
                    if next_state in current_set:
                        result.add(s)
                        break
            return result

        result = least_fixpoint(
            set(self._idx_accepting_states), coreachable_fixpoint_rule
        )

        idx_new_states = result
        if self._idx_initial_state not in idx_new_states:
            return EmptyDFA(alphabet=set(self._alphabet))

        new_states = set(map(lambda x: self._idx_to_state[x], idx_new_states))
        new_transition_function = {}  # type: TransitionFunction
        for s in idx_new_states:
            for a in self._idx_transition_function.get(s, {}):
                next_state = self._idx_transition_function[s][a]
                if next_state in idx_new_states:
                    new_transition_function.setdefault(self._idx_to_state[s], {})
                    state = self._idx_to_state[s]
                    new_transition_function[state][
                        self._idx_to_symbol[a]
                    ] = self._idx_to_state[next_state]

        return DFA(
            new_states,
            set(self._alphabet),
            self._initial_state,
            set(self._accepting_states),
            new_transition_function,
        )

    def trim(self) -> 'DFA':
        """
        Trim the automaton.

        :return: the trimmed DFA.
        """
        dfa = self
        dfa = dfa.complete()
        dfa = dfa.reachable()
        dfa = dfa.coreachable()
        return dfa

    def accepts(self, word: List[Symbol]) -> bool:
        """
        Check if the automaton accepts a word.

        :param word: the list of symbols.
        :return: True if the word is accepted by the automaton, False otherwise.
        """
        current_state = self._initial_state

        for char in word:
            if (
                current_state not in self._transition_function
                or char not in self._transition_function[current_state]
            ):
                return False
            else:
                current_state = self._transition_function[current_state][char]

        return current_state in self._accepting_states

    def to_dot(self, path: str, title: Optional[str] = None) -> None:
        """
        Print the automaton to a dot file and a svg file.

        :param path: the path where to save the file.
        :param title: the title of the DFA
        :return: None
        """
        g = graphviz.Digraph(format="svg")
        g.node("fake", style="invisible")
        for state in self._states:
            if state == self._initial_state:
                if state in self._accepting_states:
                    g.node(str(state), root="true", shape="doublecircle")
                else:
                    g.node(str(state), root="true")
            elif state in self._accepting_states:
                g.node(str(state), shape="doublecircle")
            else:
                g.node(str(state))

        g.edge("fake", str(self._initial_state), style="bold")
        for start in self._transition_function:
            for symbol, end in self._transition_function[start].items():
                g.edge(str(start), str(end), label=str(symbol))

        if title:
            g.attr(label=title)
            g.attr(fontsize="20")

        g.render(filename=path)
        return

    def levels_to_accepting_states(self) -> dict:
        """
        Return a dict from states to level.

        i.e. the number of steps to reach any accepting state.
        level = -1 if the state cannot reach any accepting state
        """
        res = {accepting_state: 0 for accepting_state in self._accepting_states}
        level = 0

        # least fixpoint
        z_current = set()  # type: Set[Hashable]
        z_next = set(self._accepting_states)

        while z_current != z_next:
            level += 1
            z_current = z_next
            z_next = copy(z_current)
            for state in self._transition_function:
                for action in self._transition_function[state]:
                    if state in z_current:
                        continue
                    next_state = self._transition_function[state][action]
                    if next_state in z_current:
                        z_next.add(state)
                        res[state] = level
                        break

        z_current = z_next
        for failure_state in filter(lambda x: x not in z_current, self._states):
            res[failure_state] = -1

        return res

    def renumbering(self) -> "DFA":
        """Deterministically renumber all the states.

        :raises ValueError: if the symbols of the transitions
                          | cannot be sorted uniquely
        """
        idx = 0
        visited_states = {self._idx_initial_state}
        q = queue.Queue()  # type: queue.Queue

        old_state_to_number = {}

        q.put(self._idx_initial_state)
        while not q.empty():
            current_state = q.get()
            old_state_to_number[current_state] = idx
            idx += 1

            try:
                next_actions = sorted(
                    self._idx_transition_function[current_state],
                    key=lambda x: self._idx_to_symbol[x],
                )
            except TypeError:
                raise TypeError("Cannot sort the transition symbols.")

            for action in next_actions:
                cur_tf = self._idx_transition_function[current_state]
                next_state = cur_tf[action]
                if next_state not in visited_states:
                    visited_states.add(next_state)
                    q.put(next_state)

        new_states = set(range(len(old_state_to_number)))
        new_initial_state = old_state_to_number[self._idx_initial_state]
        new_accepting_states = {
            old_state_to_number[x] for x in self._idx_accepting_states
        }
        new_transition_function = {
            old_state_to_number[start]: {
                self._idx_to_symbol[symbol]: old_state_to_number[end]
                for symbol, end in self._idx_transition_function[start].items()
            }
            for start in self._idx_transition_function
        }

        return DFA(
            cast(Set[Hashable], new_states),
            set(self._alphabet),
            new_initial_state,
            cast(Set[Hashable], new_accepting_states),
            cast(TransitionFunction, new_transition_function),
        )

    def __eq__(self, other):
        """Check equality with another object."""
        if not isinstance(other, DFA):
            return False

        return (
            self._states == other._states
            and self._alphabet == other._alphabet
            and self._initial_state == other._initial_state
            and self._accepting_states == other._accepting_states
            and self._transition_function == other._transition_function
        )


class EmptyDFA(DFA):
    """Implementation of an empty DFA."""

    def __init__(self, alphabet: Set[Symbol] = None):
        """Initialize an empty DFA."""
        alphabet = alphabet if alphabet is not None else set()
        super().__init__({"0"}, alphabet, "0", set(), {})

    def __eq__(self, other):
        """Check equality with another object."""
        return type(self) == type(other) == EmptyDFA
