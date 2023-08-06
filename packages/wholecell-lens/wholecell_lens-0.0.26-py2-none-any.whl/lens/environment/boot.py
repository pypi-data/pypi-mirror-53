'''
boot functions for initialize environment simulations:
Can be called from the command line
by specifying an environment "agent_type" and an outer-id:

>> python -m lens.environment.boot --type lattice --id lattice

boot functions for compartment simulations:
Can be called from the command line
after booting an environmental "outer" simulation and passing in the outer-id, the agent_type:

>> python -m lens.environment.boot --outer-id 'outer-id' --type 'agent_type'

Once an environment and agent are booted, they can be triggered with:

>> python -m lens.environment.control run --id 'outer-id'

'''

from __future__ import absolute_import, division, print_function

import os
import shutil

from lens.actor.inner import Inner
from lens.actor.outer import Outer
from lens.actor.boot import BootAgent
from lens.actor.emitter import get_emitter

from lens.environment.lattice import EnvironmentSpatialLattice
from lens.environment.make_media import Media
from lens.environment.lattice_compartment import generate_lattice_compartment

# processes
from lens.processes.transport_lookup import TransportLookup
from lens.processes.CovertPalsson2002_metabolism import Metabolism
from lens.processes.Kremling2007_transport import Transport
from lens.processes.growth import Growth
from lens.processes.Endres2006_chemoreceptor import ReceptorCluster

# composites
from lens.composites.Covert2008 import initialize_covert2008
from lens.composites.growth_division import initialize_growth_division

def wrap_boot(initialize, initial_state):
    def boot(agent_id, agent_type, agent_config):
        initial_state.update(agent_config.get('declare', {}))
        agent_config['declare'] = initial_state  # 'declare' is for the environment

        return Inner(
            agent_id,
            agent_type,
            agent_config,
            initialize)

    return boot

def wrap_initialize(make_process):
    def initialize(boot_config):
        boot_config.update({
            'emitter': {
                'type': 'database',
                'url': 'localhost:27017',
                'database': 'simulations',
                },
            'compartment_options':{
                'time_step': 1.0,
                },
            })
        process = make_process(boot_config)  # 'boot_config', set in environment.control is the process' initial_parameters
        return generate_lattice_compartment(process, boot_config)

    return initialize


DEFAULT_COLOR = [0.6, 0.4, 0.3]

class EnvironmentAgent(Outer):
    def build_state(self):
        lattice = {
            molecule: self.environment.lattice[index].tolist()
            for index, molecule in enumerate(self.environment.get_molecule_ids())}

        simulations = {
            agent_id: {
                'volume': simulation['state']['volume'],
                'width': self.environment.simulations[agent_id]['state'].get('width', self.environment.cell_radius*2), # TODO (Eran) initialize length, width in cellSimulation
                'length': self.environment.simulations[agent_id]['state'].get('length', self.environment.cell_radius*4),
                'color': simulation['state'].get('color', DEFAULT_COLOR),
                'location': self.environment.locations[agent_id][0:2].tolist(),
                'corner_location': self.environment.corner_locations[agent_id][0:2].tolist(),
                'orientation': self.environment.locations[agent_id][2],
                'parent_id': simulation.get('parent_id', '')}
            for agent_id, simulation in self.environment.simulations.iteritems()}

        return {
            'outer_id': self.agent_id,
            'agent_type': 'ecoli',
            'running': not self.paused,
            'time': self.environment.time(),
            'edge_length': self.environment.edge_length,
            'cell_radius': self.environment.cell_radius,   # TODO (Eran) -- remove this from environment config, should be an attribute of cellSimulations
            'lattice': lattice,
            'simulations': simulations}

    def update_state(self):
        self.send(
            self.topics['visualization_receive'],
            self.build_state(),
            print_send=False)

def boot_lattice(agent_id, agent_type, agent_config):
    working_dir = agent_config.get('working_dir', os.getcwd())

    # set up media
    media_id = agent_config.get('media_id', 'minimal')
    media = agent_config.get('media', {})
    print("Media condition: {}".format(media_id))
    make_media = Media()
    if not media:
        media = make_media.get_saved_media(media_id)

    output_dir = os.path.join(working_dir, 'out', agent_id)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    boot_config = {
        'media_object': make_media,
        'output_dir': output_dir,
        'concentrations': media,
    }
    boot_config.update(agent_config)

    # emitter  TODO (Eran) -- don't repeat this code in the boots
    emitter_config = {
        'type': 'database',
        'url': 'localhost:27017',
        'database': 'simulations',
        'experiment_id': agent_id}
    emitter = get_emitter(emitter_config)
    boot_config.update({'emitter': emitter})

    # create the environment
    environment = EnvironmentSpatialLattice(boot_config)

    return EnvironmentAgent(agent_id, agent_type, agent_config, environment)

def boot_glc_g6p_small(agent_id, agent_type, agent_config):
    working_dir = agent_config.get('working_dir', os.getcwd())

    media_id = 'GLC_G6P'
    make_media = Media()
    timeline_str = '0 {}, 7200 end'.format(media_id)  # (2hr*60*60 = 7200 s), (7hr*60*60 = 25200 s)
    timeline = make_media.make_timeline(timeline_str)

    print("Media condition: {}".format(media_id))
    output_dir = os.path.join(working_dir, 'out', agent_id)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    boot_config = {
        'timeline': timeline,
        'media_object': make_media,
        'output_dir': output_dir,
        # 'concentrations': media,
        'run_for': 2.0,
        'depth': 1e-05, #0.0001,  # 3000 um is default
        'edge_length': 1.0,
        'patches_per_edge': 1,
    }

    boot_config.update(agent_config)

    # emitter
    emitter_config = {
        'type': 'database',
        'url': 'localhost:27017',
        'database': 'simulations',
        'experiment_id': agent_id}
    emitter = get_emitter(emitter_config)
    boot_config.update({'emitter': emitter})

    # create the environment
    environment = EnvironmentSpatialLattice(boot_config)

    return EnvironmentAgent(agent_id, agent_type, agent_config, environment)

def boot_glc_g6p(agent_id, agent_type, agent_config):
    working_dir = agent_config.get('working_dir', os.getcwd())

    media_id = 'GLC_G6P'
    make_media = Media()
    media = make_media.get_saved_media(media_id)

    print("Media condition: {}".format(media_id))
    output_dir = os.path.join(working_dir, 'out', agent_id)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    boot_config = {
        'media_object': make_media,
        'output_dir': output_dir,
        'concentrations': media,
    }

    boot_config.update(agent_config)

    # emitter
    emitter_config = {
        'type': 'database',
        'url': 'localhost:27017',
        'database': 'simulations',
        'experiment_id': agent_id}
    emitter = get_emitter(emitter_config)
    boot_config.update({'emitter': emitter})

    # create the environment
    environment = EnvironmentSpatialLattice(boot_config)

    return EnvironmentAgent(agent_id, agent_type, agent_config, environment)

def boot_glc_lct(agent_id, agent_type, agent_config):
    working_dir = agent_config.get('working_dir', os.getcwd())

    media_id = 'GLC_LCT'
    make_media = Media()
    media = make_media.get_saved_media(media_id)

    print("Media condition: {}".format(media_id))
    output_dir = os.path.join(working_dir, 'out', agent_id)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    boot_config = {
        'media_object': make_media,
        'output_dir': output_dir,
        'concentrations': media,
    }
    boot_config.update(agent_config)

    # emitter
    emitter_config = {
        'type': 'database',
        'url': 'localhost:27017',
        'database': 'simulations',
        'experiment_id': agent_id}
    emitter = get_emitter(emitter_config)
    boot_config.update({'emitter': emitter})

    # create the environment
    environment = EnvironmentSpatialLattice(boot_config)

    return EnvironmentAgent(agent_id, agent_type, agent_config, environment)

def boot_measp(agent_id, agent_type, agent_config):
    # MeAsp is methylaspartate, a nonmetabolizable analog of aspartate and attractant for E. coli

    working_dir = agent_config.get('working_dir', os.getcwd())

    media_id = 'MeAsp timeline'
    timeline_str = '0 GLC 20.0 mmol 1 L + MeAsp 0.0 mmol 1 L, ' \
                   '100 GLC 20.0 mmol 1 L + MeAsp 0.01 mmol 1 L, ' \
                   '300 GLC 20.0 mmol 1 L + MeAsp 0.0 mmol 1 L, ' \
                   '500 GLC 20.0 mmol 1 L + MeAsp 0.1 mmol 1 L, ' \
                   '700 GLC 20.0 mmol 1 L + MeAsp 0.0 mmol 1 L'

    make_media = Media()
    timeline = make_media.make_timeline(timeline_str)

    print("Media condition: {}".format(media_id))
    output_dir = os.path.join(working_dir, 'out', agent_id)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    boot_config = {
        'output_dir': output_dir,
        'media_object': make_media,
        'timeline': timeline,
        # 'concentrations': media,
        'static_concentrations': True,
        'gradient': {
            'seed': True,
            'molecules': {
                'GLC': {
                    'center': [0.5, 1.0],
                    'deviation': 50.0},
                'MeAsp': {
                    'center': [0.25, 0.25],
                    'deviation': 30.0}
            }},
        'diffusion': 0.0,
        'translation_jitter': 0.5,
        'rotation_jitter': 0.005,
        'edge_length': 100.0,
        'patches_per_edge': 50,
    }
    boot_config.update(agent_config)
    environment = EnvironmentSpatialLattice(boot_config)

    return EnvironmentAgent(agent_id, agent_type, agent_config, environment)


class BootEnvironment(BootAgent):
    def __init__(self):
        super(BootEnvironment, self).__init__()
        self.agent_types = {
            'lattice': boot_lattice,
            'sugar1': boot_glc_g6p,
            'sugar1_small': boot_glc_g6p_small,
            'sugar2': boot_glc_lct,
            'measp': boot_measp,

            # single process compartments
            'lookup': wrap_boot(wrap_initialize(TransportLookup), {'volume': 1.0}),
            'metabolism': wrap_boot(wrap_initialize(Metabolism), {'volume': 1.0}),
            'transport': wrap_boot(wrap_initialize(Transport), {'volume': 1.0}),
            'growth': wrap_boot(wrap_initialize(Growth), {'volume': 1.0}),
            'receptor': wrap_boot(wrap_initialize(ReceptorCluster), {'volume': 1.0}),
            # composite compartments
            'growth_division': wrap_boot(initialize_growth_division, {'volume': 1.0}),
            'covert2008': wrap_boot(initialize_covert2008, {'volume': 1.0})
            }

def run():
    boot = BootEnvironment()
    boot.execute()

if __name__ == '__main__':
    run()
