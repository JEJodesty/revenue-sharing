from cadCAD import configuration

from .psub import psubs
from .state import genesis_state

# Parameters
# Values are lists because they support sweeping.

def square_wave_gain(period, magnitude, sim_length):
    """ returns list of length sim_length
    only works for magnitudes > 1
    """
    from scipy import signal
    import numpy as np
    timesteps = range(sim_length + 1)
    return [(magnitude - 1) / 2 * signal.square(2 * np.pi * (1 / period) * t) + magnitude - 2 for t in timesteps]


def get_gain(period, magnitude, sim_length):
    timesteps = range(sim_length + 1)
    return [1 for t in timesteps]


sim_length = 2000

params = {
    'initial_reserve': [10],
    'initial_supply': [10],
    'owners_share': [0.25],         # 1-theta  (theta is what all of the other delegators get)
    'arrival_rate': [0.5],
    'expected_reserve_token_holdings': [10000],
    'delegator_estimation_noise_mean': [0],
    'delegator_estimation_noise_variance': [1],  # proportional to expected_revenue
    'reserve_to_revenue_token_exchange_rate': [1],
    'delegator_activity_rate': [0.5],
    'mininum_required_price_pct_diff_to_act': [0.02],
    'risk_adjustment': [0.7],  # cut 30% of the value off due to risk
    'half_life_vesting_rate': [0.5],  # this is the fraction of shares that vest each timestep if using half life vesting
    'cliff_vesting_timesteps': [14],  # this is the number of timesteps until shares are fully vested
    'num_days_for_trends': [14],  # this is the number of days to consider for private price calculation's regression to mean price
    'halflife': [0.5],  # halflife for trend analysis
    'mean_discount_rate': [0.7],  # this is the mean of the delegators' discount rates
    # low value of smoothing_factor takes longer to catch up.
    'mean_smoothing_factor': [0.9],  # low value takes into account previous spot_price more, high value takes into account current price more
    'max_delegator_count': [4],
    # 'shock_factor': [10, 0.1],
    # 'shock_timestep': [500]
    'gain': [get_gain(200, magnitude, sim_length) for magnitude in [1, 10]]
}

simulation_config = configuration.utils.config_sim({
    # 'T': range(sim_length),
    'T': range(10),
    'N': 1,
    'M': params
})

exp = configuration.Experiment()

exp.append_configs(
    model_id='sys_model_A',
    sim_configs=simulation_config,
    initial_state=genesis_state,
    partial_state_update_blocks=psubs
)
