create_library_set -name LIBSET -timing /CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/timing/slow_vdd1v0_basicCells.lib
create_rc_corner -name RC -qx_tech_file /CMC/kits/cadence/GPDK045/gsclib045_all_v4.4/gsclib045/qrc/qx/gpdk045.tch
create_delay_corner -name DELAY -library_set LIBSET -rc_corner RC
create_constraint_mode -name CONSTR -sdc_files /home/v71349/analog-gradients/implementation/fullflow_demo/constraints/alu4_flow_demo.sdc
create_analysis_view -name VIEW -constraint_mode CONSTR -delay_corner DELAY
set_analysis_view -setup VIEW -hold VIEW
