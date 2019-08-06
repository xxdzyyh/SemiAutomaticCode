#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import re
import sys
import fileinput

from enum import Enum


def myPrint(value):
	#print(value)
	value = ''

# 词法分析是词素到词法单元的过程
class TokenType(Enum):
	Init = 0
	Operator = 1
	Number = 2
	Keyword = 3
	String = 4
	Separator = 5
	Identify = 6

# 词法单元
class Token(object):
	def __init__(this):
		# 行号
		this.line = 0
		# 类型
		this.type = TokenType.Init
		this.value = 0

	def __str__(this):
		return "line:" + str(this.line) + ", type:" + str(this.type) + ", value:" + '<' + str(this.value) + '>'

# 词法分析器
class Lexer(object):

	def __init__(this):
		# 设置语言关键字
		this.keywords = ['b','c','f','i','lbc','lbw','lc','p','t','tc','H','V']
		# 设置分隔符
		this.separator = [',','(',')','|','-','[',']']
		# 设置操作符
		this.operator = [':', '+', '=']
		this.tokenObjects = []
		this.line_num = 0

	def read_file(this):
		with fileinput.input() as f_input:
			return [line.strip() for line in f_input]

	def run(this,line):
		this.line_num = this.line_num + 1
		# 去掉空白行
		if len(line) < 1:
			return
		else:
			# 去掉注释
			if line.startswith('//'):
				return

		each = []
		for letter in line:
			each.append(letter)

		#
		op_first = ''
		word = ''
		# 判断单个字符不能确定是什么，需要进一步判断
		# 0 是初始值
		# 1 是操作符
		# 2 是常数NUM
		# 3 是关键字或变量名
		# 4 是字符串 STRING
		oflag = 0
		for e in each:
			if oflag == 1:
				# myPrint('<1,' + e + ',' + word + '>')
				if word + e in this.operator:
					# 这个位置处理操作符是多个字符的情况
					this.addToken(TokenType.Operator,word + e)
				elif e == ' ' or e == '':
					this.addToken(TokenType.Operator,op_first)
				elif re.match(r'[a-zA-Z\_]',e):
					word = word + e
					this.addToken(TokenType.Operator,op_first)
				oflag = 0
				op_first = ''
				continue
			elif oflag == 2: # 常数
				# myPrint('<2,' + e + ',' + word + '>')
				if e == '':
					this.addToken(TokenType.Number,word)
					word = ''
					oflag = 0
				elif e in this.separator:
					# myPrint('<2,Separator,' + e + ',' + word + '>')
					this.addToken(TokenType.Number,word)
					word = ''
					oflag = 0	
			elif oflag == 3: # 是关键字或变量名
				# myPrint('<3,' + e + ',' + word + '>')
				if e == '' or e == ' ':
					# myPrint('<3.1,' + e + ',' + word + '>')
					if word in this.keywords:
						this.addToken(TokenType.Keyword,word)	
					else:
						this.addToken(TokenType.Identify,word)
					word = ''
					oflag = 0
				elif e in this.separator:
					if word in this.keywords:
						this.addToken(TokenType.Keyword,word)	
					else:
						this.addToken(TokenType.Identify,word)
					
					this.addToken(TokenType.Separator,e)
					word = ''
					oflag = 0
				elif e in this.operator:
					if word in this.keywords:
						this.addToken(TokenType.Keyword,word)	
					else:
						this.addToken(TokenType.Identify,word)
					this.addToken(TokenType.Operator,e)	
					word = ''
					oflag = 0
				else:
					word = word + e
				continue
			elif oflag == 4:
				# myPrint('<4,' + e + ',' + word + '>')
				if e != '"':
					word = word + e
				elif e == '"':
					word = word + e
					this.addToken(TokenType.String,word)
					word = ''
					oflag = 0

				continue

			# 判断是否是操作符
			if e in this.operator:
				oflag = 1
				op_first = e
				continue

			# 判断是否是分隔符
			if e in this.separator:

				this.addToken(TokenType.Separator,e)
				continue

			# 判断是否是常数
			if re.match(r'[0-9\.]',e): 
				myPrint('<oflag:2,e:'+ e + 'word:'+ word +'>')
				oflag = 2
				word = word + e
				continue

			#判断是否是关键字或者变量名
			if re.match(r'[a-zA-Z\_]',e):
				oflag = 3
				word = word + e
				continue

			#判断是否是字符串
			if e == '"':
				oflag = 4
				word = word + e
				continue

		# 因为没有结束标志，所以需要在遍历完成后对word再次处理
		if len(word) > 0:
			if word in this.operator:
				this.addToken(TokenType.Operator,word)
			elif word in this.separator:
				this.addToken(TokenType.Separator,word)
			elif word in this.keywords:
				this.addToken(TokenType.Keyword,word)
			elif re.match(r'[a-zA-Z\_]',word):
				this.addToken(TokenType.Identify,word)
			

	def addToken(this,type,value):
		tokenObject = Token()
		tokenObject.type = type
		tokenObject.value = value
		tokenObject.line = this.line_num
		myPrint(tokenObject)
		this.tokenObjects.append(tokenObject)


# 语法分析器
class Parser(object):
	
	def __init__(this):
		this.result = ''
		this.declear = ''
		this.getter = ''
		this.subviews = '- (void)setupSubviews {'
		this.contraints = {}

	def run(this,tokens): 
		if len(tokens)  < 2:
			return
			
		token0 = tokens[0]
		token1 = tokens[1]

		propertyName = token0.value
		varName = '_' + propertyName
		className = this.viewTypeWithString(token0.value)

		# 0 方向未知
		# 1 左边
		# 2 右边
		orient = 0

		# 上一个视图
		preView = ''
		preValue = 0
		currentView = ''
		currentValue = 0
		preConstrains = ''
	
		# this.contraints = this.contraints + '\n\t'+ '[self.' + propertyName + ' mas_makeConstraints:^(MASConstraintMaker *make) {\n';

		if token0.type == TokenType.Keyword:
			# 词素描述的是约束
			# myPrint('创建约束')
			# myPrint(token0)
			if token0.value == 'V':
				i = 1	
				while i < len(tokens):
					tokeni = tokens[i]
					tokeni1 = tokens[i-1]
					if tokeni.type == TokenType.Number:
						if tokeni1.value == '(':
							if len(currentView):
								myPrint('<Height:' + str(tokeni1) + str(tokeni) + '>')
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t'+ 'make.height.mas_equalTo(scaleY(' + tokeni.value + '));'
						else:
							if currentView == '|':
								myPrint('<Top:' + str(tokeni1) + str(tokeni) + '>')
								preConstrains = preConstrains + '\n\t\t'+ 'make.top.mas_equalTo(scaleY(' + tokeni.value + '));'
							else:
								currentValue = tokeni.value

					elif tokeni.type == TokenType.Identify:
						if len(currentView) == 0:
							currentView = tokeni.value;
						else:
							preView = currentView
							currentView = tokeni.value;
							myPrint('<' + str(currentValue) +'>')
							if float(currentValue) > 0:
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t' +'make.top.equalTo(self.' + preView + '.mas_bottom).offset(scaleY('+ currentValue +'));'
								currentValue = 0

							if preView == '|':
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + preConstrains
								preConstrains = ''
							
							if tokeni1.value == '[':
								if len(currentView):
									myPrint('<CenterY:' + str(tokeni1) + str(tokeni) + '>')

									if preView == '|':
										this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t'+ 'make.centerY.mas_equalTo(0);'
									else:
										this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t'+ 'make.centerY.equalTo(' + preView +');'

					elif tokeni.value == '|':
						if len(currentView) == 0:
							currentView = tokeni.value;
						else:
							if tokeni1.value == '-':
								if len(currentView):
									this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t' + 'make.bottom.mas_equalTo(-scaleY('+ str(currentValue) +'));'


					i = i + 1
						
			elif token0.value == 'H':
				i = 1	
				while i < len(tokens):
					tokeni = tokens[i]
					tokeni1 = tokens[i-1]
					if tokeni.type == TokenType.Number:
						if tokeni1.value == '(':
							if len(currentView):
								myPrint('<Width:' + str(tokeni1) + str(tokeni) + '>')
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t'+ 'make.width.mas_equalTo(' + tokeni.value + ');'
						else:
							if currentView == '|':
								myPrint('<Left:' + str(tokeni1) + str(tokeni) + '>')
								preConstrains = preConstrains + '\n\t\t'+ 'make.left.mas_equalTo(scaleX(' + tokeni.value + '));'
							else:
								# 到下一个identify才能确定约束怎么写
								currentValue = tokeni.value

					elif tokeni.type == TokenType.Identify:
						if len(currentView) == 0:
							currentView = tokeni.value;
							if len(preConstrains):
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {\n') + preConstrains
								preConstrains = ''
						else:
							preView = currentView
							currentView = tokeni.value;
							if float(currentValue) > 0:
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t'+'make.left.equalTo('+ preView +'.mas_right).offset(scaleX('+ str(currentValue) +'));'
							if preView == '|':
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + preConstrains
								preConstrains = ''
					elif tokeni.value == '|':
						if len(currentView) == 0:
							# 开始的 |
							currentView = tokeni.value;
						else:
							# 结束的 |
							if (tokeni1.value == '-'):
								this.contraints[currentView] = this.contraints.get(currentView,'['+ currentView + ' mas_makeConstraints:^(MASConstraintMaker *make) {') + '\n\t\t'+'make.right.mas_equalTo(-scaleX('+ str(currentValue) +'));'

					i = i + 1
		elif token0.type == TokenType.Identify:
			if token1.type == TokenType.Separator:
				# 词素描述的是控件属性
				
				this.declear =  this.declear + "@property (nonatomic, strong) " + className + ' *' + str(token0.value) + ';\n'
				getter = '- (' + className + '*)' + propertyName + ' {\n'
				getter = getter + '\t' + 'if (!'+ varName + ') {\n'
				getter = getter + '\t\t' + varName + '= [[' + className + ' alloc] init];\n'

				i = 2
				while i < len(tokens):
					tokeni = tokens[i]
					if tokeni.type == TokenType.Keyword:
						tokeni2 = tokens[i+2]
						if tokeni.value == 'b':
							getter = getter + '\t\t' + varName + '.backgroundColor = UIColorFromRGB(' + str(tokeni2.value) + ');\n'
						elif tokeni.value == 'f':
							if 'button' in className.lower():
								getter = getter + '\t\t' + varName + '.titleLabel.font = kFontSize('+str(tokeni2.value)+ ');\n'
							elif 'label' in className.lower():
								getter = getter + '\t\t' + varName + '.font = kFontSize('+str(tokeni2.value)+ ');\n'
						elif tokeni.value == 'i':
							if 'button' in className.lower():
								getter = getter + '\t\t' + '[' + varName + ' setImage:[UIImage imageNamed:@'+str(tokeni2.value)+ '] forState:UIControlStateNormal];\n'
							elif 'imageview' in className.lower():
								getter = getter + '\t\t' + varName + '.image = [UIImage imageNamed:@'+str(tokeni2.value)+ '];\n'
						elif tokeni.value == 't':
							if 'button' in className.lower():
								getter = getter + '\t\t' + '[' + varName + ' setTitle:@' + str(tokeni2.value) + ' forState:UIControlStateNormal];\n'
							else:
								getter = getter + '\t\t' + varName + '.text = @'+str(tokeni2.value)+ ';\n'
						elif tokeni.value == 'tc':
							if 'button' in className.lower():
								getter = getter + '\t\t' + '[' + varName + ' setTitleColor:UIColorFromRGB('+str(tokeni2.value)+ ') forState:UIControlStateNormal];\n'
							else:
								getter = getter + '\t\t' + varName + '.textColor = UIColorFromRGB('+str(tokeni2.value)+ ');\n'
						elif tokeni.value == 'lc':
							getter = getter + '\t\t' + varName + '.layer.cornerRadius = ' + str(tokeni2.value)+ ';\n'
							getter = getter + '\t\t' + varName + '.layer.masksToBounds = YES;\n'
						elif tokeni.value == 'lbc':
							getter = getter + '\t\t' + varName + '.layer.borderColor = UIColorFromRGB(' + str(tokeni2.value)+ ').CGColor;\n'
						elif tokeni.value == 'lbw':
							getter = getter + '\t\t' + varName + '.layer.borderWidth = ' + str(tokeni2.value)+ ';\n'

					i = i + 2

				getter = getter + '\t}\n'
				getter = getter + '\t' + 'return ' + varName + ';\n}\n'

				this.getter = this.getter + '\n' + getter;

			elif token1.type == TokenType.Operator:
				# 词素描述的控件关系
				myPrint('创建控件关系')
				i = 2;
				while i < len(tokens):
					tokeni = tokens[i]
					
					if tokeni.type == TokenType.Identify:
						this.subviews = this.subviews + '\n\t' + '[' + token0.value + ' addSubview:self.' + tokeni.value + '];'
					i = i + 1

	
	def finish(this):
		this.subviews = this.subviews + '\n}\n'
		this.contraints = this.contraints 

		finalCons = '- (void)setupConstraints {'
		for cst in this.contraints.values():
			finalCons = finalCons + '\n\t' + cst + '\n\t}];\n'
		
		finalCons = finalCons + '\n}'

		this.result = this.result + '\n' + this.declear + '\n#pragma mark - Private Methods\n\n'+ this.subviews + '\n' + finalCons + '\n#pragma mark - Property\n\n' + this.getter


	def viewTypeWithString(this,string):
		if 'label' in string.lower():
			return 'UILabel'
		elif 'button' in string.lower():
			return 'UIButton'
		elif 'textfield' in string.lower():
			return 'UITextField'
		elif 'imageview' in string.lower():
			return 'UIImageView'
		elif 'textview' in string.lower():
			return 'UITextView'
		elif 'scrollview' in string.lower():
			return 'UIScrollView'
		else: 
			return 'UIView'


if __name__ == '__main__':
	lexer = Lexer()
	parser = Parser()

	lines = lexer.read_file()

	for line in lines:
		lexer.run(line)
		parser.run(lexer.tokenObjects)
		lexer.tokenObjects = []

	parser.finish()
	print(parser.result)
