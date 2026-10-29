from unittest.mock import patch

import promo


@patch("promo.random")
def test_top_prize(mock_random):
    mock_random.choice.return_value = 50
    assert promo.lucky_price(500) == 250
    mock_random.choice.assert_called_once_with(
        [0, 10, 25, 50]
    )
