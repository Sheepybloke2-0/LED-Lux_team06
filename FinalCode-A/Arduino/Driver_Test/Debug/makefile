################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Startup/subdir.mk
-include Libraries/XMCLib/src/subdir.mk
-include Libraries/Newlib/subdir.mk
-include Dave/Generated/SYSTIMER/subdir.mk
-include Dave/Generated/DIGITAL_IO/subdir.mk
-include Dave/Generated/CPU_CTRL_XMC1/subdir.mk
-include Dave/Generated/CLOCK_XMC1/subdir.mk
-include Dave/Generated/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
SECONDARY_FLASH += \
RGBLED_2_Safe_XMC11.hex \

SECONDARY_LIST += \
RGBLED_2_Safe_XMC11.lst \

SECONDARY_SIZE += \
RGBLED_2_Safe_XMC11.siz \


LIST_FILES = $(addsuffix .o.lst, $(basename $(OBJS))) 
MAP_FILE = RGBLED_2_Safe_XMC11.map

# All Target
all: RGBLED_2_Safe_XMC11.elf secondary-outputs

# Tool invocations
RGBLED_2_Safe_XMC11.elf: $(OBJS) ../linker_script.ld $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: ARM-GCC C Linker'
	$(file >objects.rsp,$(OBJS))
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-gcc" -T"../linker_script.ld" -nostartfiles -Xlinker --gc-sections -specs=nano.specs -specs=nosys.specs -Wl,-Map,$(MAP_FILE) -mcpu=cortex-m0 -mthumb -g -gdwarf-2 -o "RGBLED_2_Safe_XMC11.elf" "@objects.rsp" $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo.
RGBLED_2_Safe_XMC11.hex: RGBLED_2_Safe_XMC11.elf
	@echo 'Invoking: ARM-GCC Create Flash Image'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-objcopy" -O ihex "RGBLED_2_Safe_XMC11.elf"  "RGBLED_2_Safe_XMC11.hex"
	@echo 'Finished building: $@'
	@echo.
RGBLED_2_Safe_XMC11.lst: RGBLED_2_Safe_XMC11.elf
	@echo 'Invoking: ARM-GCC Create Listing'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-objdump" -h -S "RGBLED_2_Safe_XMC11.elf" > "RGBLED_2_Safe_XMC11.lst"
	@echo 'Finished building: $@'
	@echo.
RGBLED_2_Safe_XMC11.siz: RGBLED_2_Safe_XMC11.elf
	@echo 'Invoking: ARM-GCC Print Size'
	"C:\DAVEv4\DAVE-4.2.2\eclipse\ARM-GCC-49/bin/arm-none-eabi-size"  --format=berkeley "RGBLED_2_Safe_XMC11.elf"
	@echo 'Finished building: $@'
	@echo.
# Other Targets
clean:
	-$(RM) $(OBJS)$(SECONDARY_FLASH)$(SECONDARY_LIST)$(SECONDARY_SIZE)$(ARM_GCC_FOR_XMC_LINKER_OUTPUT_TYPE_OUTPUTS)$(S_DEPS)$(S_UPPER_DEPS)$(C_DEPS) RGBLED_2_Safe_XMC11.elf $(LIST_FILES) $(MAP_FILE) objects.rsp
	-@echo.
secondary-outputs: $(SECONDARY_FLASH) $(SECONDARY_LIST) $(SECONDARY_SIZE)

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets
