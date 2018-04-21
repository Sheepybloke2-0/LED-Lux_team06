<?xml version="1.0" encoding="ASCII"?>
<ResourceModel:App xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ResourceModel="http://www.infineon.com/Davex/Resource.ecore" name="SYSTIMER" URI="http://resources/4.1.12/app/SYSTIMER/0" description="The SYSTIMER APP uses the SysTick interrupt to call user&#xA;functions periodically at a specified rate or &#xA;after a given time period expires." version="4.1.12" minDaveVersion="4.0.0" instanceLabel="SYSTIMER_0" appLabel="">
  <properties singleton="true" provideInit="true" sharable="true"/>
  <requiredApps URI="http://resources/4.1.12/app/SYSTIMER/0/appres_clock" requiredAppName="CLOCK_XMC1" requiringMode="SHARABLE">
    <downwardMapList xsi:type="ResourceModel:App" href="../../CLOCK_XMC1/v4_0_14/CLOCK_XMC1_0.app#/"/>
  </requiredApps>
  <requiredApps URI="http://resources/4.1.12/app/SYSTIMER/0/appres_cpu" requiredAppName="CPU_CTRL_XMC1" requiringMode="SHARABLE">
    <downwardMapList xsi:type="ResourceModel:App" href="../../CPU_CTRL_XMC1/v4_0_6/CPU_CTRL_XMC1_0.app#/"/>
  </requiredApps>
  <hwResources name="syst" URI="http://resources/4.1.12/app/SYSTIMER/0/hwres_syst" resourceGroupUri="peripheral/cpu/0/systick" mResGrpUri="peripheral/cpu/0/systick">
    <downwardMapList xsi:type="ResourceModel:ResourceGroup" href="../../../HW_RESOURCES/CPU/CPU_0.dd#//@provided.1"/>
  </hwResources>
</ResourceModel:App>
