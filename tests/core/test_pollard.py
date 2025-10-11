from core.pollard import pollard_rho, pollard_trace


def test_pollard_rho_detects_cycle():
    result = pollard_rho(bits=10, start=1, max_steps=5000)
    assert result.collision_value >= 0
    assert result.iterations > 0
    assert result.tail_length >= 0
    assert result.cycle_length > 0
    assert len(result.tortoise_path) == len(result.hare_path)


def test_pollard_trace_mapping_not_empty():
    mapping = pollard_trace(bits=10, start=2, steps=50)
    assert mapping
    for state, nxt in mapping.items():
        assert isinstance(state, int)
        assert isinstance(nxt, int)
