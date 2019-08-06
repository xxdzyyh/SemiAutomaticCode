#!/bin/bash
alias gnu-sed="/usr/local/opt/gnu-sed/libexec/gnubin/sed"

authorInfoFunc() {
	mdate=`date +%Y/%m/%d`
	year=${mdate%%/*}
	info="//\n//	$1\n//  XNOnline\n//\n//  Created by ${USER} on ${mdate}.\n//  Copyright © ${year} xiaoniu88. All rights reserved.\n//\n\n

"
	echo $info
}

createTable() {
echo "createTable"
echo $1
echo $2

	list=$1ListVC
	authorInfo=`authorInfoFunc ${list}.h`

	echo "${authorInfo}

#import \"XFFoundation.h\"

@interface $list : XFRefreshTableViewController

@end
" >> ${list}.h


# tableType
#	refresh 下拉刷新，没有加载更多
#   refresh & load  more 下拉刷新上拉加载更多
#   simple 没有下拉刷新和加载更多

refresh=""
if [[ $2 == "simple" ]]; then
	refresh="
	self.canUpdateData = NO;
	self.canAppendData = NO;
"	
elif [[ $2 == 'refresh' ]]; then
	refresh="self.canAppendData = NO;"
else
	refresh=""	
fi
	authorInfo=`authorInfoFunc ${list}.m`
	echo "${authorInfo}
#import \"${list}.h\"

#import \"$1.h\"
#import \"$1Cell.h\"
#import \"RequestResult.h\"
#import \"$1DetailVC.h\"
#import <YYModel/YYModel.h>
#import <SVProgressHUD/SVProgressHUD.h>

//typedef NS_ENUM(NSUInteger,$1CellType) {
//    $1CellTypeOne,
//    $1CellCount
//};

@interface ${list} ()

@end

@implementation ${list}

#pragma mark - Life Cycle

- (void)viewDidLoad {
    [super viewDidLoad];

    ${refresh}
    [self sendDefaultRequest];
}

#pragma mark - Request

- (NSString *)defaultPath {
	return @\"\";
}

- (void)sendDefaultRequest {
    XFRequest *request = [[XFRequest alloc] initWithPath:[self defaultPath] finish:^(XFRequest *request, id result) {
        if (self.page == [self startPage]) {
            [self.refreshHeader endRefreshing];
        } else {
            [self.refreshFooter endRefreshing];
        }
		
		RequestResult *res = [RequestResult yy_modelWithJSON:result];
        
        if (res.isSuccess) {
            NSArray *array = [NSArray yy_modelArrayWithClass:[self modelClass] json:res.data];
            
            if (self.page == [self startPage]) {
                self.dataSource = [array mutableCopy];
            } else {
                [self.dataSource addObjectsFromArray:array];
            }
        } else {
        	Toast(res.msg);
        }
    }];
    
    [self.mainQueue push:request];
}


#pragma mark - <UITableViewDelegate>

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
	return $1CellCount;
}


$cellForRow

$didSelectRow

$cellHeight

@end

" >> ${list}.m

}


#typedef NS_ENUM(NSUInteger,MyTeamCellType) {
#    MyTeamCellTypeOne,
#    MyTeamCellCount
#};

# MyTeamCellType
enumName=$(grep 'typedef NS_ENUM' $1 | gnu-sed 's/.*,\(.*\)).*/\1/g')
# MyTeam
prefix=`echo $enumName | gnu-sed 's/CellType//'`

enumValues=$(awk -F "," 'BEGIN {
	enumValues="";
} { 
	if (match($1,"'$prefix'")) {
		# 去掉 $1 前面的空格
		sub("^ *","",$1);
		enumValue=$1;
		
		sub(".*CellType","",enumValue);
		if (enumValue !~ /Count/) {
			enumValues=enumValues""$1" ";
			fileName="'$prefix'"enumValue;
			system("sh ./TaoTemplate.sh "fileName" cell");
		} else {
			
		}
	}
} END {
	print enumValues;
}' $1)

echo $enumValues

cellForRow="- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
	switch (indexPath.row) {"

didSelectRow="- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
    [tableView deselectRowAtIndexPath:indexPath animated:YES];
    switch (indexPath.row) {"

heightForRow="- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {"

for i in ${enumValues[*]}; do

cellName=`echo $i | sed 's/CellType//' `
cellName=${cellName}"Cell"
cellForRow=$cellForRow"\n\t\tcase $i: {
	\t\t$cellName *cell = [$cellName cellForTableView:tableView];
	\t\t[cell configCellWithData:[NSObject new]];
	\t\treturn cell;
\t\t}\n\t\t\tbreak;"


didSelectRow=$didSelectRow"\n\t\tcase $i: {\n\t\t
\t\t}
\t\t\tbreak;"


heightForRow=$heightForRow"\n\tcase $i: {\n\t\t
	return [$cellName cellHeight];
\n\t}\n\tbreak;\n"
done

cellForRow=$cellForRow"\n\t\tdefault: {
	\t\treturn [SplitCell cellForTableView:tableView];
\t\t}\t\t\t
            break;\n\t}\n}"

didSelectRow=$didSelectRow"\n\t\tdefault:
            break;\n\t}\n}"

heightForRow=$heightForRow"\n\t\tdefault:\n\t\t
	return [SplitCell cellHeight];\n
            break;\n\t}\n}"

cellCount=`grep CellCount $1 | sed s/CellCount//`

echo $cellCount

createTable $cellCount



