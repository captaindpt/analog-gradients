; L5_inverter.il - CMOS Inverter Schematic
; Level 5: Basic CMOS building block
; Usage: Load in Virtuoso CIW: load("/home/v71349/analog-gradients/skill/L5_inverter.il")

procedure(createInverter()
    let((lib cell view cv pmos nmos vdd gnd inPin outPin)

        lib = "gpu_lib"
        cell = "inverter"
        view = "schematic"

        ; Create or open the cellview
        cv = dbOpenCellViewByType(lib cell view "schematic" "w")

        if(cv then
            printf("Creating inverter schematic in %s/%s/%s\n" lib cell view)

            ; === INSTANCES ===
            ; PMOS: source=VDD, gate=IN, drain=OUT
            pmos = dbCreateInst(cv "analogLib" "pmos4" "symbol" "PM0"
                list(0.0 0.5) "R0")

            ; NMOS: source=GND, gate=IN, drain=OUT
            nmos = dbCreateInst(cv "analogLib" "nmos4" "symbol" "NM0"
                list(0.0 -0.5) "R0")

            ; VDD supply
            vdd = dbCreateInst(cv "analogLib" "vdd" "symbol" "VDD"
                list(0.0 1.2) "R0")

            ; GND
            gnd = dbCreateInst(cv "analogLib" "gnd" "symbol" "GND"
                list(0.0 -1.2) "R0")

            ; === NETS ===
            ; Create nets for connectivity
            dbCreateNet(cv "VDD")
            dbCreateNet(cv "GND")
            dbCreateNet(cv "IN")
            dbCreateNet(cv "OUT")

            ; === PINS (I/O interface) ===
            inPin = dbCreatePin(
                dbCreateNet(cv "IN")
                dbCreateInst(cv "basic" "ipin" "symbol" nil list(-1.0 0.0) "R0")
                "IN" "input"
            )

            outPin = dbCreatePin(
                dbCreateNet(cv "OUT")
                dbCreateInst(cv "basic" "opin" "symbol" nil list(1.0 0.0) "R0")
                "OUT" "output"
            )

            ; === WIRES ===
            ; VDD to PMOS source
            dbCreateWire(cv "route" "full"
                list(list(0.0 1.2) list(0.0 0.8)) 0.0625 nil nil)

            ; PMOS drain to NMOS drain (output node)
            dbCreateWire(cv "route" "full"
                list(list(0.3 0.5) list(0.3 -0.5)) 0.0625 nil nil)

            ; NMOS source to GND
            dbCreateWire(cv "route" "full"
                list(list(0.0 -0.8) list(0.0 -1.2)) 0.0625 nil nil)

            ; Input to both gates
            dbCreateWire(cv "route" "full"
                list(list(-1.0 0.0) list(-0.3 0.0) list(-0.3 0.5)) 0.0625 nil nil)
            dbCreateWire(cv "route" "full"
                list(list(-0.3 0.0) list(-0.3 -0.5)) 0.0625 nil nil)

            ; Output wire
            dbCreateWire(cv "route" "full"
                list(list(0.3 0.0) list(1.0 0.0)) 0.0625 nil nil)

            ; Save and close
            dbSave(cv)
            dbClose(cv)

            printf("SUCCESS: Inverter created at %s/%s/%s\n" lib cell view)
            t
        else
            printf("ERROR: Could not create cellview\n")
            nil
        )
    )
)

; Execute
createInverter()
