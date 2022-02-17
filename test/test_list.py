from allabolag import iter_liquidated_companies


def test_liquidations():
    for c in iter_liquidated_companies("1900-01-01"):
        assert isinstance(c, dict)
        assert "orgnr" in c
        break

    future_list = [c for c in iter_liquidated_companies("2999-01-01")]
    assert len(future_list) == 0
