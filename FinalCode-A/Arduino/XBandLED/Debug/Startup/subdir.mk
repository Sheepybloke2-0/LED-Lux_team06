################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Startup/system_XMC1100.c 

S_UPPER_SRCS += \
../Startup/startup_XMC1100.S 

OBJS += \
./Startup/startup_XMC1100.o \
./Startup/system_XMC1100.o 

S_UPPER_DEPS += \
./Startup/startup_XMC1100.d 

C_DEPS += \
./Startup/system_XMC1100.d 


# Each subdirectory must supply rules for building sources it contributes
Startup/%.o: ../Startup/%.S
	@echo 'Building file: $<'
	@echo 'Invoking: ARM-GCC Assembler'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-gcc" -MMD -MT "$@" -x assembler-with-cpp -DXMC1100_T038x0064 -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries\XMCLib\inc" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Dave\Generated" -Wall -Wa,-adhlns="$@.lst" -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d) $@" -mcpu=cortex-m0 -mthumb -g -gdwarf-2 -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo.
Startup/%.o: ../Startup/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: ARM-GCC C Compiler'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-gcc" -MMD -MT "$@" -DXMC1100_T038x0064 -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries\XMCLib\inc" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11/Libraries/CMSIS/Include" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11/Libraries/CMSIS/Infineon/XMC1100_series/Include" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Dave\Generated" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries" -O0 -ffunction-sections -fdata-sections -Wall -std=gnu99 -Wa,-adhlns="$@.lst" -pipe -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d) $@" -mcpu=cortex-m0 -mthumb -g -gdwarf-2 -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo.

