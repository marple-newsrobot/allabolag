from allabolag import iter_liquidated_companies, iter_list


def test_liquidations():
    for c in iter_liquidated_companies("1900-01-01"):
        assert isinstance(c, dict)
        assert "orgnr" in c
        break

    future_list = [c for c in iter_liquidated_companies("2999-01-01")]
    assert len(future_list) == 0


def test_custom_starting_points():
    for c1 in iter_list("verksamhet/arkitektverksamhet/71110"):
        break
    for c2 in iter_list("verksamhet/arkitektverksamhet/71110", start_from=10):
        break
    assert c1["orgnr"] != c2["orgnr"]
