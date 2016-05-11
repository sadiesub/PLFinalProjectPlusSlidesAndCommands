# -*- coding: utf-8 -*-
from swift_yacc import yacc, lisp_str
import cmd

class MiniSwift(cmd.Cmd):     # See https://docs.python.org/2/library/cmd.html
    """
    MiniLisp evalúa expresiones sencillas con sabor a lisp, 
    más información en http://www.juanjoconti.com.ar
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "ms> "
        self.intro  = "Bienvenue au MiniSwift"

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    def do_EOF(self, args):
        """Exit on system end of file character"""
        print "Good bye!"
        return self.do_exit(args)

    def do_help(self, args):
        print self.__doc__

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        result = yacc.parse(line)
        print "AST is: ", result
        import lis_swift
        r =  lis_swift.eval(result)
        if r is not None: print r
        '''
        s = lisp_str(result)
        if s != 'nil':
            print s
        '''

if __name__ == '__main__':
        ml = MiniSwift()
        ml.cmdloop()     # See https://docs.python.org/2/library/cmd.html
