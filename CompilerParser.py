from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.current_index = 0


    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        tree = ParseTree('class', '')

        tree.addChild(self.mustBe('keyword', 'class'))

        tree.addChild(self.mustBe('identifier'))

        tree.addChild(self.mustBe('symbol', '{'))

        tree.addChild(self.mustBe('symbol', '}'))
        
        return tree 
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        tree = ParseTree('class', '')

        tree.addChild(self.mustBe('keyword', 'class'))

        tree.addChild(self.mustBe('identifier'))

        tree.addChild(self.mustBe('symbol', '{'))

        while self.have('keyword', 'static') or self.have('keyword', 'field'):
            tree.addChild(self.compileClassVarDec())

        while self.have('keyword', 'constructor') or self.have('keyword', 'function') or self.have('keyword', 'method'):
            tree.addChild(self.compileSubroutine())
                
        tree.addChild(self.mustBe('symbol', '}'))

        return tree


    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        tree = ParseTree('classVarDec', '')

        if self.have('keyword', 'static'):
            tree.addChild(self.mustBe('keyword', 'static'))
        elif self.have('keyword', 'field'):
            tree.addChild(self.mustBe('keyword', 'field'))
        else:
            raise ParseException('Must be keyword: static or field')
        
        if self.have('keyword', 'int'):
            tree.addChild(self.mustBe('keyword', 'int'))
        elif self.have('keyword', 'char'):
            tree.addChild(self.mustBe('keyword', 'char'))
        elif self.have('keyword', 'boolean'):
            tree.addChild(self.mustBe('keyword', 'boolean'))
        elif self.have("identifier"):
            tree.addChild(self.mustBe('identifier'))
        else:
            raise ParseException('Must be keyword: type')

        tree.addChild(self.mustBe('identifier'))

        while self.have('symbol', ','):
            tree.addChild(self.mustBe('symbol', ','))
            tree.addChild(self.mustBe('identifier'))

        tree.addChild(self.mustBe('symbol', ';'))

        return tree
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        tree = ParseTree('subroutine','')

        if self.have('keyword', 'constructor'):
            tree.addChild(self.mustBe('keyword', 'constructor'))
        elif self.have('keyword', 'function'):
            tree.addChild(self.mustBe('keyword', 'function'))
        elif self.have('keyword', 'method'):
            tree.addChild(self.mustBe('keyword', 'method'))
        else:
            raise ParseException('Must be keyword constructor,function or method')
        
        type_keywords = ['int', 'char', 'boolean', 'void']
        if self.have('keyword') and self.current().getValue() in type_keywords:
            tree.addChild(self.mustBe('keyword', self.current().getValue()))
        elif self.have('identifier'):  #identifier, className
            tree.addChild(self.mustBe('identifier')) 
        else:
            raise ParseException('Must be keyword type of identifier')

        tree.addChild(self.mustBe('identifier'))  #identifier, subroutineName

        tree.addChild(self.mustBe('symbol', '('))
        tree.addChild(self.compileParameterList())
        tree.addChild(self.mustBe('symbol', ')'))

        tree.addChild(self.compileSubroutineBody())

        return tree
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        grammar: ((type varName)(',' type varName)*)?
        """
        tree = ParseTree('parameterList', '')

        # Check for an empty parameter list (no parameters)
        if self.have('symbol', ')'):
            return tree

        type_keywords = ['int', 'char', 'boolean']

        while True:
            # Parse the type
            if self.have('keyword') and self.current().getValue() in type_keywords:
                tree.addChild(self.mustBe('keyword', self.current().getValue()))
            elif self.have('identifier'):
                tree.addChild(self.mustBe('identifier'))  # Add an identifier
            else:
                raise ParseException('Please specify a valid type')

            # Parse the varName
            tree.addChild(self.mustBe('identifier'))

            if self.have('symbol', ','):
                # If there's a comma, parse additional parameters
                tree.addChild(self.mustBe('symbol', ','))
            else:
                break

        return tree

    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        grammar: '{' varDec* statements '}'
        """
        tree = ParseTree('subroutineBody','')

        tree.addChild(self.mustBe('symbol','{'))

        while self.have('keyword', 'var'):
            tree.addChild(self.compileVarDec())

        tree.addChild(self.compileStatements())
    
        tree.addChild(self.mustBe('symbol','}'))

        return tree

    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        grammar: 'var' type varName (',' VarName)* ';'
        """
        tree = ParseTree('varDec','')

        #'var'
        tree.addChild(self.mustBe('keyword', 'var'))

        #type
        type_keywords = ['int','char','boolean']

        if self.have('keyword') and self.current().getValue() in type_keywords:
            tree.addChild(self.mustBe('keyword', self.current().getValue()))
        elif self.have('identifier'):
            tree.addChild(self.mustBe('identifier'))
        else:
            raise Exception('Please specify a valid type')
        
        #varName
        tree.addChild(self.mustBe('identifier'))

        #(',' varName)*
        while self.have('symbol',','):
            tree.addChild(self.mustBe('symbol',','))
            tree.addChild(self.mustBe('identifier'))

        #';'
        tree.addChild(self.mustBe('symbol',';'))

        return tree

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        grammar: (letStatement|ifStatement|whileStatement|doStatement|returnStatement)*
        """
        tree = ParseTree('statements','')

        statements_list = ['let', 'if', 'while', 'do', 'return']
        while self.have('keyword') and self.current().value in statements_list:
            if self.have('keyword','let'):
                tree.addChild(self.compileLet())
            elif self.have ('keyword', 'if'):
                tree.addChild(self.compileIf())
            elif self.have ('keyword', 'while'):
                tree.addChild(self.compileWhile())
            elif self.have ('keyword', 'do'):
                tree.addChild(self.compileDo())
            elif self.have ('keyword', 'return'):
                tree.addChild(self.compileReturn())
        return tree
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        grammar: 'let' varName ('[' expression ']')? '=' expression ';'
        """
        tree = ParseTree('letStatement','')

        tree.addChild(self.mustBe('keyword', 'let'))
        tree.addChild(self.mustBe('identifier'))
        
        if self.have('symbol', '['):
            tree.addChild(self.mustBe('symbol', '['))
            tree.addChild(self.compileExpression())
            tree.addChild(self.mustBe('symbol', ']'))
        
        tree.addChild(self.mustBe('symbol', '='))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe('symbol', ';'))

        return tree


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree('ifStatement', '')

        tree.addChild(self.mustBe('keyword', 'if'))

        tree.addChild(self.mustBe('symbol', '('))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe('symbol', ')'))

        tree.addChild(self.mustBe('symbol', '{'))
        tree.addChild(self.compileStatements())
        tree.addChild(self.mustBe('symbol', '}'))

        if self.have('keyword', 'else'):
            tree.addChild(self.mustBe('keyword', 'else'))
            tree.addChild(self.mustBe('symbol', '{'))
            tree.addChild(self.compileStatements())
            tree.addChild(self.mustBe('symbol', '}'))

        return tree
    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree("whileStatement", "")

        tree.addChild(self.mustBe('keyword', 'while'))

        tree.addChild(self.mustBe('symbol', '('))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe('symbol', ')'))

        tree.addChild(self.mustBe('symbol', '{'))
        tree.addChild(self.compileStatements())
        tree.addChild(self.mustBe('symbol', '}'))

        return tree 

    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        tree = ParseTree('doStatement','')

        tree.addChild(self.mustBe('keyword', 'do'))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe('symbol', ';'))

        return tree


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        tree =ParseTree('returnStatement','')

        tree.addChild(self.mustBe('keyword', 'return'))
        
        if not self.have('symbol', ';'):
            tree.addChild(self.compileExpression()) # Parse an expression if it's present

        tree.addChild(self.mustBe('symbol', ';'))

        return tree


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        tree = ParseTree('expression','')

        if self.have('keyword', 'skip'):
            tree.addChild(self.mustBe('keyword', 'skip'))
            return tree

        tree.addChild(self.compileTerm())

        op = ['+','-','*','/','&','|','>','<','=']

        while self.have('symbol') and self.current().getValue() in op:
            tree.addChild(self.mustBe('symbol', self.current().getValue()))
            tree.addChild(self.compileTerm())

        return tree 


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        tree = ParseTree('term','')

        keywords=['true','false','null','this']
        
        if self.have('integerConstant'):
            tree.addChild(self.mustBe('integerConstant'))
        elif self.have('stringConstant'):
            tree.addChild(self.mustBe('stringConstant'))
        elif self.have('keyword') and self.current().getValue() in keywords:
            tree.addChild(self.mustBe('keyword', self.current().getValue()))
        elif self.have('identifier'):
            tree.addChild(self.mustBe('identifier'))
            if self.have('symbol','['):
                tree.addChild(self.mustBe('symbol','['))
                tree.addChild(self.compileExpression())
                tree.addChild(self.mustBe('symbol',']'))
            elif self.have('symbol','('):
                tree.addChild(self.mustBe('symbol','('))
                tree.addChild(self.compileExpressionList())
                tree.addChild(self.mustBe('symbol',')'))
            elif self.have('symbol','.'):
                tree.addChild(self.mustBe('symbol','.'))
                tree.addChild(self.mustBe('identifier'))
                tree.addChild(self.mustBe('symbol','('))
                tree.addChild(self.compileExpressionList())
                tree.addChild(self.mustBe('symbol',')'))
        elif self.have('symbol','('):
            tree.addChild(self.mustBe('symbol','('))
            tree.addChild(self.compileExpression())
            tree.addChild(self.mustBe('symbol',')'))
        elif self.have('symbol','-'):
            tree.addChild(self.mustBe('symbol','-'))
            tree.addChild(self.compileTerm())
        elif self.have('symbol','~'):
            tree.addChild(self.mustBe('symbol','~'))
            tree.addChild(self.compileTerm())
        else:
            raise Exception("Invalid term")

        return tree
    

    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        grammar: (expression (',' expression)*)?
        """
        tree = ParseTree('expressionList','')

        if self.have('symbol', ')'):
            return tree
        
        tree.addChild(self.compileExpression())

        while self.have('symbol',','):
            tree.addChild(self.mustBe('symbol',','))
            tree.addChild(self.compileExpression())

        return tree 


    def next(self):
        """
        Advance to the next token
        """
        self.current_index += 1
        return


    def current(self):
        """
        Return the current token
        @return the token
        """
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        else:
            return None 


    def have(self,expectedType,expectedValue=None):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        current_token = self.current()

        if current_token is None:
            return False
        elif expectedValue is not None:
            return current_token.node_type == expectedType and current_token.value == expectedValue
        else:
            return current_token.node_type == expectedType


    def mustBe(self, expectedType, expectedValue=None):
        """
        Check if the current token matches the expected type and (optionally) the expected value.
        If so, advance to the next token, returning the current token. If expectedValue is None, it matches any value.
        Otherwise, it must match the specific expectedValue, and if not, a ParseException is raised.
        @return token that was current prior to advancing.
        """
        current_token = self.current()

        if current_token.node_type == expectedType and current_token.value == expectedValue:
                self.next()
                return current_token
        elif expectedType == "integerConstant" and current_token.node_type == 'integerConstant':
            # Check integerConstant constraints here (e.g., between 0 to 32767)
            if 0 <= int(current_token.value) <= 32767:
                self.next()
                return current_token
        elif expectedType == "stringConstant":
            # Check stringConstant constraints here (e.g., must start and end with ")
            # if current_token.value[0] == '"' and current_token.value[-1] == '"':
            self.next()
            return current_token
        elif expectedType == "identifier" and current_token.node_type == 'identifier':
            # Check identifier constraints here (e.g., any sequence of letters, digits, and underscores, not starting with a digit)
            if not current_token.value[0].isnumeric():
                self.next()
                return current_token
        else:
            raise ParseException(f"Expected token of type '{expectedType}' with value '{expectedValue}', but found '{current_token.node_type}' with value '{current_token.value}'.")


if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    
    tokens.append(Token("identifier","Main"))
    tokens.append(Token("symbol","."))
    tokens.append(Token("identifier","myFunc"))
    tokens.append(Token("symbol","("))
    tokens.append(Token("integerConstant","1"))
    tokens.append(Token("symbol",","))
    tokens.append(Token("stringConstant","Hello"))
    tokens.append(Token("symbol",")"))
    
    parser = CompilerParser(tokens)
    
    result = parser.compileTerm()
    print(result)
