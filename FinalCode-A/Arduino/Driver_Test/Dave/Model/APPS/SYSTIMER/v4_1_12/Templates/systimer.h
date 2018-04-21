/**
 * @file systimer.h
 * @date 2015-08-10
 *
 * NOTE:
 * This file is generated by DAVE. Any manual modification done to this file will be lost when the code is regenerated.
 *
 * @cond
 ***********************************************************************************************************************
 * SYSTIMER v4.1.12 - The SYSTIMER APP uses the SysTick interrupt to call user functions periodically at a specified
 *                   rate or after a given period of time expires.
 *
 * Copyright (c) 2015, Infineon Technologies AG
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,are permitted provided that the
 * following conditions are met:
 *
 *   Redistributions of source code must retain the above copyright notice, this list of conditions and the  following
 *   disclaimer.
 *
 *   Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
 *   disclaimer in the documentation and/or other materials provided with the distribution.
 *
 *   Neither the name of the copyright holders nor the names of its contributors may be used to endorse or promote
 *   products derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE  FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY,OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  OF THE
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * To improve the quality of the software, users are encouraged to share modifications, enhancements or bug fixes
 * with Infineon Technologies AG (dave@infineon.com).
 ***********************************************************************************************************************
 *
 * Change History
 * --------------
 *
 * 2015-02-16:
 *     - Initial version.<br>
 *
 * 2015-05-19:
 *     - Structure name changed from SYSTIMER_TimerObject to SYSTIMER_OBJECT_t and SYSTIMER_INIT_t to SYSTIMER_t. And
 *       also changed its parameter name.<br>
 *     - Enum name changed from SYSTIMER_TimerStateType, SYSTIMER_TimerType to SYSTIMER_STATE_t and SYSTIMER_MODE_t.
 *       And also changed its parameter name.<br>
 *     - Supported new APIs SYSTIMER_GetTimerState() and  SYSTIMER_GetTickCount().<br>
 *
 * 2015-06-20:
 *     - Version check added for XMCLib dependency.<br>
 *
 * 2015-06-26:
 *     - SYSTIMER_OBJECT_t structure variable delete renamed to delete_swtmr.<br>
 *     - SYSTIMER_OBJECT_t structure scope changed from global to local scope.<br>
 *
 * 2015-08-25:
 *     - Fixed GUI tool tip issues. Updated SYSTIMER.h file for help documentation range mistakes.<br>
 *     - Support for XMC1400 / XMC4700 / XMC4800 added.
 *     - Removed CPU_CTRL_XMC1 / CPU_CTRL_XMC4 APP header file inclusions.
 * @endcond
 *
 */
/***********************************************************************************************************************
 * HEADER FILES
 **********************************************************************************************************************/

#ifndef SYSTIMER_H
#define SYSTIMER_H

#include "xmc_common.h"
#include <DAVE_Common.h>
#include "systimer_conf.h"

/**********************************************************************************************************************
 * MACROS
 **********************************************************************************************************************/

#if (!((XMC_LIB_MAJOR_VERSION == 2U) && \
       (XMC_LIB_MINOR_VERSION >= 0U) && \
       (XMC_LIB_PATCH_VERSION >= 0U)))
#error "SYSTIMER requires XMC Peripheral Library v2.0.0 or higher"
#endif

/**********************************************************************************************************************
 * ENUMS
 **********************************************************************************************************************/

/**
 * @ingroup SYSTIMER_enumerations
 * @{
 */

/**
 * @brief This enumeration indicates status of SYSTIMER
 */
typedef enum SYSTIMER_STATUS
{
  SYSTIMER_STATUS_SUCCESS = 0U, /**< Status Success if initialization is successful */
  SYSTIMER_STATUS_FAILURE  /**< Status Failure if initialization is failed */
} SYSTIMER_STATUS_t;

/**
 * @brief This enumeration defines possible timer state
 */
typedef enum SYSTIMER_STATE
{
  SYSTIMER_STATE_NOT_INITIALIZED = 0U, /**< The timer is in uninitialized state */
  SYSTIMER_STATE_RUNNING, /**< The timer is in running state */
  SYSTIMER_STATE_STOPPED /**< The timer is in stop state */
} SYSTIMER_STATE_t;

/**
 * @brief Enumeration values which describes timer types
 */
typedef enum SYSTIMER_MODE
{
  SYSTIMER_MODE_ONE_SHOT = 0U, /**< timer type is one shot */
  SYSTIMER_MODE_PERIODIC /**< timer type is periodic */
} SYSTIMER_MODE_t;

/**
 * @}
 */

/**********************************************************************************************************************
* DATA STRUCTURES
**********************************************************************************************************************/
/**
  * @ingroup SYSTIMER_datastructures
  * @{
  */

/**
 * @brief timer callback function pointer
 */
typedef void (*SYSTIMER_CALLBACK_t)(void *args);

/**
 * @brief This structure contains pointer which is used to hold CPU instance handle and
 * variables for priority group
 */
typedef struct SYSTIMER
{
  bool init_status; /**< APP initialization status to ensure whether SYSTIMER_Init called or not */
} SYSTIMER_t;
/**
 * @}
 */

/***********************************************************************************************************************
 * API Prototypes
 **********************************************************************************************************************/

/* Support for C++ codebase */
#ifdef __cplusplus
extern "C" {
#endif

/**
 * @ingroup SYSTIMER_apidoc
 * @{
 */

/**
 * @brief Get SYSTIMER APP version
 * @return DAVE_APP_VERSION_t APP version information (major, minor and patch number).
 *
 * \par<b>Description: </b><br>
 * The function can be used to check application software compatibility with a
 * specific version of the APP.
 *
 * @code
 * #include <DAVE.h>
 *
 * int main(void)
 * {
 *  DAVE_Init();
 *  DAVE_APP_VERSION_t systimer_version;
 *  systimer_version = SYSTIMER_GetAppVersion();
 *  if ((systimer_version.major == 4U) && (systimer_version.minor == 1U))
 *  {
 *    // Add application code here
 *    while (1)
 *   {
 *   }
 *  }
 *   return(1);
 * }
 * @endcode
 */
DAVE_APP_VERSION_t SYSTIMER_GetAppVersion(void);

/**
 * @brief Initializes SYSTIMER APP
 * @param handle Pointer pointing to SYSTIMER APP data structure. Refer @ref SYSTIMER_t for details.
 * @return SYSTIMER_STATUS_t APP status. Refer @ref SYSTIMER_STATUS_t for details.
 *
 * \par<b>Description: </b><br>
 * Initializes the SysTick counter as per the SysTick interval specified by the
 * user and start the SysTick counter. It also initializes global variables.
 *
 * \par<b>Example Usage:</b><br>
 * @code
 *   #include <DAVE.h>         //Declarations from DAVE Code Generation (includes SFR declaration)
 *
 *   int main(void)
 *   {
 *     SYSTIMER_STATUS_t init_status;
 *
 *     init_status = (SYSTIMER_STATUS_t)SYSTIMER_Init(&SYSTIMER_0); // Initialization of SYSTIMER APP
 *     if (init_status == SYSTIMER_STATUS_SUCCESS)
 *     {
 *       // Add application code here
 *       while(1)
 *       {
 *       }
 *     }
 *     else
 *     {
 *      XMC_DEBUG("main: Application initialization failed");
 *      while(1)
 *      {
 *      }
 *     }
 *      return (1);
 *  }
 *  @endcode
 */
 SYSTIMER_STATUS_t SYSTIMER_Init(SYSTIMER_t *handle);

/**
 * @brief Creates a new software timer.
 * @param period  timer period value in microseconds. Range: (SYSTIMER_TICK_PERIOD_US) to pow(2,32).
 * @param mode  Mode of timer(ONE_SHOT/PERIODIC). Refer @ref SYSTIMER_MODE_t for details.
 * @param callback  Call back function of the timer(No Macros are allowed).
 * @param args  Call back function parameter.
 *
 * @return uint32_t returns timer ID if timer created successfully otherwise returns 0 if timer creation failed.
 *                  Range: 0 to 16, 0: Invalid timer ID, 1-16: Valid timer ID.
 *
 * \par<b>Description: </b><br>
 * API for creating a new software timer instance. This also add created software timer to timer list.<br>
 * <b>Note :</b><br> 1. This APP uses SysTick exception for controlling the timer list.
 *  Call back function registered through this function will be called in 
 *  SysTick exception when the software timer is expired i.e the software timers callback is executed in
 *  the interrupt context.<br>
 *  2. Due to time at which software timer creation asked by user will not be in synchronize with Hardware SysTick
 *  timer, the count value used during creation of software timer will not create starting/initial period same as
 *  expected value. It is decided to add one extra count(HW_TIMER_ADDITIONAL_CNT) with Software timer. Impact of this
 *  additional count(HW_TIMER_ADDITIONAL_CNT) is, first SW timer period(Initial one) is always equal to or more than
 *  expected/configured.<br>
 *  3. Callbacks are executed in round robin manner if more than one software timers are created with same period
 *  value. Last created software is having higher priority and its associated callback is executed first.<br>
 *  4. Avoid any call to wait, infinitive while loop, blocking calls or creating software timer in ISR because their
 *  behavior could be corrupted when called from an ISR.<br>
 *  5. Software timers are based on 24-bit Hardware SysTick counters, so maximum counts can achieve is
 *  pow(2,24) *(1/fCPU) * 1E6,  where fCPU is in hertz. Software timers are designed for times between microseconds and
 *  seconds. For longer times, application code need to ensure to take necessary action.<br>
 *  6. Software timer period value must be equal to SysTick Interval or integer multiple of a number with SysTick
 *  interval (i.e. SysTick Interval  * n, where n is integer number, n can be 1,2,3,4... but n should not be fractional
 *  or float number). And also software timer period value should not be 0 or less than Hardware SysTick Interval.
 *
 *
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //software timer is created successfully
 *      //Add user code here
 *    }
 *    else
 *    {
 *      // //software timer creation is failed
 *    }
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
uint32_t SYSTIMER_CreateTimer
(
  uint32_t period,
  SYSTIMER_MODE_t mode,
  SYSTIMER_CALLBACK_t callback,
  void  *args
);

/**
 * @brief Starts the software timer.
 * @param id  timer ID obtained from SYSTIMER_CreateTimer. Range : 1 to 16
 * @return SYSTIMER_STATUS_t APP status. Refer @ref SYSTIMER_STATUS_t for details.
 *
 * \par<b>Description: </b><br>
 * API for starting a software timer instance.<br>
 *<b>Note :</b> This API must be called after software timer is created using SYSTIMER_CreateTimer API with generated
 * ID and enable XMC_ASSERT for better understanding of API behavioral in run time.<br>
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    SYSTIMER_STATUS_t status;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully, now start/run software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      if (status == SYSTIMER_STATUS_SUCCESS)
 *      {
 *        // Software timer is running
 *        // Add user code here
 *      }
 *      else
 *      {
 *        // Error during software timer start operation
 *      }
 *    }
 *    else
 *    {
 *      // timer ID Can not be zero
 *    }
 *    // ... infinite loop ...
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
SYSTIMER_STATUS_t SYSTIMER_StartTimer(uint32_t id);

/**
 * @brief Stops the software timer.
 * @param id  timer ID obtained from SYSTIMER_CreateTimer. Range : 1 to 16
 * @return SYSTIMER_STATUS_t APP status. Refer @ref SYSTIMER_STATUS_t for details.
 *
 * \par<b>Description: </b><br>
 * API to stop created software timer instance.<br>
 *<b>Note :</b> This API must be called after software timer is created using SYSTIMER_CreateTimer API with generated
 * ID and enable XMC_ASSERT for better understanding of API behavioral in run time.<br>
 *
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    SYSTIMER_STATUS_t status;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully, now start/run software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      if (status == SYSTIMER_STATUS_SUCCESS)
 *      {
 *        // Software timer is running
 *        // Add user code here
 *
 *
 *
 *        //stop the timer
 *        status = SYSTIMER_StopTimer(TimerId);
 *        if (status == SYSTIMER_STATUS_SUCCESS)
 *        {
 *          //Software timer has stopped
 *        }
 *        else
 *        {
 *           // Error during software timer stop operation
 *        }
 *      }
 *      else
 *      {
 *        // Error during software timer start operation
 *      }
 *    }
 *    else
 *    {
 *      // timer ID Can not be zero
 *    }
 *    // ... infinite loop ...
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
SYSTIMER_STATUS_t SYSTIMER_StopTimer(uint32_t id);

/**
 * @brief Function to modify the time interval and restart the timer for the new time interval.<br>
 * @param id ID of already created system timer. Range : 1 to 16
 * @param microsec new time interval. Range: (SYSTIMER_TICK_PERIOD_US) to pow(2,32).
 * @return SYSTIMER_STATUS_t APP status. Refer @ref SYSTIMER_STATUS_t for details.
 *
 * \par<b>Description: </b><br>
 * API for restarting the created software timer instance with new time interval.<br>
 *<b>Note :</b> This API must be called after software timer is created using SYSTIMER_CreateTimer API with generated
 * ID and enable XMC_ASSERT for better understanding of API behavioral in run time.<br>
 *
 * \par<b>Example Usage:</b><br>
 * Demonstrate SYSTIMER_RestartTimer API
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  #define NEW_INTERVAL (ONESEC * 10U)
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    SYSTIMER_STATUS_t status;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully
 *      // Start/Run Software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      if (status == SYSTIMER_STATUS_SUCCESS)
 *      {
 *
 *        // User code
 *
 *
 *        status = SYSTIMER_StopTimer(TimerId);
 *        //User code
 *
 *        if (status == SYSTIMER_STATUS_SUCCESS)
 *        {
 *          //User code
 *
 *
 *          status = SYSTIMER_RestartTimer(TimerId,NEW_INTERVAL);
 *          if (status == SYSTIMER_STATUS_SUCCESS)
 *          {
 *            // timer configured with the new time interval and is running
 *          }
 *          else
 *          {
 *            // Error during software timer restart operation
 *          }
 *        }
 *        else
 *        {
 *           // Error during software timer stop operation
 *        }
 *      }
 *      else
 *      {
 *        // Error during software timer start operation
 *      }
 *    }
 *    else
 *    {
 *      // timer ID can not be zero
 *    }
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
SYSTIMER_STATUS_t SYSTIMER_RestartTimer(uint32_t id, uint32_t microsec);

/**
 * @brief Deletes the software timer from the timer list.
 * @param id  timer ID obtained from SYSTIMER_CreateTimer. Range : 1 to 16
 * @return SYSTIMER_STATUS_t APP status. Refer @ref SYSTIMER_STATUS_t for details.
 *
 * \par<b>Description: </b><br>
 * API for deleting the created software timer instance from timer list.<br>
 *<b>Note :</b> This API must be called after software timer is created using SYSTIMER_CreateTimer API with generated
 * ID and enable XMC_ASSERT for better understanding of API behavioral in run time.<br>
 *
 *
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    SYSTIMER_STATUS_t status;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully, now start/run software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      if (status == SYSTIMER_STATUS_SUCCESS)
 *      {
 *
 *      // User code
 *
 *
 *      status = SYSTIMER_StopTimer(TimerId);
 *      //User code
 *
 *        if (status == SYSTIMER_STATUS_SUCCESS)
 *        {
 *          //User code
 *
 *
 *          status = SYSTIMER_DeleteTimer(TimerId);
 *          if (status == SYSTIMER_STATUS_SUCCESS)
 *          {
 *            // Software timer has deleted
 *          }
 *          else
 *          {
 *            // Error during software timer delete operation
 *          }
 *        }
 *        else
 *        {
 *           // Error during software timer stop operation
 *        }
 *      }
 *      else
 *      {
 *        // Error during software timer start operation
 *      }
 *    }
 *    else
 *    {
 *      // timer ID Can not be zero
 *    }
 *    // ... infinite loop ...
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
SYSTIMER_STATUS_t SYSTIMER_DeleteTimer(uint32_t id);

/**
 * @brief Gives the current hardware SysTick time in microsecond since start of hardware SysTick timer.
 * @return  uint32_t  returns current SysTick time in microsecond. Range: (SYSTIMER_TICK_PERIOD_US) to pow(2,32).
 *
 * \par<b>Description: </b><br>
 * API to get current hardware SysTick time in microsecond since start of hardware SysTick timer.
 *
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    uint32_t SysTick_Time;
 *    SYSTIMER_STATUS_t status;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully, now start/run software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      if (status == SYSTIMER_STATUS_SUCCESS)
 *      {
 *        // Add user code here
 *
 *
 *         SysTick_Time = SYSTIMER_GetTime();
 *         // Add user code here
 *
 *      }
 *      else
 *      {
 *      // Error during software timer start operation
 *      }
 *    }
 *    else
 *    {
 *      // timer ID Can not be zero
 *    }
 *    // ... infinite loop ...
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
uint32_t SYSTIMER_GetTime(void);

/**
 * @brief Gives the SysTick count.
 * @return  uint32_t  returns SysTick count. Range: 0 to pow(2,32).
 *
 * \par<b>Description: </b><br>
 * API to get hardware SysTick counts since start of hardware SysTick timer.
 *
 *
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    uint32_t SysTick_Count;
 *    SYSTIMER_STATUS_t status;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully, now start/run software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      if (status == SYSTIMER_STATUS_SUCCESS)
 *      {
 *        // Add user code here
 *
 *
 *         SysTick_Count = SYSTIMER_GetTickCount();
 *         // Add user code here
 *
 *      }
 *      else
 *      {
 *      // Error during software timer start operation
 *      }
 *    }
 *    else
 *    {
 *      // timer ID Can not be zero
 *    }
 *    // ... infinite loop ...
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
uint32_t SYSTIMER_GetTickCount(void);

/**
 * @brief Gives the current state of software timer.
 * @param id  timer ID obtained from SYSTIMER_CreateTimer. Range : 1 to 16
 * @return SYSTIMER_STATE_t Software timer state. Refer @ref SYSTIMER_STATE_t for details.
 *
 * \par<b>Description: </b><br>
 * API to get current software timer state.
 *
 * \par<b>Example Usage:</b><br>
 *
 * @code
 *  #include <DAVE.h>
 *  #define ONESEC 1000000U
 *  #define NEW_INTERVAL (ONESEC * 10U)
 *  void LED_Toggle_EverySec(void)
 *  {
 *    // Add user code here
 *  }
 *
 *  int main(void)
 *  {
 *    uint32_t TimerId;
 *    SYSTIMER_STATUS_t status;
 *    SYSTIMER_STATE_t timer_state;
 *    // ... Initializes APPs configuration ...
 *    DAVE_Init(); // SYSTIMER APP Initialized during DAVE Initialization
 *    // Create Software timer
 *    TimerId = (uint32_t)SYSTIMER_CreateTimer(ONESEC,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *    if (TimerId != 0U)
 *    {
 *      //timer is created successfully, now start/run software timer
 *      status = SYSTIMER_StartTimer(TimerId);
 *      timer_state = SYSTIMER_GetTimerState(TimerId);  // use case scenario 1
 *      if (timer_state == SYSTIMER_STATE_RUNNING)
 *      {
 *        // software timer start operation is successful
 *        // Add user code here
 *      }
 *      else
 *      {
 *        // Error during software timer start operation
 *      }
 *
 *      // Add user code here
 *
 *      // user decided to change software interval, oops but user don't know the timer state
 *
 *      timer_state = SYSTIMER_GetTimerState(TimerId);   // use case scenario 2
 *      if (timer_state == SYSTIMER_STATE_RUNNING)
 *      {
 *        status = SYSTIMER_StopTimer(TimerId);
 *        status = SYSTIMER_RestartTimer(TimerId,NEW_INTERVAL);
 *        // Add user code here
 *      }
 *      else if (timer_state == SYSTIMER_STATE_STOPPED)
 *      {
 *        status = SYSTIMER_RestartTimer(TimerId,NEW_INTERVAL);
 *      }
 *      else if (timer_state == SYSTIMER_STATE_NOT_INITIALIZED)
 *      {
 *       // user has already deleted this software timer but need to recreate
 *       TimerId = (uint32_t)SYSTIMER_CreateTimer(NEW_INTERVAL,SYSTIMER_MODE_PERIODIC,(void*)LED_Toggle_EverySec,NULL);
 *       status = SYSTIMER_StartTimer(TimerId);
 *       // Add user code here
 *
 *      }
 *    }
 *    else
 *    {
 *      // timer ID Can not be zero
 *    }
 *    // ... infinite loop ...
 *    while (1)
 *    {
 *
 *    }
 *    return (1);
 *  }
 * @endcode<BR> </p>
 */
SYSTIMER_STATE_t SYSTIMER_GetTimerState(uint32_t id);

/**
 *@}
 */

/* Support for C++ codebase */
#ifdef __cplusplus
}
#endif

/* Inclusion of APP extern file */
#include "systimer_extern.h"

#endif /* SYSTIMER_H */
