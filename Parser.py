from Lexer import *
from Translator import *

class Parser:
	lex = None
	token = None
	current_table = None

	def __init__(self, filepath):
		self.lex = Lexer(filepath)
		self.token = None
		self.current_table = None

		""" DEFINE FIRST SET """
		self.firstPrimaryExpression = set((Tag.ID, Tag.NUMBER, Tag.TRUE, Tag.FALSE, ord('(')))
		self.firstUnaryExpression = self.firstPrimaryExpression.union( set((ord('-'), ord('!'))) )
		self.firstExtendedMultiplicativeExpression = set((ord('*'), ord('/'), Tag.MOD))
		self.firstMultiplicativeExpression = self.firstUnaryExpression
		self.firstExtendedAdditiveExpression = set((ord('+'), ord('-')))
		self.firstAdditiveExpression = self.firstMultiplicativeExpression
		self.firstExtendedRelationalExpression = set((ord('<'), Tag.LEQ, ord('>'), Tag.GEQ))
		self.firstRelationalExpression = self.firstAdditiveExpression
		self.firstExtendedEqualityExpression = set((ord('='), Tag.NEQ))
		self.firstEqualityExpression = self.firstRelationalExpression
		self.firstExtendedConditionalTerm = set({Tag.AND})
		self.firstConditionalTerm = self.firstEqualityExpression
		self.firstExtendedConditionalExpression = set({Tag.OR})
		self.firstConditionalExpression = self.firstConditionalTerm
		self.firstExpression = self.firstConditionalExpression
		self.firstTextStatement = set({Tag.PRINT})
		self.firstAssigmentStatement = set({Tag.ID})
		self.firstStatement = self.firstAssigmentStatement.union(self.firstTextStatement)
		self.firstStatementSequence = self.firstStatement
		self.firstIdentifierList = set({ord(',')})
		self.firstDeclarationSequence = set({Tag.VAR})
		self.firstProgram = self.firstDeclarationSequence

	def error(self, extra = None):
		text = 'Line ' + str(self.lex.line) + " - " 
		if extra == None:
			text = text + "."
		else:
			text = text + extra
		raise Exception(text)

	def check(self, tag):
		if self.token.tag == tag:
			self.token = self.lex.scan()
			#print("", self.token)
		else:
			text = 'expected '
			if self.token.tag != Tag.ID:
				#print("tag = ", self.token.tag)
				aux = Token(tag)
				text = text + str(aux) + " before " + str(self.token) 
			else:
				text = text + "an identifier before " + str(self.token) 
			self.error(text)
	
	def analize(self):
		self.current_table = SymbolTable()
		self.token = self.lex.scan()
		tree = self.program()
		if self.token.tag == Tag.EOF:
			tree.eval(self.current_table)
	
	#<primary-expression> ::= <identifier> || <number> || <true>	|| <false> ||  '(' <expression> ')'
	def primaryExpression(self):
		if self.token.tag in self.firstPrimaryExpression:
			if self.token.tag == Tag.ID:
				name = self.token.value
				line = self.lex.line
				self.check(Tag.ID)
				return Identifier(name, line)
			elif self.token.tag == Tag.NUMBER:
				value = self.token.value
				self.check(Tag.NUMBER)
				return Number(value)
			elif self.token.tag == Tag.TRUE:
				self.check(Tag.TRUE)
				return Boolean(True)
			elif self.token.tag == Tag.FALSE:
				self.check(Tag.FALSE)
				return Boolean(False)
			elif self.token.tag == ord('('):
				self.check(ord('('))
				expression = self.expression()
				self.check(ord(')'))
				return expression
		else:
			self.error("expected a primary expression before " + str(self.token)) 

	#<unary-expression> ::= '-' <unary-expression> || '!' <unary-expression> || <primary-expression>
	def unaryExpression(self):
		if self.token.tag in self.firstUnaryExpression:
			if self.token.tag == ord('-'):
				self.check(ord('-'))
				expr = self.unaryExpression()
				return Minus(expr)
			elif self.token.tag == ord('!'):
				self.check(ord('!'))
				expr = self.unaryExpression()
				return Not(expr)
			else:
				return self.primaryExpression()
		else: 
			self.error("expected an unary expression before " + str(self.token))

	#<extended-multiplicative-expression> ::= '*' <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= '/' <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= MOD <unary-expression> <extended-multiplicative-expression>
	#<extended-multiplicative-expression> ::= ' '
	def extendedMultiplicativeExpression(self,left):
		if self.token.tag in self.firstExtendedMultiplicativeExpression:
			if self.token.tag == ord('*'):
				self.check(ord('*'))
				right = self.unaryExpression()
				node = Multiply(left,right)
				self.extendedMultiplicativeExpression(node)
			elif self.token.tag == ord('/'):
				self.check(ord('/'))
				right = self.unaryExpression()
				node = Divide(left, right)
				self.extendedMultiplicativeExpression(node)
			elif self.token.tag == Tag.MOD:
				self.check(Tag.MOD)
				right = self.unaryExpression()
				node = Modulo(left, right)
				self.extendedMultiplicativeExpression(node)
		else:
			return left

	#<multiplicative-expression> ::= <unary-expression> <extended-multiplicative-expression>
	def multiplicativeExpression(self):
		if self.token.tag in self.firstMultiplicativeExpression:
			expr = self.unaryExpression()
			return self.extendedMultiplicativeExpression(expr)
		else:
			self.error("expected an multiplicative expression before " + str(self.token))

	#<extended-additive-expression> ::= '+' <multiplicative-expression> <extended-additive-expression>
	#<extended-additive-expression> ::= '-' <multiplicative-expression> <extended-additive-expression>
	#<extended-additive-expression> ::= ' '
	def extendedAdditiveExpression(self,left):
		if self.token.tag in self.firstExtendedAdditiveExpression:
			if self.token.tag == ord('+'):
				self.check(ord('+'))
				right = self.multiplicativeExpression()
				node = Add(left,right)
				return self.extendedAdditiveExpression(node)
			elif self.token.tag == ord('-'):
				self.check(ord('-'))
				right = self.multiplicativeExpression()
				node = Subtract(left,right)
				return self.extendedAdditiveExpression(node)
		else:
			return left

	#<additive-expression> ::= <multiplicative-expression> <extended-additive-expression>
	def additiveExpression(self):
		if self.token.tag in self.firstAdditiveExpression:
			left = self.multiplicativeExpression()
			return self.extendedAdditiveExpression(left)
		else:
			self.error("expected an additive expression before " + str(self.token))

	#<extended-relational-expression> := '<' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= '<''=' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> := '>' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= '>''=' <additive-expression> <extended-relational-expression>
	#<extended-relational-expression> ::= ' '
	def extendedRelationalExpression(self,left):
		if self.token.tag in self.firstExtendedRelationalExpression:
			if self.token.tag == ord('<'):
				self.check(ord('<'))
				right = self.additiveExpression()
				node = Lesser(left,right)
				return self.extendedRelationalExpression(node)
			elif self.token.tag == ord('>'):
				self.check(ord('>'))
				right = self.additiveExpression()
				node = Larger(left,right)
				return self.extendedRelationalExpression(node)
			elif self.token.tag == Tag.LEQ:
				self.check(Tag.LEQ)
				right = self.additiveExpression()
				node = LesserEqual(left,right)
				return self.extendedRelationalExpression(node)
			elif self.token.tag == Tag.GEQ:
				self.check(Tag.GEQ)
				right = self.additiveExpression()
				node = LargerEqual(left,right)
				return self.extendedRelationalExpression(node)
		else:
			return left
	
	#<relational-expression> ::= <additive-expression> <extended-relational-expression>
	def relationalExpression(self):
		if self.token.tag in self.firstRelationalExpression:
			left = self.additiveExpression()
			return self.extendedRelationalExpression(left)
		else:
			self.error("expected an relational expression before " + str(self.token))

	#<extended-equality-expression> := '=' <relational-expression> <extended-equality-expression>
	#<extended-equality-expression> := '<''>' <relational-expression> <extended-equality-expression>
	#<extended-equality-expression> ::= ' '
	def extendedEqualityExpression(self,left):
		if self.token.tag in self.firstExtendedEqualityExpression:
			if self.token.tag == ord('='):
				self.check(ord('='))
				right = self.relationalExpression()
				node = Equal(left,right)
				return self.extendedEqualityExpression(node)
			elif self.token.tag == Tag.NEQ:
				self.check(Tag.NEQ)
				right = self.relationalExpression()
				node = NotEqual(left,right)
				return self.extendedEqualityExpression(node)
		else:
			return left

	#<equality-expression> ::= <relational-expression> <extended-equality-expression>
	def equalityExpression(self):
		if self.token.tag in self.firstEqualityExpression:
			left = self.relationalExpression()
			return self.extendedEqualityExpression(left)
		else:
			self.error("expected an equality expression before " + str(self.token))

	#<extended-conditional-term> ::= AND <equality-expression> <extended-conditional-term>
	#<extended-boolean-term> ::= ' '
	def extendedConditionalTerm(self,left):
		if self.token.tag in self.firstExtendedConditionalTerm:
			if self.token.tag == Tag.AND:
				self.check(Tag.AND)
				right = self.equalityExpression()
				node = And(left,right)
				return self.extendedConditionalTerm(node)
		else:
			return left

	#<conditional-term> ::= <equality-expression> <extended-conditional-term>
	def conditionalTerm(self):
		if self.token.tag in self.firstConditionalTerm:
			expr = self.equalityExpression()
			return self.extendedConditionalTerm(expr)
		else:
			self.error("expected an conditional term before " + str(self.token))

	#<extended-conditional-expression> ::= OR <conditional-term> <extended-conditional-expression>
	#<extended-conditional-expression> ::= ' '
	def extendedConditionalExpression(self,left):
		if self.token.tag in self.firstExtendedConditionalExpression:
			if self.token.tag == Tag.OR:
				self.check(Tag.OR)
				right = self.conditionalTerm()
				node = Or(left,right)
				return self.extendedConditionalExpression(node)
		else:
			return left

	#<conditional-expression> ::= <conditional-term> <extended-conditional-expression>
	def conditionalExpression(self):
		if self.token.tag in self.firstConditionalExpression:
			expr = self.conditionalTerm() #typo fix
			return self.extendedConditionalExpression(expr)
		else:
			self.error("expected an conditional expression before " + str(self.token))

	#<expression> ::= <conditional-expression>
	def expression(self):
		if self.token.tag in self.firstExpression:
			return self.conditionalExpression()
		else:
			self.error("expected an expression before " + str(self.token))

	#<text-statement> ::= PRINT '(' <expression> )'
	def textStatement(self):
		if self.token.tag in self.firstTextStatement:
			if self.token.tag == Tag.PRINT:
				self.check(Tag.PRINT)
				self.check(ord('('))
				expr = self.expression()
				self.check(ord(')'))
				return Print(expr)
		else:
			self.error("expected a text statement before " + str(self.token))

	#<assigment-statement> ::= <identifier> ':''=' <expression>
	def assigmentStatement(self):
		if self.token.tag in self.firstAssigmentStatement:
			if self.token.tag == Tag.ID:
				id_name = self.token.value
				line = self.lex.line
				self.check(Tag.ID)
				self.check(Tag.ASSIGN)
				expr = self.expression()
				return Assignment(id_name, expr, line)
		else:
			self.error("expected a assigment statement before " + str(self.token))
	
	#<statement> ::= <assignment-statement> | <text-statement>
	def statement(self):
		if self.token.tag in self.firstStatement:
			if self.token.tag in self.firstAssigmentStatement:
				return self.assigmentStatement()
			elif self.token.tag in self.firstTextStatement:
				return self.textStatement()
		else: 
			self.error("expected a statement before " + str(self.token))
	
	#<statement-sequence> ::= <statement> <statement-sequence>
	#<statement-sequence> ::= ' '
	# Recursively descend and append statements
	def statementSequence(self):
		statements = []
		while self.token.tag in self.firstStatementSequence:
			stmnt = self.statement()
			if stmnt:
				statements.append(stmnt)
		return statements #fixed identation LOL
	
	#<identifier-list> ::= ',' <identifier> <identifier-list>
	#<identifier-list> ::= ' '
	# not sure if i should handle the else here since ill call it recursively
	def identifierList(self):
		if self.token.tag in self.firstIdentifierList:
			if self.token.tag == ord(','):
				self.check(ord(','))
				id_name = self.token.value
				self.check(Tag.ID)
				self.current_table.insert(id_name)
				self.identifierList()
	
	#<declaration-sequence> ::= VAR <identifier> <identifier-list>
	def declarationSequence(self):
		if self.token.tag in self.firstDeclarationSequence:
			if self.token.tag == Tag.VAR:
				self.check(Tag.VAR)
				id_name = self.token.value
				self.check(Tag.ID)
				self.current_table.insert(id_name)
				self.identifierList()
		else: 
			self.error("expected a declaration sequence before " + str(self.token))

	#<program> ::= <declaration-sequence> <statement-sequence>
	def program(self):
		if self.token.tag in self.firstProgram:
			self.declarationSequence()
			statements = self.statementSequence()
			return Sequence(statements)
		else: 
			self.error("expected a program before " + str(self.token))