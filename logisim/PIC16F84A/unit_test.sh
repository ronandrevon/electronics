#! /bin/bash
# Runs a series of unit tests based on the programs found in programs/*.pic. Provides a report 
#   The programs are compiled, flashed into the ROM of the PIC16F84A.circ and run through the PIC_tester.circ 
#   where the halt condition is reached after the last instruction has been executed
#   Note : To prevent overriding the original files(bin/*.out, PIC16F84A.circ, PIC_tester.circ)
#          temporary copies are used and retrieved in dat/tests/


# some definitions
dir=`dirname $0`                    # base folder of the PIC project 
source $dir/../../../colors.sh      #color constants (not important)
cxx="$dir/compiler.py"              #compiler
flash=$dir"/programs/flash_PIC.sh"  #flashing program

#### directories and files
test_dir="$dir/dat/tests"
lib_dir="$test_dir/lib"             #copy library over so it can be run locally
cxx_dir="$test_dir/bin"             #binary files folder for the tests
exe_dir="$test_dir/run"             #run result files folder for the tests
logfile=$test_dir/unit_test.log
errfile=$test_dir/unit_test.err
tests="mult_test.pic"
#tests=$(ls $dir/programs/*.pic | xargs -n1 basename)

#### setup the dat/tests folder
rm -rf $test_dir/*
cp $dir/PIC_tester.circ $test_dir                           #copy tester and PIC
mkdir $cxx_dir $exe_dir $lib_dir                            #create folders
cp $dir/lib/* $lib_dir                                      #copy libraries


#### compile and run the programs
date>$logfile
date>$errfile
printf $yellow"%-20s : " program; printf $yellow"cxx exe\n"$black
for test in $tests; do
    printf "$purple\t$test:\n$black" >> $logfile
    printf "$purple\t$test:\n$black" >> $errfile
    printf "%-20s : " $test
    
    #Compile
    test_out=$cxx_dir/$test"_unit.out"
    $cxx $dir/programs/$test -o $test_out &>> $logfile; ccx_r=$?
    printf "$ccx_r   "
    
    #flash and run 
    exe_r=1
    if [ $ccx_r -eq 0 ]; then
        #Flash the program binaries into the Flash memory(ROM) of circuit PIC16F84A.circ 
        $flash $test_out
        
        #Modify the halt condition for the execution of this program
        pcmax=$(python3 -c "print(hex(  $(wc -l $test_out | cut -d' ' -f1)  ))") #;echo $pcmax
        sed -i "/Constant/,/<\/comp>/{s/0x[0-9a-f]*/$pcmax/; t;}" $test_dir/PIC_tester.circ
        
        # run the corresponding PIC_tester circuit 
        logisim $test_dir/PIC_tester.circ -tty table,halt,speed > $exe_dir/$test.txt 2>>$errfile; exe_r=$?
    fi
    printf "$exe_r   \n"
    
done

#printf "\n\n\t"$green"LOGFILE"$black"
#cat $logfile

#diff --color test_ref_table.txt test_tmp_table.txt
#./chronogram.py test_tmp_table.txt