#!/bin/bash

awk '{
	if ($1~/Label/) {
		print "@property (nonatomic, strong) UILabel *"$1;
	} else if ($1~/Button/) {
		print "@property (nonatomic, strong) UIButton *"$1;
	} else if ($1~/TextField/) {
		print "@property (nonatomic, strong) UITextField *"$1;
	} else if ($1~/ImageView/) {
		print "@property (nonatomic, strong) UIImageView *"$1;
	} else {
		print "@property (nonatomic, strong) UIView *"$1;
	}
}' $1