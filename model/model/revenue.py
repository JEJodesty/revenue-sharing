import scipy.stats as stats
# import numpy as np


def revenue_amt(params, step, prev_state, state):
    revenue_amt = state["expected_revenue"] * stats.expon.rvs()

    # revenue_amt = state["expected_revenue"] * (1 + np.sin(timestep * np.pi / 2))
    # print(f'{revenue_amt=}')
    return {'revenue_amt': revenue_amt}


def expected_revenue_change(params, step, prev_state, state):
    expected_revenue_change = state['expected_revenue']
    if state['timestep'] == 250:
        expected_revenue_change *= 10
    return {'expected_revenue_change': expected_revenue_change}


def expected_revenue(params, step, sL, s, inputs):
    key = 'expected_revenue'
    value = inputs['expected_revenue_change']
    return key, value


def update_delegators_expected_revenue(params, step, sL, s, inputs):
    key = 'delegators'
    for d in s['delegators'].values():
        d.expected_revenue = inputs['expected_revenue_change']
    value = s['delegators']
    return key, value


def store_revenue(params, step, sL, s, inputs):
    # print('storing revenue')
    key = 'period_revenue'
    value = inputs['revenue_amt']

    return key, value


def distribute_revenue(params, step, sL, s, inputs):
    revenue = s['period_revenue']
    owners_share = params['owners_share']
    supply = s['supply']

    # step 1: collect revenue from the state
    non_owners_share = ((1-owners_share) * revenue)
    revenue_per_share = non_owners_share / supply

    for id, delegator in s['delegators'].items():
        if id == 0:
            # step 2: get owners share, theta
            delegator.revenue_token_holdings += owners_share * revenue
        
        #  step 3: distribute non-owners share
        # print(f'{delegator.shares=}')
        delegator.revenue_token_holdings += delegator.shares * revenue_per_share
    
    key = 'delegators'
    value = s['delegators']
    return key, value


