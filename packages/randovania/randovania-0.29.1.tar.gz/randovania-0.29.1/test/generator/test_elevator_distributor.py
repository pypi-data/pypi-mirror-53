from random import Random
from typing import List
from unittest.mock import patch, MagicMock

import pytest

from randovania.game_description.area_location import AreaLocation
from randovania.generator import elevator_distributor


@pytest.mark.parametrize(["seed_number", "expected_ids"], [
    (5000, [589949, 2949235, 4260106, 2162826, 393260, 4522032, 152, 3538975, 136970379, 204865660, 589851,
            1245332, 38, 1572998, 1638535, 2097251, 3342446, 1245307, 122, 129, 524321, 1966093]),
    (9000, [1245307, 2949235, 1245332, 152, 589949, 4522032, 129, 2097251, 204865660, 1638535, 136970379,
            4260106, 589851, 1572998, 3538975, 38, 3342446, 2162826, 1966093, 524321, 393260, 122]),
    (1157772449, [4260106, 393260, 1638535, 2162826, 1245307, 2949235, 152, 3538975, 1572998, 129, 1245332,
                  204865660, 136970379, 3342446, 524321, 2097251, 38, 4522032, 589949, 1966093, 122, 589851])
])
def test_try_randomize_elevators(seed_number: int,
                                 expected_ids: List[int],
                                 echoes_game_description):
    # Setup
    rng = Random(seed_number)

    # Run
    result = elevator_distributor.try_randomize_elevators(
        rng,
        elevator_distributor.create_elevator_database(echoes_game_description.world_list, set()))
    connected_ids = [elevator.connected_elevator.instance_id for elevator in result]

    # Assert
    assert connected_ids == expected_ids


@patch("randovania.generator.elevator_distributor.try_randomize_elevators", autospec=True)
def test_elevator_connections_for_seed_number(mock_try_randomize_elevators: MagicMock,
                                              ):
    # Setup
    rng = MagicMock()
    elevator = MagicMock()
    database = MagicMock()
    mock_try_randomize_elevators.return_value = [
        elevator
    ]

    # Run
    result = elevator_distributor.elevator_connections_for_seed_number(rng, database)

    # Assert
    mock_try_randomize_elevators.assert_called_once_with(rng, database)
    assert result == {
        elevator.instance_id: AreaLocation(elevator.connected_elevator.world_asset_id,
                                           elevator.connected_elevator.area_asset_id)
    }
