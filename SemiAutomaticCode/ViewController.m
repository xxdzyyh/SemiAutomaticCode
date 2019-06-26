//
//  ViewController.m
//  SemiAutomaticCode
//
//  Created by xiaoniu on 2019/6/26.
//  Copyright © 2019 com.bluefin. All rights reserved.
//

#import "ViewController.h"

#define kNameToDeclear @"控件名字生成属性声明"
#define kDeclearToFile @"控件属性声明生成getter"
#define kJsonToDeclear @"Json生成属性声明"
#define kNameToFile    @"控件名字生成getter/addSubview.."

@interface ViewController()

@property (weak) IBOutlet NSPopUpButton *popUpButton;
@property (nonatomic, strong) NSText *text;

@property (weak) IBOutlet NSButton *commitButton;
@property (unsafe_unretained) IBOutlet NSTextView *inputTextView;
@property (unsafe_unretained) IBOutlet NSTextView *outputTextView;

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self setupItems];
}

- (void)setupItems {
    [self.popUpButton removeAllItems];
    [self.popUpButton addItemsWithTitles:@[kNameToDeclear,kDeclearToFile,kJsonToDeclear]];
}

- (void)setRepresentedObject:(id)representedObject {
    [super setRepresentedObject:representedObject];

    // Update the view, if already loaded.
}

- (IBAction)commitButtonClick:(id)sender {
    NSTask *shellTask = [[NSTask alloc] init];
    [shellTask setLaunchPath:@"/bin/bash"];
    
    NSString *shellScriptPath = nil;
    
    if ([self.popUpButton.selectedItem.title isEqualToString:kNameToDeclear]) {
        shellScriptPath = [[NSBundle mainBundle] pathForResource:@"NameToDeclear" ofType:@"sh"];
    } else if ([self.popUpButton.selectedItem.title isEqualToString:kDeclearToFile]) {
        shellScriptPath = [[NSBundle mainBundle] pathForResource:@"declearToFile" ofType:@"sh"];
    } else if ([self.popUpButton.selectedItem.title isEqualToString:kJsonToDeclear]) {
        shellScriptPath = [[NSBundle mainBundle] pathForResource:@"JsonToModel" ofType:@"sh"];
    } else if ([self.popUpButton.selectedItem.title isEqualToString:kNameToFile]) {
        
    }
    
    NSString *shellStr = [NSString stringWithFormat:@"echo '%@' | sh %@",self.inputTextView.string,shellScriptPath];
    
    // -c 表示将后面的内容当成shellcode来执行
    [shellTask setArguments:[NSArray arrayWithObjects:@"-c",shellStr, nil]];
    
    NSPipe *pipe = [[NSPipe alloc]init];
    
    [shellTask setStandardOutput:pipe];
    [shellTask launch];
    
    NSFileHandle *file = [pipe fileHandleForReading];
    NSData *data =[file readDataToEndOfFile];
    NSString *strReturnFromShell = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
    
    NSLog(@"The return content from shell script is: %@",strReturnFromShell);
    
    self.outputTextView.string = strReturnFromShell;
}

@end
