from openshiftcli import PodKeywords


def test_get_pods():
    oc = PodKeywords()
    actual = len(oc.get_pods("redhat-ods-applications"))
    expected = 9

    assert actual == expected


def test_pods_should_contain():
    oc = PodKeywords()
    actual = len(oc.pods_should_contain("jupyterhub-db", "redhat-ods-applications"))
    expected = 3
    print(oc.pods_should_contain("jupyterhub-db", "redhat-ods-applications"))
    assert actual == expected
