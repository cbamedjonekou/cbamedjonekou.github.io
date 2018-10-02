# Library Imports
import math as m

# Functions:
def relativePowerGain(P_O= 0, P_I= 0, switch= 0, Ap_dB= 0):
    """Calculates the relative power gain as a ratio.
    Takes in three arguments: P_O= Output Power, P_I= Input Power.
    """
    if switch == 0:
        return P_O/P_I
    else:
        return m.pow(10, Ap_dB/10)


def relativeVoltageGain(V_O= 0, V_I= 0,  switch= 0, Av_dB= 0):
    """Calculates the relative voltage gain as a ratio.
    Takes in two arguments: V_O= Output Voltage, V_I= Input Voltage.
    """
    if switch == 0:
        return V_O/V_I
    else:
        return m.pow(10, Av_dB/20)


def relativeVoltDecibel(A_V):
    """Calculates the relative voltage gain in decibels.
    Takes in one argument: A_V= Relative Voltage Gain as a ratio.
    (hint: use relativeVoltageGain())"""
    return 20*m.log(A_V, 10)


def relativePowerDecibel(A_P):
    """Cagelculates the relative power gain in decibels.
    Takes in one argument: A_P= Relative Power Gain as a ratio.
    (hint: use relativePowerGain())"""
    return 10*m.log(A_P, 10)


def absolutePowerGain_dBm(P):
    """Calculates the absolute power gain in decibels.
    Takes in one argument: ration_Standard=  a ratio of power and some standardized reference.
    "Decibels referenced to 10^-3 W (1 mW)"
    """
    reference = m.pow(10, -3)
    ratio_Standard = P/reference
    return 10*m.log(ratio_Standard, 10)


def absolutePowerGain_dBw(P):
    """Calculates the absolute power gain in decibels.
    Takes in one argument: ration_Standard=  a ratio of power and some standardized reference.
    "Decibels referenced to 1 W"
    """
    reference = m.pow(10, 0)
    ratio_Standard = P/reference
    return 10*m.log(ratio_Standard, 10)


def inputPower_rPG(Ap_dB, P_O):
    """This formula finds the input power of the relative power gain.
    It takes two arguments: The r.p.g in decibels and the given output power."""
    return P_O/m.pow(10, Ap_dB/10)


def outputPower_rPG(Ap_dB, P_I):
    """This formula finds the output power of the relative power gain.
    It takes two arguments: The r.p.g in decibels and the given output power."""
    return P_I*m.pow(10, Ap_dB/10)


def inputVoltage_rPG(Av_dB, V_O):
    """This formula finds the input power of the relative voltage gain.
    It takes two arguments: The r.p.g in decibels and the given output voltage."""
    return V_O/m.pow(10, Av_dB/20)


def outputVoltage_rPG(Av_dB, V_I):
    """This formula finds the output power of the relative voltage gain.
    It takes two arguments: The r.p.g in decibels and the given output voltage."""
    return V_I*m.pow(10, Av_dB/20)


def db_dropped(Av_db, init_Vi, final_Vi):
    """Calculates the difference between initial and final voltage gain.
    Needs three parameters."""
    Vo_init = outputVoltage_rPG(Av_db, init_Vi)
    Vo_final = outputVoltage_rPG(Av_db, final_Vi)
    Av_db_new = relativeVoltDecibel(A_V= Vo_final/ init_Vi)
    db_dropped = Av_db - Av_db_new
    return db_dropped


def reverse_APG_dBm(Ap_dBm, P_standard= m.pow(10, -3)):
    """This formula finds the power of the absolute power gain w/ respect to 1 mW.
    It takes two arguments: The a.p.g in decibels and the given standard power."""
    return P_standard*m.pow(10, Ap_dBm/10)



def find_RMS_Voltage(R, Ap_dBm, P_standard= m.pow(10, -3)):
    """Find the rms voltage given the impedance.
    Takes three arguments: "R" which represents the impedance, "P_Standard"
    which represents the standard reference point (dBm = 1 mW), and Ap_dBm
    which represents the power gain in decibels."""
    return m.sqrt(P_standard*m.pow(10, Ap_dBm/10)*R)


def rms_to_Peak(rms):
    """Converts rms values to their respective peak values.
    Takes in one argument: rms, or root mean square value.
    (sqrt(2)*rms = v_peak)"""
    return m.sqrt(2)*rms


def peak_to_PeakPeak(v_peak):
    """Calculates to peak-to-peak value of a unit measurement.
    Multplies the voltage peak by 2. Takes in one argument: v_peak"""
    return v_peak * 2


def signalNoiseRatio(signal_voltage, noise_voltage):
    """Calculates the signal noise ratio. Takes in two parameters: signal_power,
    and noise_power"""
    return 20*m.log(signal_voltage/noise_voltage, 10)


def snr_Decibels(signalVoltage= 1, noiseVoltage= 1, signalPower= 0, noisePower= 0, sn_Ratio= 0, snp_Ratio= 0):
    """This function calculates the signal noise ratio in decibels. It takes in a total of 6 possible arguments.
    They are: signalVoltage= 1, noiseVoltage=1 , signalPower= 0, noisePower= 0, sn_Ratio= 0, snp_Ratio= 0.
    The variables assigned to '0' are by default 'switched off'. If any of these arguments are assigned
    a value, then they become 'switched on' and access the segment of code associated with their activation.
    The variables assigned to '1' are by default 'switched on'."""
    if sn_Ratio != 0:
        # Calculates snr in Decibels using the already obtained signal/noise ratio (power ratio/1 value input)
        if snp_Ratio != 0:
            return 10*m.log(snp_Ratio, 10)
        # Calculates snr in Decibels using the already obtained signal/noise ratio (voltage ratio/1 value input)
        else:
            return 20*m.log(sn_Ratio, 10)
    else:
        # Calculates snr in Decibels using the given signal/noise power (2 value input)
        if signalPower != 0 or noisePower != 0:
            snp_Ratio = signalPower/noisePower
            return 10*m.log(snp_Ratio, 10)
        # Calculates snr in Decibels using the given signal/noise voltage (2 value input)
        else:
            sn_Ratio = signalVoltage/noiseVoltage
            return 20*m.log(sn_Ratio, 10)


def snr(signalPower= 1, noisePower= 1, signalVoltage= 0, noiseVoltage=0):
    """This function calculates the signal noise ratio. It takes in a total of 4 possible arguments.
    They are: signalPower, noisePower, signalVoltage= 0, noiseVoltage=0. The variables assigned to '0'
    are by default 'switched off'. If any of these arguments are assigned a value, then they become
    'switched on' and access the segment of code associated with their activation."""
    if signalVoltage != 0 or noiseVoltage != 0:
        snr_Bels = snr_Decibels(signalVoltage, noiseVoltage)
        return m.pow(10, snr_Bels/10)
    else:
        return signalPower/noisePower


def outputSNR(noiseFactor, inputSNR):
    """This function calculates the output signal to noise ratio.
    It takes in 2 arguments. They are: noiseFactor, inputSNR."""
    #Calculates the noise ratio which is not in decibels
    noiseRatio = m.pow(10, noiseFactor/10)

    # converts the input s/n ratio to a ratio not in decibels
    snR = relativePowerGain(switch= 1, Ap_dB=inputSNR)

    # Returns the ratio form of the output ratio (not in decibels)
    return snR/noiseRatio

