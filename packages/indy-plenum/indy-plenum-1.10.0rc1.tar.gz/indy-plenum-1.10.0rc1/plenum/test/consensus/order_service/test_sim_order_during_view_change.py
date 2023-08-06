from functools import partial

import pytest

from plenum.common.messages.internal_messages import NeedViewChange
from plenum.common.timer import RepeatingTimer
from plenum.test.consensus.order_service.sim_helper import MAX_BATCH_SIZE, setup_pool, order_requests, \
    check_consistency, check_batch_count
from plenum.test.simulation.sim_random import DefaultSimRandom


REQUEST_COUNT = 10


@pytest.mark.skip(reason="Can be turned on after INDY-1340")
@pytest.mark.parametrize("seed", range(1))
def test_view_change_while_ordering_with_real_msgs(seed):
    # 1. Setup pool
    requests_count = REQUEST_COUNT
    batches_count = requests_count // MAX_BATCH_SIZE
    random = DefaultSimRandom(seed)
    pool = setup_pool(random, requests_count)

    # 2. Send 3pc batches
    random_interval = 1000
    RepeatingTimer(pool.timer, random_interval, partial(order_requests, pool))

    for node in pool.nodes:
        pool.timer.schedule(3000,
                            partial(node._view_changer.process_need_view_change, NeedViewChange(view_no=1)))
    # 3. Make sure that view_change is completed
    for node in pool.nodes:
        pool.timer.wait_for(lambda: node._view_changer._data.view_no == 1, timeout=20000)

    # 3. Make sure all nodes ordered all the requests
    for node in pool.nodes:
        pool.timer.wait_for(partial(check_batch_count, node, batches_count), timeout=20000)

    # 4. Check data consistency
    check_consistency(pool)
