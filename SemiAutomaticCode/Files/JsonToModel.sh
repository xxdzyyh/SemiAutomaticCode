awk -F '"' '{
	if ($2 > 0) {
		if ($4 > 0) {
			print "@property (nonatomic, copy) NSString *"$2";";
		} else {
			print "@property (nonatomic, strong) NSNumber *"$2";";
		}
	}
}' $1