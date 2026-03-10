gantt
    dateFormat  DD.MM.YY
    axisFormat  %d.%m
    title       CNC Modernization Gannt Chart
    todayMarker on

    Project Topic Assignments :    milestone,f1,03.03.26,1d

    Literature Survey         : 03.03.26, 3w
    Previous Work Survey      : lit_sur, 03.03.26, 3w

    section Physical Inspection
    Cleaning                  : ins1,24.03.26,2w
    Component Evaluation      : ins2,24.03.26,3w

    section Conceptual Design
    Functional Decomposition  : cd1,14.04.26, 1w
    Concept Generation        : cd2,14.04.26, 1w
    Concept Evaluation        : cd3,after cd2,1w

    section Detailed Design
    Detailed Design                   : dd2, after cd3, 2w

    section Manufacturing and Testing
    Shopping                  : shop, after dd2,2w
    Mechanics Assembly        : mech, after dd2,5w
    Electronics & Motor Drivers: elec, after dd2,4w
    Software Development      : soft,19.05.26,4w
    Control Loop Tuning       : loop, 09.06.26, 2w
    Testing & Axis Calibration: test, after mech,1w
    Demo Preparation : test, after mech, 2w
    Final Presentation        : crit,milestone,final,01.07.26,1d