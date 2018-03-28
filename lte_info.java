private class SignalStrengthListener extends PhoneStateListener
{
public void onSignalStrengthsChanged(SignalStrength signalStrength)
{
super.onSignalStrengthsChanged(signalStrength);

try {
lte_sinr = (Integer) signalStrength.getClass().getMethod("getLteSignalStrength").invoke(signalStrength);
lte_rsrp = (Integer) signalStrength.getClass().getMethod("getLteRsrp").invoke(signalStrength);
lte_rsrq = (Integer) signalStrength.getClass().getMethod("getLteRsrq").invoke(signalStrength);
lte_rssnr = (Integer) signalStrength.getClass().getMethod("getLteRssnr").invoke(signalStrength);
lte_cqi = (Integer) signalStrength.getClass().getMethod("getLteCqi").invoke(signalStrength);
} catch (Exception e) {
e.printStackTrace();
return;
}
}
