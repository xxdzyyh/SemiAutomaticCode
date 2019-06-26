path=$1

awk 'BEGIN {
	getter="";
	constraints="";
	subviews="";
	hasSubviewFn=0;
	hasConstraintsFn=0;
} {
	if ($0~/@property/) {
		propertyname=substr($5,2,length($5)-2);
		property="_"propertyname;
		
		if ($3!~/assign/) {
			if ($4~/Label/) {
				getter=getter"- ("$4" *)" propertyname "{\n	if (!"property") {\
		"property" = [["$4" alloc] init];\n\
		"property".font = kFontSize(14);\
		"property".textColor = UIColorFromRGB(0x<#color#>);\
	}\n	return "property";\n}\n\n";
			} else if ($4~/ImageView/) {
				getter=getter"- ("$4" *)" propertyname "{\n	if (!"property") {\
		"property" = [["$4" alloc] init];\n\
		"property".image = [UIImage imageNamed:@\"\"];\
	}\n	return "property";\n}\n\n";
			} else if ($4~/Button/) {
				getter=getter"- ("$4" *)" propertyname "{\n	if (!"property") {\
		"property" = [["$4" alloc] init];\n\
		["property" setTitleColor:UIColorFromRGB(0x22222) forState:UIControlStateNormal];\
		["property" setImage:[UIImage imageNamed:@\"\"] forState:UIControlStateNormal];\
		["property" setTitle:@\"\" forState:UIControlStateNormal];\
	}\n	return "property";\n}\n\n";
			} else if ($4~/TextField/) {
				getter=getter"- ("$4" *)" propertyname "{\n	if (!"property") {\
		"property" = [["$4" alloc] init];\n\
		"property".placeholder = @\"\";\
		"property".font = kFontSize(14);\
		"property".textColor = UIColorFromRGB(0x123456);\
		"property".keyboardType = UIKeyboardTypeDefault;\
	}\n	return "property";\n}\n\n";
			} else {
				getter=getter"- ("$4" *)" propertyname "{\n	if (!"property") {\
		"property" = [["$4" alloc] init];\
	}\n	return "property";\n}\n\n";
			}
			
			subviews=subviews"	[self addSubview:self."propertyname"];\n";
			constraints=constraints"  [self."propertyname" mas_makeConstraints:^(MASConstraintMaker *make) {\
			\
			}];\n\n";
		} 
	} else {
		if ($0~/setupSubviews/) {
			hasSubviewFn=1;
		}

		if ($0~/setupContraints/) {
			hasConstraintsFn=1;
		}
	}
} END {
	
	if (hasSubviewFn) {
		print subviews;
	} else {
		print "- (void)setupSubviews {\n	"subviews"\n}";
	}

	if (hasConstraintsFn) {
		print constraints >> "'$path'";
	} else {
		print "- (void)setupContraints {\n    "constraints"\n}";
	}

	print getter;

}' $1
