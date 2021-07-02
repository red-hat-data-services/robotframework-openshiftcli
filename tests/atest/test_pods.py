from OpenShiftCLI import OpenShiftCLI


def test_get_pods():
    oc = OpenShiftCLI()
    actual = oc.get_pods()
    expected = None
    assert actual == expected
