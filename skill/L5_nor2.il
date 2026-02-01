; L5_nor2.il - 2-input CMOS NOR Gate
; Level 5: Basic CMOS building block
; Usage: Load in Virtuoso CIW: load("/home/v71349/analog-gradients/skill/L5_nor2.il")
;
; NOR2 topology:
;        VDD
;         |
;        PM0       (series PMOS)
;         |
;        PM1
;         |
;        OUT
;         |
;     +---+---+
;     |       |
;    NM0     NM1   (parallel NMOS)
;     |       |
;     +---+---+
;         |
;        GND
;
; A --+-- PM0 gate
;     +-- NM0 gate
; B --+-- PM1 gate
;     +-- NM1 gate
;
; Truth table: OUT = ~(A | B)

procedure(createNor2()
    let((lib cell view cv pm0 pm1 nm0 nm1 vdd gnd)

        lib = "gpu_lib"
        cell = "nor2"
        view = "schematic"

        cv = dbOpenCellViewByType(lib cell view "schematic" "w")

        if(cv then
            printf("Creating NOR2 schematic in %s/%s/%s\n" lib cell view)

            ; === PMOS (series, stacked between VDD and output) ===
            pm0 = dbCreateInst(cv "analogLib" "pmos4" "symbol" "PM0"
                list(0.0 0.9) "R0")
            pm1 = dbCreateInst(cv "analogLib" "pmos4" "symbol" "PM1"
                list(0.0 0.3) "R0")

            ; === NMOS (parallel, both connected to output and GND) ===
            nm0 = dbCreateInst(cv "analogLib" "nmos4" "symbol" "NM0"
                list(-0.4 -0.5) "R0")
            nm1 = dbCreateInst(cv "analogLib" "nmos4" "symbol" "NM1"
                list(0.4 -0.5) "R0")

            ; === SUPPLIES ===
            vdd = dbCreateInst(cv "analogLib" "vdd" "symbol" "VDD"
                list(0.0 1.5) "R0")
            gnd = dbCreateInst(cv "analogLib" "gnd" "symbol" "GND"
                list(0.0 -1.2) "R0")

            ; === NETS ===
            dbCreateNet(cv "VDD")
            dbCreateNet(cv "GND")
            dbCreateNet(cv "A")
            dbCreateNet(cv "B")
            dbCreateNet(cv "OUT")
            dbCreateNet(cv "mid") ; internal node between PM0 and PM1

            ; === PINS ===
            dbCreatePin(
                dbCreateNet(cv "A")
                dbCreateInst(cv "basic" "ipin" "symbol" nil list(-1.2 0.5) "R0")
                "A" "input"
            )
            dbCreatePin(
                dbCreateNet(cv "B")
                dbCreateInst(cv "basic" "ipin" "symbol" nil list(-1.2 -0.1) "R0")
                "B" "input"
            )
            dbCreatePin(
                dbCreateNet(cv "OUT")
                dbCreateInst(cv "basic" "opin" "symbol" nil list(1.0 0.0) "R0")
                "OUT" "output"
            )

            ; Save
            dbSave(cv)
            dbClose(cv)

            printf("SUCCESS: NOR2 created at %s/%s/%s\n" lib cell view)
            printf("NOTE: Wiring needs to be completed in Virtuoso GUI\n")
            t
        else
            printf("ERROR: Could not create cellview\n")
            nil
        )
    )
)

createNor2()
