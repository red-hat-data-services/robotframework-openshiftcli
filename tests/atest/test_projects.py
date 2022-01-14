from openshiftcli import ProjectKeywords


def test_get_projects():
    oc = ProjectKeywords()
    actual = oc.get_projects()
    expected = ['redhat-ods-applications', 'redhat-ods-monitoring', 'redhat-ods-operator']

    assert all(item in actual for item in expected)


def test_project_should_contain():
    oc = ProjectKeywords()
    actual = oc.projects_should_contain("redhat-ods-applications")
    expected = {'redhat-ods-applications': 'Active'}

    assert actual == expected
