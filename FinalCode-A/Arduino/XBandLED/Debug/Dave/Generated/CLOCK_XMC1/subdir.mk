################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Dave/Generated/CLOCK_XMC1/clock_xmc1.c \
../Dave/Generated/CLOCK_XMC1/clock_xmc1_conf.c 

OBJS += \
./Dave/Generated/CLOCK_XMC1/clock_xmc1.o \
./Dave/Generated/CLOCK_XMC1/clock_xmc1_conf.o 

C_DEPS += \
./Dave/Generated/CLOCK_XMC1/clock_xmc1.d \
./Dave/Generated/CLOCK_XMC1/clock_xmc1_conf.d 


# Each subdirectory must supply rules for building sources it contributes
Dave/Generated/CLOCK_XMC1/%.o: ../Dave/Generated/CLOCK_XMC1/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: ARM-GCC C Compiler'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-gcc" -MMD -MT "$@" -DXMC1100_T038x0064 -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries\XMCLib\inc" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11/Libraries/CMSIS/Include" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11/Libraries/CMSIS/Infineon/XMC1100_series/Include" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Dave\Generated" -I"C:\Workspaces\DAVE-4.2.2\RGB_LED_Shield_Ws\RGBLED_2_Safe_XMC11\Libraries" -O0 -ffunction-sections -fdata-sections -Wall -std=gnu99 -Wa,-adhlns="$@.lst" -pipe -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d) $@" -mcpu=cortex-m0 -mthumb -g -gdwarf-2 -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo.

