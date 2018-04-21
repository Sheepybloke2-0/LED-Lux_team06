################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../main.c 

OBJS += \
./main.o 

C_DEPS += \
./main.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.c
	@echo 'Building file: $<'
	@echo 'Invoking: ARM-GCC C Compiler'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-gcc" -MMD -MT "$@" -DXMC1100_T038x0064 -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries\XMCLib\inc" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11/Libraries/CMSIS/Include" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11/Libraries/CMSIS/Infineon/XMC1100_series/Include" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Dave\Generated" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries" -O0 -ffunction-sections -fdata-sections -Wall -std=gnu99 -Wa,-adhlns="$@.lst" -pipe -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d) $@" -mcpu=cortex-m0 -mthumb -g -gdwarf-2 -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo.

