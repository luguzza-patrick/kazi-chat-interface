from app.rbac.graph import rbac_engine

def test_employee_can_access_own_data():
    assert rbac_engine.can_access(1, "employee", 1) is True

def test_employee_cannot_access_other_data():
    assert rbac_engine.can_access(1, "employee", 2) is False

def test_hr_can_access_employee_data():
    assert rbac_engine.can_access(4, "hr", 1) is True
    assert rbac_engine.can_access(4, "hr", 2) is True

def test_ceo_can_access_all_data():
    assert rbac_engine.can_access(5, "ceo", 1) is True
    assert rbac_engine.can_access(5, "ceo", 4) is True
