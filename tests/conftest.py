import pytest

@pytest.fixture
def example_beam_data():
    import numpy as np
    return np.random.randn(10000, 6)

