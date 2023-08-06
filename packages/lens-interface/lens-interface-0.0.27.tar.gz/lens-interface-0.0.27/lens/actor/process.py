from __future__ import absolute_import, division, print_function

import collections
import numpy as np
import lens.actor.emitter as emit


target_key = '__target'
exchange_key = '__exchange'  # TODO exchange key is also being set in lattice_compartment

def npize(d):
    ''' Turn a dict into an ordered set of keys and values. '''

    ordered = [[key, value] for key, value in d.iteritems()]
    keys = [key for key, _ in ordered]
    values = np.array([value for _, value in ordered], np.float64)

    return keys, values

def update_delta(key, state_dict, current_value, new_value):
    return current_value + new_value, {}

def update_set(key, state_dict, current_value, new_value):
    return new_value, {}

def update_target(key, state_dict, current_value, new_value):
    return current_value, {key + target_key: new_value}

def accumulate_delta(key, state_dict, current_value, new_value):
    new_key = key + exchange_key
    return current_value, {new_key: state_dict[new_key] + new_value}

updater_library = {
    'delta': update_delta,
    'set': update_set,
    'target': update_target,
    'accumulate': accumulate_delta}


KEY_TYPE = 'U31'


class State(object):
    ''' Represents a set of named values. '''

    def __init__(self, initial_state={}, updaters={}):
        ''' Keys and state initialize empty, with a maximum key length of 31. '''

        self.keys = np.array([], dtype=KEY_TYPE) # maximum key length
        self.state = np.array([], dtype=np.float64)
        self.updaters = updaters

        self.initialize_state(initial_state)

    def initialize_state(self, initial):
        ''' Provide an initial value for any keys in this dict. '''

        self.declare_state(initial.keys())
        self.apply_delta(initial)

    def merge_updaters(self, updaters):
        ''' Merge in a new set of updaters '''

        self.updaters.merge(updaters)

    def sort_keys(self):
        ''' re-sort keys after adding some '''

        sort = np.argsort(self.keys)
        self.keys = self.keys[sort]
        self.state = self.state[sort]

    def declare_state(self, keys):
        ''' Initialize values for the given keys to zero. '''

        existing_keys = np.isin(keys, self.keys)
        novel = np.array(keys, dtype=KEY_TYPE)[~existing_keys]

        self.keys = np.concatenate([self.keys, novel])
        self.state = np.concatenate([self.state, np.zeros(novel.shape)])
        self.sort_keys()

    def index_for(self, keys):
        if self.keys.size == 0:
            return np.array([])
        return np.searchsorted(self.keys, keys)

    def assign_values(self, values_dict):
        ''' Assign a dict of keys and values to the state. '''
        if self.keys.size == 0:
            return
        keys, values = npize(values_dict)
        index = self.index_for(keys)
        self.state[index] = values

    def apply_delta(self, delta):
        ''' Apply a dict of keys and deltas to the state. '''
        if self.keys.size == 0:
            return
        keys, values = npize(delta)
        index = self.index_for(keys)
        self.state[index] += values

    def apply_deltas(self, deltas):
        ''' Apply a list of deltas to the state. '''

        for delta in deltas:
            self.apply_delta(delta)

    def apply_update(self, update):
        ''' Apply a dict of keys and values to the state using its updaters. '''

        if self.keys.size == 0:
            return
        keys, values = npize(update)
        index = self.index_for(keys)
        state_dict = dict(zip(self.keys, self.state))

        for index, key, value in zip(index, keys, values):
            # updater can be a function or a key into the updater library
            updater = self.updaters.get(key, 'delta')
            if not callable(updater):
                updater = updater_library[updater]

            self.new_state[index], other_updates = updater(
                key,
                state_dict,
                self.new_state[index],
                value)

            for other_key, other_value in other_updates.iteritems():
                other_index = self.index_for(other_key)
                self.new_state[other_index] = other_value

    def apply_updates(self, updates):
        ''' Apply a list of updates to the state '''

        for update in updates:
            self.apply_update(update)

    def prepare(self):
        ''' Prepares for state updates by creating new copy of existing state '''

        self.new_state = np.copy(self.state)

    def proceed(self):
        ''' Once all updates are complete, swaps out state for newly calculated state '''

        self.state = self.new_state

    def state_for(self, keys):
        ''' Get the current state of these keys as a dict of values. '''

        if self.keys.size == 0:
            return {}
        index = self.index_for(keys)
        return dict(zip(keys, self.state[index]))

    def to_dict(self):
        ''' Get the current state of all keys '''

        return {
            self.keys[index]: self.state[index]
            for index in range(self.keys.shape[0])}


class Process(object):
    def __init__(self, roles, parameters=None, deriver=False):
        ''' Declare what roles this process expects. '''

        self.roles = roles
        self.parameters = parameters or {}
        self.states = None
        self.deriver = deriver

    def default_state(self):
        return {}

    def default_emitter_keys(self):
        return {}

    def default_updaters(self):
        return {}

    # def default_parameters(self):
    #     return {}

    def assign_roles(self, states):
        '''
        Provide States for some or all of the roles this Process expects.

        Roles and States must have the same keys. '''

        self.states = states
        for role, state in self.states.iteritems():
            state.declare_state(self.roles[role])

    def update_for(self, timestep):
        ''' Called each timestep to find the next state for this process. '''

        states = {
            role: self.states[role].state_for(self.roles[role])
            for role, values in self.roles.iteritems()}

        return self.next_update(timestep, states)

    def next_update(self, timestep, states):
        '''
        Find the next update given the current states this process cares about.

        This is the main function a new process would override.'''

        return {
            role: {}
            for role, values in self.roles.iteritems()}


def connect_topology(processes, states, topology):
    ''' Given a set of processes and states, and a description of the connections
        between them, link the roles in each process to the state they refer to.'''

    for name, process in processes.iteritems():
        connections = topology[name]
        roles = {
            role: states[key]
            for role, key in connections.iteritems()}

        process.assign_roles(roles)

def merge_initial_states(processes):
    initial_state = {}
    for process_id, process in processes.iteritems():
        default = process.default_state()
        dict_merge(initial_state, default)
    return initial_state

def dict_merge(dct, merge_dct):
    ''' Recursive dict merge '''
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]

class Compartment(object):
    ''' Track a set of processes and states and the connections between them. '''

    def __init__(self, processes, states, configuration):
        ''' Given a set of processes and states, and a topology describing their
            connections, perform those connections. '''

        self.local_time = 0.0
        self.time_step = configuration.get('time_step', 1.0)

        self.derivers = {
            name: process
            for name, process in processes.iteritems()
            if process.deriver}

        self.processes = {
            name: process
            for name, process in processes.iteritems()
            if not process.deriver}

        self.states = states
        self.topology = configuration['topology']

        # emitter
        self.emitter_keys = configuration['emitter'].get('keys')
        self.emitter = configuration['emitter'].get('object')

        connect_topology(processes, self.states, self.topology)
        self.run_derivers(0)

    def run_derivers(self, timestep):
        ''' Run each deriver process to set up state for subsequent processes. '''

        for name, deriver in self.derivers.iteritems():
            all_updates = deriver.update_for(timestep)
            for role, update in all_updates.iteritems():
                key = self.topology[name][role]
                self.states[key].assign_values(update)

    def update(self, timestep):
        ''' Run each process for the given time step and update the related states. '''

        updates = {}
        for name, process in self.processes.iteritems():
            update = process.update_for(timestep)
            for role, deltas in update.iteritems():
                key = self.topology[name][role]

                if not updates.get(key):
                    updates[key] = []
                updates[key].append(deltas)

        for key in self.states.keys():
            self.states[key].prepare()

        for key, update in updates.iteritems():
            self.states[key].apply_updates(update)

        for key in self.states.keys():
            self.states[key].proceed()

        self.run_derivers(timestep)

        self.local_time += timestep

        # run emitters
        self.emit_data()

    def current_state(self):
        ''' Construct the total current state from the existing substates. '''

        return {
            key: state.to_dict()
            for key, state in self.states.iteritems()}

    def current_parameters(self):
        return {
            name: process.parameters
            for name, process in self.processes.iteritems()}

    def time(self):
        return self.local_time

    def emit_data(self):
        data = {}
        for role_key, emit_keys in self.emitter_keys.iteritems():
            data[role_key] = self.states[role_key].state_for(emit_keys)

        data.update({
            'type': 'compartment',
            'time': self.time()})

        self.emitter.emit(data)



def test_compartment():
    # simplest possible metabolism
    class Metabolism(Process):
        def __init__(self, initial_parameters={}):
            roles = {'pool': ['GLC', 'MASS']}
            parameters = {'mass_conversion_rate': 1}
            parameters.update(initial_parameters)

            super(Metabolism, self).__init__(roles, parameters)

        def next_update(self, timestep, states):
            update = {}
            glucose_required = timestep / self.parameters['mass_conversion_rate']
            if states['pool']['GLC'] >= glucose_required:
                update = {
                    'pool': {
                        'GLC': -2,
                        'MASS': 1}}

            return update

    # simplest possible transport
    class Transport(Process):
        def __init__(self, initial_parameters={}):
            roles = {
                'external': ['GLC'],
                'internal': ['GLC']}
            parameters = {'intake_rate': 2}
            parameters.update(initial_parameters)

            super(Transport, self).__init__(roles, parameters)

        def next_update(self, timestep, states):
            update = {}
            intake = timestep * self.parameters['intake_rate']
            if states['external']['GLC'] >= intake:
                update = {
                    'external': {'GLC': -2, 'MASS': 1},
                    'internal': {'GLC': 2}}

            return update

    class DeriveVolume(Process):
        def __init__(self, initial_parameters={}):
            roles = {
                'compartment': ['MASS', 'DENSITY', 'VOLUME']}
            parameters = {}

            super(DeriveVolume, self).__init__(roles, parameters, deriver=True)

        def next_update(self, timestep, states):
            volume = states['compartment']['MASS'] / states['compartment']['DENSITY']
            update = {
                'compartment': {'VOLUME': volume}}

            return update

    # declare the processes
    processes = {
        'metabolism': Metabolism(initial_parameters={'mass_conversion_rate': 0.5}), # example of overriding default parameters
        'transport': Transport(),
        'external_volume': DeriveVolume(),
        'internal_volume': DeriveVolume()}

    def update_mass(key, state, current, new):
        return current / (current + new), {}

    # declare the states
    states = {
        'periplasm': State(
            initial_state={'GLC': 20, 'MASS': 100, 'DENSITY': 10},
            updaters={'MASS': update_mass}),
        'cytoplasm': State(
            initial_state={'MASS': 3, 'DENSITY': 10},
            updaters={'DENSITY': 'set'})}

    # hook up the states to the roles in each process
    topology = {
        'metabolism': {
            'pool': 'cytoplasm'},

        'transport': {
            'external': 'periplasm',
            'internal': 'cytoplasm'},

        'external_volume': {
            'compartment': 'periplasm'},

        'internal_volume': {
            'compartment': 'cytoplasm'}}

    emitter = emit.get_emitter({
        'type': 'print',
        'keys': {
            'periplasm': ['GLC', 'MASS'],
            'cytoplasm': ['MASS']}})

    configuration = {
        'time_step': 1.0,
        'topology': topology,
        'emitter': emitter}

    # create the compartment (which automatically hooks everything up)
    compartment = Compartment(processes, states, configuration)
    timestep = 1

    # print initial parameters and state
    print(compartment.current_parameters())
    print(compartment.current_state())

    for steps in np.arange(13):
        # run the simulation
        compartment.update(timestep)
        print(compartment.current_state())


if __name__ == '__main__':
    test_compartment()
