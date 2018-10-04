EESchema Schematic File Version 4
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:CP1 C
U 1 1 5BB507D3
P 4900 3150
F 0 "C" H 5015 3196 50  0000 L CNN
F 1 "CP1" H 5015 3105 50  0000 L CNN
F 2 "" H 4900 3150 50  0001 C CNN
F 3 "~" H 4900 3150 50  0001 C CNN
	1    4900 3150
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R?
U 1 1 5BB50DD8
P 4350 2750
F 0 "R?" V 4555 2750 50  0000 C CNN
F 1 "R_US" V 4464 2750 50  0000 C CNN
F 2 "" V 4390 2740 50  0001 C CNN
F 3 "~" H 4350 2750 50  0001 C CNN
	1    4350 2750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5250 2750 4900 2750
Wire Wire Line
	3400 2750 4200 2750
Wire Wire Line
	4900 3000 4900 2750
Connection ~ 4900 2750
Wire Wire Line
	4900 2750 4500 2750
Text GLabel 3400 2750 0    50   Input ~ 0
+
Text GLabel 5250 2750 0    50   Input ~ 0
+
Wire Wire Line
	3400 3450 4900 3450
Wire Wire Line
	4900 3300 4900 3450
Connection ~ 4900 3450
Wire Wire Line
	4900 3450 5250 3450
Text GLabel 5250 3450 0    50   Input ~ 0
-
Text GLabel 3400 3450 0    50   Input ~ 0
-
$EndSCHEMATC
