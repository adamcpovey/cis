#!/bin/bash -e

SUBJECT=othercontourf

#########################################
# Code in this section not to be modified.
#########################################
# The current directory.
TEST_DIR=`pwd`
# The full path of the directory containing the common build and run scripts.
ROOT_TEST_DIR="${TEST_DIR}/.."

source_dir="${ROOT_TEST_DIR}/test_files/"

rm -f "O$SUBJECT.png"
# load in the standard functions
. "$TEST_DIR/CommonFunctions.sh"
########################################

#################################
# Place the execution lines below.
#
#################################
start_time="$(date +%s)"

cis plot RVOD_liq_water_content:${source_dir}2007180125457_06221_CS_2B-CWC-RVOD_GRANULE_P_R04_E02.hdf --type contour --xlabel overiddenxlabel --itemwidth 4 --fontsize 15 --height 10 --ymin 0 --ymax 10000 --vmin 0 --vstep 300 --cbarorient horizontal --grid --xaxis latitude --yaxis altitude --output "O$SUBJECT.png"

end_time="$(($(date +%s)-start_time))"
echo "Time taken: ${end_time}s"
#################################
#
# Call standard function that compares the results and removes and unnecessary files
CompareResultsAndClean
# exit code is 0 for success and 1 for failure.
exit $COMPARE_RESULTS_RETURN_VALUE

######################### END OF SCRIPT ####################################
