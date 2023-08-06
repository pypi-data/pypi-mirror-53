def test_connect():
    """Check that casput and caget work together"""
    PV_name = "TEST:TEST.VAL" 
    from CAServer import casput
    casput(PV_name,1)
    from CA import caget
    assert caget(PV_name) == 1

def test_diconnect():
    """Check that 'casdel' disconnects a PV"""
    PV_name = "TEST:TEST.VAL" 
    from CAServer import casput
    casput(PV_name,1)
    from CA import caget
    assert caget(PV_name) == 1
    from CAServer import casdel
    casdel(PV_name)
    from time import sleep
    sleep(0.1)
    assert caget(PV_name) is None
