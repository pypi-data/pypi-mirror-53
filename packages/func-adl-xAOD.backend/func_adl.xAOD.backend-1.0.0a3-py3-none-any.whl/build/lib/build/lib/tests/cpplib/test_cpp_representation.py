# Test the cpp representations. These objects are quite simple, so there
# aren't that many tests. Mostly when bugs are found something gets added here.

import func_adl.xAOD.backend.cpplib.cpp_representation as crep
import func_adl.xAOD.backend.cpplib.cpp_types as ctyp
from func_adl.xAOD.backend.xAODlib.util_scope import top_level_scope

def test_expression_pointer_decl():
    e2 = crep.cpp_value("dude", top_level_scope(), ctyp.terminal("int"))
    assert False == e2.is_pointer()

    e3 = crep.cpp_value("dude", top_level_scope(), ctyp.terminal("int", is_pointer=True))
    assert True == e3.is_pointer()
