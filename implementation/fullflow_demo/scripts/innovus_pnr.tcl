set TOP "alu4_flow_demo"

if {![info exists ::env(REPO_DIR)]} {
    puts "ERROR: REPO_DIR environment variable is not set."
    exit 2
}

set REPO_DIR $::env(REPO_DIR)
set WORK_DIR "$REPO_DIR/implementation/fullflow_demo/work/innovus"
set NETLIST "$REPO_DIR/implementation/fullflow_demo/work/dc/out/${TOP}_mapped.v"
set SDC_FILE "$REPO_DIR/implementation/fullflow_demo/constraints/${TOP}.sdc"

if {[info exists ::env(DC_TARGET_LIB)]} {
    set TARGET_LIB $::env(DC_TARGET_LIB)
} else {
    set TARGET_LIB "/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/timing/slow_vdd1v0_basicCells.lib"
}

if {[info exists ::env(GPDK045_TECH_LEF)]} {
    set TECH_LEF $::env(GPDK045_TECH_LEF)
} else {
    set TECH_LEF "/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/lef/gsclib045_tech.lef"
}

if {[info exists ::env(GPDK045_MACRO_LEF)]} {
    set MACRO_LEF $::env(GPDK045_MACRO_LEF)
} else {
    set MACRO_LEF "/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/lef/gsclib045_macro.lef"
}

if {[info exists ::env(GPDK045_QRC)]} {
    set QRC_FILE $::env(GPDK045_QRC)
} else {
    set QRC_FILE "/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/qrc/qx/gpdk045.tch"
}

if {[info exists ::env(GPDK045_STD_GDS)]} {
    set STD_GDS $::env(GPDK045_STD_GDS)
} else {
    set STD_GDS "/CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/gds/gsclib045.gds"
}

file mkdir $WORK_DIR
file mkdir "$WORK_DIR/reports"
file mkdir "$WORK_DIR/out"

if {![file exists $NETLIST]} {
    puts "ERROR: Netlist does not exist: $NETLIST"
    exit 3
}

set MMMC_FILE "$WORK_DIR/mmmc.tcl"
set m [open $MMMC_FILE w]
puts $m "create_library_set -name LIBSET -timing [list $TARGET_LIB]"
puts $m "create_rc_corner -name RC -qx_tech_file $QRC_FILE"
puts $m "create_delay_corner -name DELAY -library_set LIBSET -rc_corner RC"
puts $m "create_constraint_mode -name CONSTR -sdc_files [list $SDC_FILE]"
puts $m "create_analysis_view -name VIEW -constraint_mode CONSTR -delay_corner DELAY"
puts $m "set_analysis_view -setup [list VIEW] -hold [list VIEW]"
close $m

set init_design_settop 1
set init_verilog $NETLIST
set init_top_cell $TOP
set init_lef_file "$TECH_LEF $MACRO_LEF"
set init_mmmc_file $MMMC_FILE
set init_pwr_net VDD
set init_gnd_net VSS

init_design

clearGlobalNets
globalNetConnect VDD -type pgpin -pin VDD -all
globalNetConnect VSS -type pgpin -pin VSS -all
applyGlobalNets

floorPlan -site CoreSite -r 1.0 0.70 10 10 10 10

placeDesign
routeDesign

report_area > "$WORK_DIR/reports/${TOP}_area.rpt"
report_timing -max_paths 20 > "$WORK_DIR/reports/${TOP}_timing.rpt"
report_power > "$WORK_DIR/reports/${TOP}_power.rpt"

defOut "$WORK_DIR/out/${TOP}.def"
saveNetlist "$WORK_DIR/out/${TOP}_postroute.v"

set gds_out "$WORK_DIR/out/${TOP}.gds"
if {[catch {streamOut $gds_out -merge [list $STD_GDS] -units 1000 -mode ALL} err]} {
    puts "WARN: streamOut failed: $err"
    set sf [open "$WORK_DIR/reports/${TOP}_streamout.warn" w]
    puts $sf $err
    close $sf
} else {
    puts "INFO: streamOut completed: $gds_out"
}

exit
