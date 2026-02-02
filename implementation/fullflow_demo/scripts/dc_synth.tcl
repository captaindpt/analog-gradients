set TOP "alu4_flow_demo"

if {![info exists ::env(REPO_DIR)]} {
    puts "ERROR: REPO_DIR environment variable is not set."
    exit 2
}

set REPO_DIR $::env(REPO_DIR)
set WORK_DIR "$REPO_DIR/implementation/fullflow_demo/work/dc"
set RTL_FILE "$REPO_DIR/implementation/fullflow_demo/rtl/${TOP}.v"
set SDC_FILE "$REPO_DIR/implementation/fullflow_demo/constraints/${TOP}.sdc"

if {[info exists ::env(DC_TARGET_LIB)]} {
    set TARGET_LIB $::env(DC_TARGET_LIB)
} else {
    set TARGET_LIB "/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/timing/slow_vdd1v0_basicCells.lib"
}

file mkdir $WORK_DIR
file mkdir "$WORK_DIR/reports"
file mkdir "$WORK_DIR/out"

set_app_var search_path [list "." [file dirname $TARGET_LIB] "$REPO_DIR/implementation/fullflow_demo/rtl"]
set_app_var target_library [list $TARGET_LIB]
set_app_var link_library [concat "*" $target_library]
set_app_var synthetic_library [list dw_foundation.sldb]

define_design_lib WORK -path "$WORK_DIR/work"

analyze -format verilog $RTL_FILE
elaborate $TOP
current_design $TOP
link

source $SDC_FILE

set_fix_multiple_port_nets -all -buffer_constants
compile

report_qor > "$WORK_DIR/reports/${TOP}_qor.rpt"
report_area -hierarchy > "$WORK_DIR/reports/${TOP}_area.rpt"
report_timing -max_paths 20 > "$WORK_DIR/reports/${TOP}_timing.rpt"

write -hierarchy -format verilog -output "$WORK_DIR/out/${TOP}_mapped.v"
write_file -format ddc -hierarchy -output "$WORK_DIR/out/${TOP}.ddc"
write_sdc "$WORK_DIR/out/${TOP}.sdc"

exit
