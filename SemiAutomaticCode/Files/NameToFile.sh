#!/bin/bash

array=$(awk '{
	if ($1~/Label/) {
		print "@property (nonatomic, strong) UILabel *"$1";";
	} else if ($1~/Button/) {
		print "@property (nonatomic, strong) UIButton *"$1";";
	} else if ($1~/TextField/) {
		print "@property (nonatomic, strong) UITextField *"$1";";
	} else if ($1~/ImageView/) {
		print "@property (nonatomic, strong) UIImageView *"$1";";
	} else {
		print "@property (nonatomic, strong) UIView *"$1";";
	}
}' $1)

echo $array | sed 's/;/;\n/g;' | awk 'BEGIN {
	declear="";
	getter="";
	constraints="";
	subviews="";
} {
	if ($0~/@property/) {
		declear=declear$0"\n"

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
	}
} END {
	print declear;
    print "- (void)setupSubviews {\n	"subviews"\n}";
    print "- (void)setupContraints {\n    "constraints"\n}";
	print getter;
}' 





