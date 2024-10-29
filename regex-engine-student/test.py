from regex import parse_regex, RSingle
from fa import NFA, DFA, SUPPORTED_SYMBOLS, EPSILON

def test_regexpr_str(): 
    assert str(parse_regex("a")) == "RSingle('a')", f"Part 1 Test 1 failed: Expected 'RSingle('a')', got {RSingle('a')}"
    
    assert str(parse_regex("ab")) == "RConcat(RSingle('a'),RSingle('b'))", \
        f"Part 1 Test 2 failed: Expected 'RConcat(RSingle('a'),RSingle('b'))', got {parse_regex('ab')}"
    
    assert str(parse_regex("(a|b)*c")) == \
        "RConcat(RStar(RUnion(RSingle('a'),RSingle('b'))),RSingle('c'))", \
        f"Part 1 Test 3 failed: Expected 'RConcat(RStar(RUnion(RSingle('a'),RSingle('b'))),RSingle('c'))', got {str(parse_regex('(a|b)*c'))}"
    
    print("Part 1 tests passed!")

def test_nfa():
    # this only checks if your from_regex runs without error
    nfa0 = NFA.from_regex(parse_regex("ab(c|d)*"))
    
    nfa1 = NFA.from_regex(parse_regex("a*"))
    assert nfa1.accepts(EPSILON) == True, f"Part 3 Test 1 failed: Expected True, got {nfa1.accepts('')}"
    assert nfa1.accepts("a") == True, f"Part 3 Test 2 failed: Expected True, got {nfa1.accepts('a')}"
    assert nfa1.accepts("aab") == False, f"Part 3 Test 3 failed: Expected False, got {nfa1.accepts('aab')}"

    nfa2 = NFA.from_regex(parse_regex("a(b|c)*"))
    assert nfa2.accepts("acc") == True, f"Part 3 Test 4 failed: Expected True, got {nfa2.accepts('ac')}"
    assert nfa2.accepts("ad") == False, f"Part 3 Test 5 failed: Expected False, got {nfa2.accepts('ad')}"
    assert nfa2.accepts("a") == True, f"Part 3 Test 6 failed: Expected True, got {nfa2.accepts('a')}"

    print("Part 2 tests passed!")


def test_dfa():
    nfa1 = NFA.from_regex(parse_regex("a*"))
    dfa1 = DFA.from_nfa(nfa1)

    assert dfa1.accepts(EPSILON) == True, f"Part 3 Test 1 failed: Expected True, got {dfa1.accepts('')}"
    assert dfa1.accepts("a") == True, f"Part 3 Test 2 failed: Expected True, got {dfa1.accepts('a')}"
    assert dfa1.accepts("aab") == False, f"Part 3 Test 3 failed: Expected False, got {dfa1.accepts('aab')}"

    nfa2 = NFA.from_regex(parse_regex("a(b|c)*"))
    dfa2 = DFA.from_nfa(nfa2)

    assert dfa2.accepts("acc") == True, f"Part 3 Test 4 failed: Expected True, got {dfa2.accepts('ac')}"
    assert dfa2.accepts("ad") == False, f"Part 3 Test 5 failed: Expected False, got {dfa2.accepts('ad')}"
    assert dfa2.accepts("a") == True, f"Part 3 Test 6 failed: Expected True, got {dfa2.accepts('a')}"
    
    print("Part 3 tests passed!")