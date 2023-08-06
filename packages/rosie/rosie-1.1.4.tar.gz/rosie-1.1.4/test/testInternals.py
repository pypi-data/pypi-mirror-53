# coding: utf-8
#  -*- Mode: Python; -*-                                              
# 
# python testInternals.py [local | system]
# AUTHOR  Jamie A. Jennings
#
from __future__ import unicode_literals, print_function

import unittest
import sys, os, json
import internal

# Notes
#
# (1) We use the librosie.so that is in the directory above this one,
#     i.e. "..", so we supply the librosiedir argument to
#     internal.engine().  Normally, no argument to internal.engine() is
#     needed.

if sys.version_info.major < 3:
    str23 = lambda s: str(s)
    bytes23 = lambda s: bytes(s)
else:
    str23 = lambda s: str(s, encoding='UTF-8')
    bytes23 = lambda s: bytes(s, encoding='UTF-8')


class internalInitTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        internal.load(librosiedir, quiet=True)
        engine = internal.engine()
        assert(engine)
        path = internal.librosie_path()
        assert(path)

class internalLoadTest(unittest.TestCase):

    engine = None
    
    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        ok, pkgname, errs = self.engine.load(b'package x; foo = "foo"')

        self.assertTrue(ok)
        self.assertTrue(pkgname == b"x")
        self.assertTrue(errs == None)

        b, errs = self.engine.compile(b"x.foo")
        self.assertTrue(b.valid())
        self.assertTrue(errs == None)

        bb, errs = self.engine.compile(b"[:digit:]+")
        self.assertTrue(bb.valid())
        self.assertTrue(errs == None)
        self.assertTrue(b.id[0] != bb.id[0])

        b2, errs = self.engine.compile(b"[:foobar:]+")
        self.assertTrue(not b2)
        errlist = json.loads(errs)
        self.assertTrue(len(errlist) > 0)
        err = errlist[0]
        self.assertTrue(err['message'])
        self.assertTrue(err['who'] == 'compiler')

        b = None                       # trigger call to librosie to gc the compiled pattern
        b, errs = self.engine.compile(b"[:digit:]+")
        self.assertTrue(b.id[0] != bb.id[0]) # distinct values for distinct patterns
        self.assertTrue(errs == None)

        num_int, errs = self.engine.compile(b"num.int")
        self.assertTrue(not num_int)
        errlist = json.loads(errs)
        err = errlist[0]
        self.assertTrue(err['message'])
        self.assertTrue(err['who'] == 'compiler')

        ok, pkgname, errs = self.engine.load(b'foo = "')
        self.assertTrue(not ok)
        errlist = json.loads(errs)
        err = errlist[0]
        self.assertTrue(err['message'])
        self.assertTrue(err['who'] == 'parser')

        engine2 = internal.engine()
        self.assertTrue(engine2)
        self.assertTrue(engine2 != self.engine)
        engine2 = None          # triggers call to librosie to gc the engine

class internalConfigTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        a = self.engine.config()
        self.assertTrue(a)
        cfg = json.loads(a)
        array = cfg[0]
        for entry in array:
            self.assertTrue(type(entry) is dict)
            self.assertTrue(entry['name'])
            self.assertTrue(entry['description'])
            if not entry['value']:
                self.assertTrue(entry['name'] == 'ROSIE_COMMAND')
        array = cfg[1]
        rpl_version = None
        libpath = None
        for entry in array:
            if entry['name']=='RPL_VERSION':
                rpl_version = entry['value']
            if entry['name']=='ROSIE_LIBPATH':
                libpath = entry['value']
        if sys.version_info.major < 3:
            self.assertTrue(type(rpl_version) is unicode)
            self.assertTrue(type(libpath) is unicode)
        else:
            self.assertTrue(type(rpl_version) is str)
            self.assertTrue(type(libpath) is str)
            
            
class internalLibpathTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        path = self.engine.libpath()
        self.assertIsInstance(path, bytes)
        newpath = b"foo bar baz"
        self.engine.libpath(newpath)
        testpath = self.engine.libpath()
        self.assertIsInstance(testpath, bytes)
        self.assertTrue(testpath == newpath)
                
class internalAlloclimitTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        limit, usage = self.engine.alloc_limit()
        self.assertIsInstance(limit, int)
        self.assertTrue(limit == 0)
        limit, usage = self.engine.alloc_limit(0)
        limit, usage = self.engine.alloc_limit()
        self.assertTrue(limit == 0)
        limit, usage = self.engine.alloc_limit(8199)
        self.assertTrue(limit == 8199)
        with self.assertRaises(ValueError):
            limit, usage = self.engine.alloc_limit(8191) # too low
        limit, usage = self.engine.alloc_limit()
        self.assertTrue(limit == 8199)

class internalImportTest(unittest.TestCase):

    engine = None
    
    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()
        self.assertTrue(self.engine)

    def tearDown(self):
        pass

    def test(self):
        ok, pkgname, errs = self.engine.import_pkg(b'net')
        self.assertTrue(ok)
        self.assertTrue(pkgname == b'net')
        self.assertTrue(errs == None)

        ok, pkgname, errs = self.engine.import_pkg(b'net', b'foobar')
        self.assertTrue(ok)
        self.assertTrue(pkgname == b'net') # actual name inside the package
        self.assertTrue(errs == None)

        net_any, errs = self.engine.compile(b"net.any")
        self.assertTrue(net_any)
        self.assertTrue(errs == None)

        foobar_any, errs = self.engine.compile(b"foobar.any")
        self.assertTrue(foobar_any)
        self.assertTrue(errs == None)
        
        m, left, abend, tt, tm = self.engine.match(net_any, b"1.2.3.4", 1, b"color")
        self.assertTrue(m)

        m, left, abend, tt, tm = self.engine.match(net_any, b"1.2.3.4", 1, b"json")
        self.assertTrue(isinstance(str(m), str))
        m = json.loads(m)
        self.assertTrue(m['data'])
        self.assertTrue(m)
        self.assertTrue(m['subs'])

        m, left, abend, tt, tm = self.engine.match(net_any, b"Hello, world!", 1, b"color")
        self.assertTrue(not m)

        ok, pkgname, errs = self.engine.import_pkg(b'THISPACKAGEDOESNOTEXIST')
        self.assertTrue(not ok)
        self.assertTrue(errs != None)


class internalLoadfileTest(unittest.TestCase):

    engine = None
    
    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()
        self.assertTrue(self.engine)

    def tearDown(self):
        pass

    def test(self):
        ok, pkgname, errs = self.engine.loadfile(b'test.rpl')
        self.assertTrue(ok)
        self.assertTrue(pkgname == bytes(b'test'))
        self.assertTrue(errs == None)


class internalMatchTest(unittest.TestCase):

    engine = None
    
    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):

        b, errs = self.engine.compile(b"[:digit:]+")
        self.assertTrue(b.valid())
        self.assertTrue(errs == None)

        m, left, abend, tt, tm = self.engine.match(b, b"321", 2, b"json")
        self.assertTrue(m)
        m = json.loads(bytes(m))
        self.assertTrue(m['type'] == "*")
        self.assertTrue(m['s'] == 2)     # match started at char 2
        self.assertTrue(m['e'] == 4)
        self.assertTrue(m['data'] == "21")
        self.assertTrue(left == 0)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        m, left, abend, tt, tm = self.engine.match(b, b"xyz", 1, b"json")
        self.assertTrue(m == False)
        self.assertTrue(left == 3)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        inp = b"889900112233445566778899100101102103104105106107108109110xyz"
        linp = len(inp)

        m, left, abend, tt, tm = self.engine.match(b, inp, 1, b"json")
        self.assertTrue(m)
        m = json.loads(m)
        self.assertTrue(m['type'] == "*")
        self.assertTrue(m['s'] == 1)
        self.assertTrue(m['e'] == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m['data'] == str23(inp[0:-3]))
        self.assertTrue(left == 3)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        m, left, abend, tt, tm = self.engine.match(b, inp, 10, b"json")
        self.assertTrue(m)
        m = json.loads(m)
        self.assertTrue(m['type'] == "*")
        self.assertTrue(m['s'] == 10)
        self.assertTrue(m['e'] == linp-3+1) # due to the "xyz" at the end
        self.assertTrue(m['data'] == str23(inp[9:-3]))
        self.assertTrue(left == 3)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        m, left, abend, tt, tm = self.engine.match(b, inp, 1, b"line")
        self.assertTrue(m)
        self.assertTrue(m == inp)
        self.assertTrue(left == 3)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        m, left, abend, tt, tm = self.engine.match(b, inp, 1, b"bool")
        self.assertIs(m, True)
        self.assertTrue(left == 3)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        m, left, abend, tt, tm = self.engine.match(b, inp, 1, b"color")
        self.assertTrue(m)
        # only checking the first two chars, looking for the start of
        # ANSI color sequence
        self.assertTrue(str23(m)[0] == '\x1B')
        self.assertTrue(str23(m)[1] == '[')
        self.assertTrue(left == 3)
        self.assertTrue(abend == False)
        self.assertTrue(tt >= 0)
        self.assertTrue(tm >= 0)

        self.assertRaises(ValueError, self.engine.match, b, inp, 1, b"this_is_not_a_valid_encoder_name")

            
class internalTraceTest(unittest.TestCase):

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()
        self.assertTrue(self.engine)
        ok, pkgname, errs = self.engine.import_pkg(b'net')
        self.assertTrue(ok)
        self.net_any, errs = self.engine.compile(b'net.any')
        self.assertTrue(self.net_any)

    def tearDown(self):
        pass

    def test(self):
        matched, trace = self.engine.trace(self.net_any, b"1.2.3.4", 1, b"condensed")
        self.assertTrue(matched == True)
        self.assertTrue(trace)
        self.assertTrue(len(trace) > 0)

        net_ip, errs = self.engine.compile(b"net.ip")
        self.assertTrue(net_ip)
        matched, trace = self.engine.trace(net_ip, b"1.2.3", 1, b"condensed")
        self.assertTrue(matched == False)
        self.assertTrue(trace)
        self.assertTrue(len(trace) > 0)

        matched, trace = self.engine.trace(self.net_any, b"1.2.3.4", 1, b"full")
        self.assertTrue(matched == True)
        self.assertTrue(trace)
        self.assertTrue(len(trace) > 0)
        self.assertTrue(trace.find(b'Matched 6 chars') != -1)

        try:
            matched, trace = self.engine.trace(self.net_any, b"1.2.3", 1, b"no_such_trace_style")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(repr(e).find('invalid trace style') != -1)

        matched, trace = self.engine.trace(self.net_any, b"1.2.3.4", 1, b"json")
        self.assertTrue(matched == True)
        self.assertTrue(trace)
        self.assertTrue(len(trace) > 0)
        tr = json.loads(trace)
        self.assertTrue('match' in tr)
        self.assertTrue(tr['match'])
        self.assertTrue('nextpos' in tr)
        self.assertTrue(tr['nextpos'] == 8)
        

class internalMatchFileTest(unittest.TestCase):

    engine = None
    net_any = None
    findall_net_any = None
    
    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()
        self.assertTrue(self.engine)
        ok, pkgname, errs = self.engine.import_pkg(b'net')
        self.assertTrue(ok)
        self.net_any, errs = self.engine.compile(b"net.any")
        self.assertTrue(self.net_any)
        self.findall_net_any, errs = self.engine.compile(b"findall:net.any")
        self.assertTrue(self.findall_net_any)

    def tearDown(self):
        pass

    def test(self):
        if testdir:
            cin, cout, cerr = self.engine.matchfile(self.findall_net_any,
                                                    b"json",
                                                    bytes23(os.path.join(testdir, "resolv.conf")),
                                                    b"/tmp/resolv.out",
                                                    b"/tmp/resolv.err")
            self.assertTrue(cin == 10)
            self.assertTrue(cout == 5)
            self.assertTrue(cerr == 5)

            cin, cout, cerr = self.engine.matchfile(self.net_any,
                                                    b"color",
                                                    infile=bytes23(os.path.join(testdir, "resolv.conf")),
                                                    errfile=b"/dev/null",
                                                    wholefile=True)
            self.assertTrue(cin == 1)
            self.assertTrue(cout == 0)
            self.assertTrue(cerr == 1)

class internalReadRcfileTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        if testdir:
            options, messages = self.engine.read_rcfile(bytes23(os.path.join(testdir, "rcfile1")))
            self.assertIsInstance(options, list)
            self.assertTrue(messages is None)
            options, messages = self.engine.read_rcfile(bytes23(os.path.join(testdir, "rcfile2")))
            self.assertTrue(messages[0].find("Syntax errors in rcfile") != -1)
            self.assertTrue(options is False)
            options, messages = self.engine.read_rcfile(b"This file does not exist")
            self.assertTrue(options is None)
            self.assertTrue(messages[0].find("Could not open rcfile") != -1)

class internalExecuteRcfileTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        result, messages = self.engine.execute_rcfile(b"This file does not exist")
        self.assertTrue(result is None)
        if testdir:
            result, messages = self.engine.execute_rcfile(bytes23(os.path.join(testdir, "rcfile1")))
            self.assertFalse(result)
            self.assertNotEqual(messages[0].find("Failed to load another-file"), -1)
            result, messages = self.engine.execute_rcfile(bytes23(os.path.join(testdir, "rcfile2")))
            self.assertFalse(result)
            self.assertTrue(messages[0].find("Syntax errors in rcfile") != -1)
            result, messages = self.engine.execute_rcfile(bytes23(os.path.join(testdir, "rcfile3")))
            self.assertFalse(result)
            self.assertTrue(messages[0].find("Failed to load nofile_mod1.rpl") != -1)
            result, messages = self.engine.execute_rcfile(bytes23(os.path.join(testdir, "rcfile6")))
            self.assertTrue(result)
            self.assertTrue(messages is None)
        
# -----------------------------------------------------------------------------
class internalParseTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        # Parse expression
        result, messages = self.engine.parse_expression(b"A")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue('ref' in pt)
        self.assertTrue('localname' in pt['ref'])
        self.assertTrue(pt['ref']['localname'] == "A")
        result, messages = self.engine.parse_expression(b"A / B.c")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue('choice' in pt)
        self.assertTrue('exps' in pt['choice'])
        second_exp = pt['choice']['exps'][1]
        self.assertTrue('ref' in second_exp)
        self.assertTrue(second_exp['ref']['packagename'] == "B")
        self.assertTrue(second_exp['ref']['localname'] == "c")
        result, messages = self.engine.parse_expression(b"A // B.c") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)
        # Parse block
        result, messages = self.engine.parse_block(b"x = A / B.c; y=[:alpha:]")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue('block' in pt)
        self.assertTrue('stmts' in pt['block'])
        binding1 = pt['block']['stmts'][0]
        binding2 = pt['block']['stmts'][1]
        def check_binding(b, boundname):
            self.assertTrue('binding' in b)
            self.assertTrue('ref' in b['binding'])
            self.assertTrue('ref' in b['binding']['ref'])
            self.assertTrue('localname' in b['binding']['ref']['ref'])
            self.assertTrue(b['binding']['ref']['ref']['localname'] == boundname)
        check_binding(binding1, 'x')
        check_binding(binding2, 'y')
        result, messages = self.engine.parse_block(b" = A / B.c; y=[:alpha:]") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)

# -----------------------------------------------------------------------------
class internalRefsTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        # Expression
        result, messages = self.engine.expression_refs(b"A")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue(len(pt) == 1)
        self.assertTrue('ref' in pt[0])
        self.assertTrue('localname' in pt[0]['ref'])
        self.assertTrue(pt[0]['ref']['localname'] == "A")
        result, messages = self.engine.expression_refs(b'A / "hello" / B.c [:digit:]+ mac:#hi')
        def check_refs(result, messages):
            self.assertFalse(result is None)
            self.assertTrue(messages is None)
            pt = json.loads(result)
            self.assertTrue(len(pt) == 3)
            self.assertTrue('ref' in pt[0])
            self.assertTrue(pt[0]['ref']['localname'] == "A")
            self.assertTrue('ref' in pt[1])
            self.assertTrue(pt[1]['ref']['packagename'] == "B")
            self.assertTrue(pt[1]['ref']['localname'] == "c")
            self.assertTrue('ref' in pt[2])
            self.assertTrue(pt[2]['ref']['localname'] == "mac")
        check_refs(result, messages)
        result, messages = self.engine.expression_refs(b"A // B.c") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)
        # Block
        result, messages = self.engine.block_refs(b"x = A / B.c; y=[:alpha:] mac:#tagname")
        check_refs(result, messages)
        result, messages = self.engine.block_refs(b" = A / B.c; y=[:alpha:]") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)

# -----------------------------------------------------------------------------
class internalDepsTest(unittest.TestCase):

    engine = None

    def setUp(self):
        internal.load(librosiedir, quiet=True)
        self.engine = internal.engine()

    def tearDown(self):
        pass

    def test(self):
        # Expression
        result, messages = self.engine.expression_deps(b"A")
        self.assertFalse(result is None)
        self.assertTrue(messages is None)
        pt = json.loads(result)
        self.assertTrue(len(pt) == 0)
        result, messages = self.engine.expression_deps(b'A / "hello" / B.c [:digit:]+ p.mac:#hi')
        def check_deps(result, messages, index=None):
            self.assertFalse(result is None)
            self.assertTrue(messages is None)
            pt = json.loads(result)
            if index: pt = pt[index]
            self.assertTrue(len(pt) == 2)
            self.assertTrue(pt[0] == 'B')
            self.assertTrue(pt[1] == 'p')
        check_deps(result, messages)
        result, messages = self.engine.expression_deps(b"A // B.c") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)
        # Block
        result, messages = self.engine.block_deps(b"x = A / B.c; y=[:alpha:] p.mac:#tagname")
        check_deps(result, messages, 'implicit')
        result, messages = self.engine.block_deps(b"import F as G, H; x = A / B.c; y=[:alpha:] p.mac:#tagname")
        check_deps(result, messages, 'implicit')
        pt = json.loads(result)
        pt = pt['explicit']
        self.assertTrue(len(pt) == 2)
        self.assertTrue('as_name' in pt[0])
        self.assertTrue(pt[0]['as_name'] == 'G')
        self.assertTrue('importpath' in pt[0])
        self.assertTrue(pt[0]['importpath'] == 'F')
        self.assertTrue(not 'as_name' in pt[1])
        self.assertTrue('importpath' in pt[1])
        self.assertTrue(pt[1]['importpath'] == 'H')
        result, messages = self.engine.block_deps(b" = A / B.c; y=[:alpha:]") # syntax error
        self.assertTrue(result is None)
        self.assertFalse(messages is None)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Error: missing command-line parameter specifying 'local' or 'system' test")
    if sys.argv[1]=='local':
        librosiedir = '//../binaries'
        print("Loading librosie from ", librosiedir[2:])
        testdir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '../../test')
    elif sys.argv[1]=='system':
        librosiedir = internal.librosie_system
        print("Loading librosie from system library path")
        testdir = None
    else:
        sys.exit("Error: invalid command-line parameter (must be 'local' or 'system')")
    print("Running tests using " + sys.argv[1] + " rosie installation")
    del sys.argv[1:]
    unittest.main()
