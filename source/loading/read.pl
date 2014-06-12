#!usr/bin/perl 


# io section
$filein = "classifications.txt";
$file = "qa.out";
open(OUT, ">$file");
open(FILEIN, "$filein");

# read in the data
$i=0;
while(<FILEIN>) {
chop;
        ($diagnosis[$i],$type[$i],$t) = split(",");
	$id[$i] = $t*1;
	if($i>0 && $type[$i] eq 'textual'){
	$data{$id[$i]}{$diagnosis[$i]}++;
	if($type[$i] eq 'textual'){$text++;}
	if($type[$i] eq 'intuitive'){$intuit++;}
	$cases{$id[$i]}++;
	$diag{$diagnosis[$i]}++;
	}
	$i++;
        }

	$kk = 0;
	foreach $case (sort keys %cases){
	#printf( "%4d - %s ",$kk,$case);
	foreach $diag (sort keys %diag){
	#printf( "%d ",$data{$case}{$diag});
	}
	$kk++;	
	$count++;
	#print "\n";
	}
	
	print "Cases: $count\n";
	print "Types: $text $intuit\n";


    foreach $diag (sort keys %diag){
	$d[$l] = $diag;
        #printf( "%4d %s\n",$diag{$diag},$diag);
	$l++;
	}

        for($i=0;$i<@d;$i++){
	print "$d[$i] ";
	}
	print "\n";
	$kk = 0;
        foreach $case (sort keys %cases){
        #printf( "%4d-%s ",$kk,$case);
	#print "\n";
	for($i=0;$i<@d;$i++){
        printf( "%d ",$data{$case}{$d[$i]});
        }
	$kk++;
	printf( "\n");}



