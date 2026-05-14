---lab
date: 2026-5-13
author: CCChiJi
category: 软件
tags: FreeRTOS
---

# FreeRTOS

官网：[FreeRTOS官网](https://freertos.org/)

## 1. FreeRTOS概述

FreeRTOS是一个迷你（mini）的**实时操作系统**内核。作为一个轻量级的操作系统，功能包括：任务管理、时间管理、信号量、消息队列、内存管理、记录功能、软件定时器、协程（线程）等，可基本满足较小系统的需要。

实时操作系统（RTOS-Real Time Operating System）中**实时（Real Time）指的是任务（Task）或者说实现一个功能的线程（Thread）必须在给定的时间(Deadline)内完成。-------抢占性的。  非实时(Linux windows)是时间片轮换。**

由于RTOS需占用一定的系统资源(尤其是RAM资源)，只有μC/OS-II、embOS、salvo、FreeRTOS等少数实时操作系统能在小RAM单片机上运行。相对μC/OS-II、embOS等商业操作系统，**FreeRTOS操作系统是完全免费的操作系统，具有源码公开、可移植、可裁减、调度策略灵活的特点，可以方便地移植到各种单片机上运行**

## 2. FreeRTOS的优势

- 开源和免费：FreeRTOS是一款开源的RTOS，采用MIT许可证发布，可以免费使用、修改和分发。
- 轻量级设计：FreeRTOS注重轻量级设计，适用于资源受限的嵌入式系统（stmf103c8t6-20kb），不占用过多内存和处理器资源。
- 广泛应用：FreeRTOS在嵌入式领域得到广泛应用，包括工业自动化、医疗设备、消费电子产品、汽车电子等。
- 多平台支持：FreeRTOS的设计注重可移植性，可以轻松地移植到不同的硬件平台，支持多种处理器架构。
- 功能丰富：提供了多任务调度、任务通信、同步等功能，适用于复杂的嵌入式应用场景。
- 具有抢占式或时间片轮换的实时操作系统内核
- 功能可裁剪，**最小占用10Kb左右的ROM空间，0.5Kb的RAM空间**
- 灵活的任务优先级分配
- 具有低功耗模式
- 有互斥锁、信号量、消息队列等任务之间通讯机制
- 运行过程可追踪
- 支持中断嵌套

## 3. FreeRTOS移植（重点 ，针对标准库）

其实freerots相当于是一个三方库，需要集成源码到我们的单片机代码中，编译一个带有**freertos源码功能**的程序烧录到板子里面去。

### 3.1 源码获取

1. 官网下载

![FreeRTOS](images\FreeRTOS.png)

当前选择的是202212.01版本

2. GitHub下载

   Github地址:[Github地址](https://github.com/FreeRTOS/FreeRTOS/releases)

![Github下载](images\Github下载.png)

### 3.2 源码结构

1. 整体结构

| **名称**                  | **描述**                                     |
| ------------------------- | -------------------------------------------- |
| FreeRTOS                  | FreeRTOS内核                                 |
| FreeRTOS-Plus             | FreeRTOS组件，一般我们会选择使用第三方的组件 |
| tools                     | 工具                                         |
| GitHub-FreeRTOS-Home      | FreeRTOS的GitHub仓库链接                     |
| Quick_Start_Guide         | 快速入门指南官方文档链接                     |
| Upgrading-to-FreeRTOS-xxx | 升级到指定FreeRTOS版本官方文档链接           |
| History.txt               | FreeRTOS历史更新记录                         |
| 其他                      | 其他                                         |

2. 文件夹结构

| **名称** | **描述**                                         |
| -------- | ------------------------------------------------ |
| Demo     | FreeRTOS演示例程，支持多种芯片架构、多种型号芯片 |
| License  | FreeRTOS相关许可                                 |
| Source   | FreeRTOS源码，最重要的文件夹                     |
| Test     | 公用以及移植层测试代码                           |

**其中要移植的文件在Source文件夹下**

3. Source文件夹结构

| **名称**        | **描述**                                         |
| --------------- | ------------------------------------------------ |
| include         | 内包含了FreeRTOS的头文件                         |
| portable        | 包含FreeRTOS移植文件：与编译器相关、keil编译环境 |
| croutine.c      | 协程(线程)相关文件                               |
| event_groups.c  | 事件相关文件                                     |
| list.c          | 列表相关文件                                     |
| queue.c         | 队列相关文件                                     |
| stream_buffer.c | 流式缓冲区相关文件                               |
| tasks.c         | 任务相关文件                                     |
| timers.c        | 软件定时器相关文件                               |

**着重注意**

**include 、portable、event_groups.c、list.c、queue.c、tasks.c、timers.c**文件为必须移植文件

portable文件夹下内容要根据编译器和内核的实际情况选取

4. portable文件夹结构

| **名称** | **描述**               |
| -------- | ---------------------- |
| Keil     | 指向RVDS文件夹         |
| RVDS     | 不同内核芯片的移植文件 |
| MemMang  | 内存管理相关文件       |

Keil文件夹里只有一个See-also-the-RVDS-directory.txt，意思是让我们看RVDS文件夹。

5. RVDS文件夹

RVDS 文件夹包含了各种处理器相关的文件夹，FreeRTOS 是一个软件，单片机是一个硬件，FreeRTOS 要想运行在一个单片机上面，它们就必须关联在一起。

关联还是得通过写代码来关联，这部分关联的文件叫接口文件，通常由汇编和 C 联合编写。这些接口文件都是跟硬件密切相关的，不同的硬件接口文件是不一样的，但都大同小异。编写这些接口文件的过程我们就叫移植，移植的过程通常由 FreeRTOS 和 mcu 原厂的人来负责，移植好的这些接口文件就放在 RVDS 这个文件夹的目录下。

FreeRTOS 为我们提供了 cortex-m0、m3、m4 和 m7 等内核的单片机的接口文件，根据mcu的内核选择对应的接口文件即可。其实准确来说，不能够叫移植，应该叫使用官方的移植， 因为这些跟硬件相关的接口文件，RTOS 官方都已经写好了，我们只是使用而已。

![RVDS文件夹](images\RVDS文件夹.png)

以 ARM_CM3 这个文件夹为例，里面只有`port.c`与`portmacro.h` 两个文件

其中`port.c`文件：

里面的内容是由 FreeRTOS 官方的技术人员为 Cortex-M3 内核的处理器写的接口文件，里面核心的上下文切换代码是由汇编语言编写而成，对技术员的要求比较高，我们只是使用的话只需拷贝过来用即可。

其中`portmacro.h`文件：

port.c文件对应的头文件，主要是一些数据类型和宏定义。

6. MemMang文件夹

MemMang 文件夹下存放的是跟内存管理相关的，总共有五个 heap 文件以及一个 readme 说明文件。

![内存管理](images\内存管理.png)

这五个 heap 文件在移植的时候必须使用一个，因为 FreeRTOS 在创建内核对象的时候使用的是动态分配内存，而这些动态内存分配的函数则在这几个文件里面实现，不同的分配算法会导致不同的效率与结果，后面在内存管理中我们会讲解每个文件的区别，由于现在是初学，所以我们选用 **heap4.c** 即可。

### 3.3 移植流程（需要自己有一个原始模板）

#### 3.3.1 目录添加源代码文件

在原始例程的根路径下，创建**FreeRTOS**文件夹，并且往里面新建**portable**和**source**文件夹

![新建文件夹](images\新建文件夹.png)

拷贝FreeRTOS源码的Source文件夹的7个.c文件到例程的source文件夹。

![拷贝源文件](images\拷贝源文件.png)

拷贝FreeRTOS源码portable文件夹下的Keil、RVDS、MemMang到例程的portable文件夹下。

![拷贝文件夹](images\拷贝文件夹.png)

**其中例程的MemMang可只保留heap_4.c**

**RVDS文件夹下要保留当前使用芯片所对应的内核（STM32F103就是CM3内核的）**

![保留CM3文件夹](images\保留CM3文件夹.png)

拷贝FreeRTOS源码include文件夹到例程的FreeRTOS文件夹下。

![拷贝头文件](images\拷贝头文件.png)

`FreeRTOSConfig.h`文件是对FreeRTOS系统进行配置的一个头文件，需要自己创建，这里**在FreeRTOS文件夹下的include文件夹中创建，内容建议直接复制以下：**

```c
#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

/* 公共头文件*/
#include "system.h"
#include "myusart.h"
#include "stm32f10x.h"
extern uint32_t SystemCoreClock;

/* 基础配置项 */
#define configUSE_PREEMPTION              1            /* 1: 抢占式调度器, 0: 协程式调度器, 无默认需定义 */
#define configUSE_PORT_OPTIMISED_TASK_SELECTION     1            /* 1: 使用硬件计算下一个要运行的任务, 0: 使用软件算法计算下一个要运行的任务, 默认: 0 */
#define configUSE_TICKLESS_IDLE             0            /* 1: 使能tickless低功耗模式, 默认: 0 */
#define configCPU_CLOCK_HZ               SystemCoreClock     /* 定义CPU主频, 单位: Hz, 无默认需定义 */
//#define configSYSTICK_CLOCK_HZ             (configCPU_CLOCK_HZ / 8)/* 定义SysTick时钟频率，当SysTick时钟频率与内核时钟频率不同时才可以定义, 单位: Hz, 默认: 不定义 */
#define configTICK_RATE_HZ               1000          /* 定义系统时钟节拍频率, 单位: Hz, 无默认需定义 */
#define configMAX_PRIORITIES              32           /* 定义最大优先级数, 最大优先级=configMAX_PRIORITIES-1, 无默认需定义 */
#define configMINIMAL_STACK_SIZE            128           /* 定义空闲任务的栈空间大小, 单位: Word, 无默认需定义 */
#define configMAX_TASK_NAME_LEN             16           /* 定义任务名最大字符数, 默认: 16 */
#define configUSE_16_BIT_TICKS             0            /* 1: 定义系统时钟节拍计数器的数据类型为16位无符号数, 无默认需定义 */
#define configIDLE_SHOULD_YIELD             1            /* 1: 使能在抢占式调度下,同优先级的任务能抢占空闲任务, 默认: 1 */
#define configUSE_TASK_NOTIFICATIONS          1            /* 1: 使能任务间直接的消息传递,包括信号量、事件标志组和消息邮箱, 默认: 1 */
#define configTASK_NOTIFICATION_ARRAY_ENTRIES      1            /* 定义任务通知数组的大小, 默认: 1 */
#define configUSE_MUTEXES                1            /* 1: 使能互斥信号量, 默认: 0 */
#define configUSE_RECURSIVE_MUTEXES           1            /* 1: 使能递归互斥信号量, 默认: 0 */
#define configUSE_COUNTING_SEMAPHORES          1            /* 1: 使能计数信号量, 默认: 0 */
#define configUSE_ALTERNATIVE_API            0            /* 已弃用!!! */
#define configQUEUE_REGISTRY_SIZE            8            /* 定义可以注册的信号量和消息队列的个数, 默认: 0 */
#define configUSE_QUEUE_SETS              1            /* 1: 使能队列集, 默认: 0 */
#define configUSE_TIME_SLICING             1            /* 1: 使能时间片调度, 默认: 1 */
#define configUSE_NEWLIB_REENTRANT           0            /* 1: 任务创建时分配Newlib的重入结构体, 默认: 0 */
#define configENABLE_BACKWARD_COMPATIBILITY       0            /* 1: 使能兼容老版本, 默认: 1 */
#define configNUM_THREAD_LOCAL_STORAGE_POINTERS     0            /* 定义线程本地存储指针的个数, 默认: 0 */
#define configSTACK_DEPTH_TYPE             uint16_t        /* 定义任务堆栈深度的数据类型, 默认: uint16_t */
#define configMESSAGE_BUFFER_LENGTH_TYPE        size_t         /* 定义消息缓冲区中消息长度的数据类型, 默认: size_t */

/* 内存分配相关定义 */
#define configSUPPORT_STATIC_ALLOCATION         0            /* 1: 支持静态申请内存, 默认: 0 */
#define configSUPPORT_DYNAMIC_ALLOCATION        1            /* 1: 支持动态申请内存, 默认: 1 */
#define configTOTAL_HEAP_SIZE              ((size_t)(10 * 1024))  /* FreeRTOS堆中可用的RAM总量, 单位: Byte, 无默认需定义 */
#define configAPPLICATION_ALLOCATED_HEAP        0            /* 1: 用户手动分配FreeRTOS内存堆(ucHeap), 默认: 0 */
#define configSTACK_ALLOCATION_FROM_SEPARATE_HEAP    0            /* 1: 用户自行实现任务创建时使用的内存申请与释放函数, 默认: 0 */

/* 钩子函数相关定义 */
#define configUSE_IDLE_HOOK               0            /* 1: 使能空闲任务钩子函数, 无默认需定义 */
#define configUSE_TICK_HOOK               0            /* 1: 使能系统时钟节拍中断钩子函数, 无默认需定义 */
#define configCHECK_FOR_STACK_OVERFLOW         0            /* 1: 使能栈溢出检测方法1, 2: 使能栈溢出检测方法2, 默认: 0 */
#define configUSE_MALLOC_FAILED_HOOK          0            /* 1: 使能动态内存申请失败钩子函数, 默认: 0 */
#define configUSE_DAEMON_TASK_STARTUP_HOOK       0            /* 1: 使能定时器服务任务首次执行前的钩子函数, 默认: 0 */

/* 运行时间和任务状态统计相关定义 */
#define configGENERATE_RUN_TIME_STATS          0            /* 1: 使能任务运行时间统计功能, 默认: 0 */
#if configGENERATE_RUN_TIME_STATS
#include "./BSP/TIMER/btim.h"
#define portCONFIGURE_TIMER_FOR_RUN_TIME_STATS()    ConfigureTimeForRunTimeStats()
extern uint32_t FreeRTOSRunTimeTicks;
#define portGET_RUN_TIME_COUNTER_VALUE()        FreeRTOSRunTimeTicks
#endif
#define configUSE_TRACE_FACILITY            1            /* 1: 使能可视化跟踪调试, 默认: 0 */
#define configUSE_STATS_FORMATTING_FUNCTIONS      1            /* 1: configUSE_TRACE_FACILITY为1时，会编译vTaskList()和vTaskGetRunTimeStats()函数, 默认: 0 */

/* 协程相关定义 */
#define configUSE_CO_ROUTINES              0            /* 1: 启用协程, 默认: 0 */
#define configMAX_CO_ROUTINE_PRIORITIES         2            /* 定义协程的最大优先级, 最大优先级=configMAX_CO_ROUTINE_PRIORITIES-1, 无默认configUSE_CO_ROUTINES为1时需定义 */

/* 软件定时器相关定义 */
#define configUSE_TIMERS                1                /* 1: 使能软件定时器, 默认: 0 */
#define configTIMER_TASK_PRIORITY            ( configMAX_PRIORITIES - 1 )  /* 定义软件定时器任务的优先级, 无默认configUSE_TIMERS为1时需定义 */
#define configTIMER_QUEUE_LENGTH            5                /* 定义软件定时器命令队列的长度, 无默认configUSE_TIMERS为1时需定义 */
#define configTIMER_TASK_STACK_DEPTH          ( configMINIMAL_STACK_SIZE * 2) /* 定义软件定时器任务的栈空间大小, 无默认configUSE_TIMERS为1时需定义 */

/* 可选函数, 1: 使能 */
#define INCLUDE_vTaskPrioritySet            1            /* 设置任务优先级 */
#define INCLUDE_uxTaskPriorityGet            1            /* 获取任务优先级 */
#define INCLUDE_vTaskDelete               1            /* 删除任务 */
#define INCLUDE_vTaskSuspend              1            /* 挂起任务 */
#define INCLUDE_xResumeFromISR             1            /* 恢复在中断中挂起的任务 */
#define INCLUDE_vTaskDelayUntil             1            /* 任务绝对延时 */
#define INCLUDE_vTaskDelay               1            /* 任务延时 */
#define INCLUDE_xTaskGetSchedulerState         1            /* 获取任务调度器状态 */
#define INCLUDE_xTaskGetCurrentTaskHandle        1            /* 获取当前任务的任务句柄 */
#define INCLUDE_uxTaskGetStackHighWaterMark       1            /* 获取任务堆栈历史剩余最小值 */
#define INCLUDE_xTaskGetIdleTaskHandle         1            /* 获取空闲任务的任务句柄 */
#define INCLUDE_eTaskGetState              1            /* 获取任务状态 */
#define INCLUDE_xEventGroupSetBitFromISR        1            /* 在中断中设置事件标志位 */
#define INCLUDE_xTimerPendFunctionCall         1            /* 将函数的执行挂到定时器服务任务 */
#define INCLUDE_xTaskAbortDelay             1            /* 中断任务延时 */
#define INCLUDE_xTaskGetHandle             1            /* 通过任务名获取任务句柄 */
#define INCLUDE_xTaskResumeFromISR           1            /* 恢复在中断中挂起的任务 */

/* 中断嵌套行为配置 */
#ifdef __NVIC_PRIO_BITS
  #define configPRIO_BITS __NVIC_PRIO_BITS
#else
  #define configPRIO_BITS 4
#endif

#define configLIBRARY_LOWEST_INTERRUPT_PRIORITY     15         /* 中断最低优先级 */
#define configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY  5          /* FreeRTOS可管理的最高中断优先级 */
#define configKERNEL_INTERRUPT_PRIORITY         ( configLIBRARY_LOWEST_INTERRUPT_PRIORITY << (8 - configPRIO_BITS) )
#define configMAX_SYSCALL_INTERRUPT_PRIORITY      ( configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY << (8 - configPRIO_BITS) )
#define configMAX_API_CALL_INTERRUPT_PRIORITY      configMAX_SYSCALL_INTERRUPT_PRIORITY

/* FreeRTOS中断服务函数相关定义 */
#define xPortPendSVHandler               PendSV_Handler
#define vPortSVCHandler                 SVC_Handler

/* 断言 */
#define vAssertCalled(char, int) printf("Error: %s, %d\r\n", char, int)
#define configASSERT( x ) if( ( x ) == 0 ) vAssertCalled( __FILE__, __LINE__ )

/* FreeRTOS MPU 特殊定义 */
//#define configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS 0
//#define configTOTAL_MPU_REGIONS                8
//#define configTEX_S_C_B_FLASH                 0x07UL
//#define configTEX_S_C_B_SRAM                  0x07UL
//#define configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY      1
//#define configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS       1

/* ARMv8-M 安全侧端口相关定义。 */
//#define secureconfigMAX_SECURE_CONTEXTS     5

#endif /* FREERTOS_CONFIG_H */

```

#### 3.3.2 工程添加源码文件

工程配置中添加如下四个新文件夹，其中`APP`文件夹是实际的业务代码文件

![工程配置1](images\工程配置1.png)

`FreeRTOS/include`目录中添加所有`FreeRTOS`文件夹下的`include`文件夹所有内容

![include配置](images\include配置.png)

`FreeRTOS/source`目录中添加如下内容，文件来自于`FreeRTOS`文件夹下的`source`文件夹

![source配置](images\source配置.png)

`FreeRTOS/portable`目录中添加如下内容，文件来自于`FreeRTOS`文件夹下的`portable`文件夹

![portable配置](images\portable配置.png)

`APP`目录中添加如下内容（主要就是自定义的业务逻辑文件）

![APP配置](images\APP配置.png)

以上内容添加好后，为了防止编译时找不到对应的头文件，还需要添加头文件所在的路径

1. 

![添加头文件配置](images\添加头文件配置.png)

2. 

![添加头文件配置2](images\添加头文件配置2.png)

3. 

![头文件配置](images\头文件配置.png)

#### 3.3.3 编译报错修复

编译一次会有报错，如果前面配置的正常现在应该会是这个错误：

![编译报错1](images\编译报错1.png)

解决方法：

找到这个stm32f10x_it.c里面三个空函数注释掉

![注释函数1](images\注释函数1.png)

![注释函数2](images\注释函数2.png)

![注释函数3](images\注释函数3.png)

如果出现这些错误：

1. 

![编译报错2](images\编译报错2.png)

说明没有创建`FreeRTOSConfig.h`文件且没有正确配置头文件路径

2. 

![编译报错3](images\编译报错3.png)

说明没有将`ARM_CM3`文件夹配置到头文件路径中

编译如果还有报错，如说**没有找到myusart.h**文件

解决方法：

把自己的串口相关代码修改一下文件名称即可，例如我这里原来是`Usart1.c`和`Usart1.h`

![报错解决](images\报错解决.png)

#### 3.3.4 自定义嘀嗒时钟相关代码

我这里是创建在`Public`目录下的，位置不是很重要

主要原因是FreeRTOS中延时函数要参考的时钟标准不同，这里需要单独定义（主要就是将时钟的周期直接用系统主频计算，原来的方式可能需要对72Mhz分频，这里是直接用72Mhz计算），配置完成后**系统中断周期是1ms，也就是说系统任务的轮换时间片是1ms**

建议直接复制以下内容：

头文件`systick.h`：

```c
#ifndef __SYSTICK_H
#define __SYSTICK_H

#include "stdint.h"

void systick_init();

void delay_us(uint32_t us);

void delay_ms(uint32_t ms);

#endif

```

源文件`systick.c`：

```c
#include "stm32f10x.h"                  // Device header
#include "systick.h"
#include "FreeRTOS.h"
#include "task.h"

extern void xPortSysTickHandler(void);
void SysTick_Handler(void)
{
		if(xTaskGetSchedulerState() != taskSCHEDULER_NOT_STARTED)
		{
				xPortSysTickHandler();
		}
}

static u8 fac_us=0;                             //us延时倍乘数
static u16 fac_ms=0;                            //ms延时倍乘数
void systick_init()
{
    u32 reload;
    SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK); 
    fac_us=SystemCoreClock/1000000;         //系统还没运行，以Systick计时
  
    reload=SystemCoreClock/configTICK_RATE_HZ;    //configTICK_RATE_HZ=1000
     
    fac_ms=1000/configTICK_RATE_HZ;         //系统已经运行，这就是个节拍数，用于给系统提供的延迟函数
  
    SysTick->CTRL|=SysTick_CTRL_TICKINT_Msk;//开启SYSTICK中断
    SysTick->LOAD=reload;                    //每1/configTICK_RATE_HZ断一次  
    SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk; //开启SYSTICK     
}
  
//延迟us，不会引起任务切换
//注意:nus的值,不要大于23860929us(最大值即2^32/fac_us@fac_us=180) 
void delay_us(uint32_t nus)
{       
    u32 ticks;
    u32 told,tnow,tcnt=0;
    u32 reload=SysTick->LOAD;                //LOAD的值             
    ticks=nus*fac_us;                       //需要的节拍数 
    told=SysTick->VAL;                       //刚进入时的计数器值
    while(1)
    {
        tnow=SysTick->VAL;   
        if(tnow!=told)
        {       
            if(tnow<told)tcnt+=told-tnow;    //这里注意一下SYSTICK是一个递减的计数器就可以了.
            else tcnt+=reload-tnow+told;        
            told=tnow;
            if(tcnt>=ticks)break;            //时间超过/等于要延迟的时间,则退出.
        }  
    }
}
//延时nms,其实就是对会vTaskDelay的简单封装，会引起任务调度
//nms:要延时的ms数
//nms:0~65535
void delay_ms(uint32_t nms)
{   
    if(xTaskGetSchedulerState()!=taskSCHEDULER_NOT_STARTED)//系统已经运行
    {       
        if(nms>=fac_ms)                      //延时的时间大于OS的最少时间周期 
        { 
            vTaskDelay(nms);            //FreeRTOS延时：vTaskDelay演示固定的时钟节拍，由于前面设定了频率为1000HZ，所以一个节拍就是1ms
        }
        nms%=fac_ms;                        //OS已经无法提供这么小的延时了,采用普通方式延时    
    }
    delay_us((u32)(nms*1000));              //普通方式延时
}

```

然后再编译一次，如果没有错误（警告可以忽略，大部分都是最后一行没有新行这样的警告），移植其实就算完成了

## 4. 使用

### 4.1 APP文件夹相关内容

前面创建的APP文件夹是用来放freeRTOS要执行的业务代码的，文件夹名不重要

头文件`freeRTOS_demo.h`内容：

```c
#ifndef __FREERTOS_DEMO_H
#define __FREERTOS_DEMO_H

void freeRTOS_Start(void);

#endif

```

这里的`freeRTOS_Start`函数就是整个系统的入口函数

源文件`freeRTOS_demo.c`内容：

```c
#include "stm32f10x.h"                  // Device header

#include "freeRTOS_demo.h"

#include "myusart.h"

#include "FreeRTOS.h"
#include "task.h"

TaskHandle_t start_task_Handler;

TaskHandle_t task1_Handler;
TaskHandle_t task2_Handler;
TaskHandle_t task3_Handler;

void start_Task(void *param);
void Task1(void *param);
void Task2(void *param);
void Task3(void *param);

void freeRTOS_Start(void)
{
	BaseType_t res = xTaskCreate(start_Task ,"create_allTasks" ,256 ,NULL ,2 ,&start_task_Handler);
	
	if(res == pdPASS)
	{
		Usart1_printf("startTask_create success \r\n");
	}
	
	vTaskStartScheduler();
}

void start_Task(void *param)
{
	taskENTER_CRITICAL();
	
	xTaskCreate(Task1 ,"myTask1" ,256 ,NULL ,2 ,&task1_Handler);
	xTaskCreate(Task2 ,"myTask2" ,256 ,NULL ,2 ,&task2_Handler);
	xTaskCreate(Task3 ,"myTask3" ,256 ,NULL ,2 ,&task3_Handler);
	
	vTaskDelete(NULL);
	
	taskEXIT_CRITICAL();
}

void Task1(void *param)
{
	
}

void Task2(void *param)
{
	
}

void Task3(void *param)
{
	
}

```

### 4.2 源代码解释

#### 4.2.1 初始任务

freeRTOS中去轮流运行各个要执行的任务的，而这些任务是自己创建的

整体结构上，需要**先创建一个初始任务，该任务的作用就是用来创建其他任务**

创建任务的函数：`xTaskCreate(任务要执行的函数,任务描述,任务所占用的栈大小,传给任务函数的参数,任务的优先级,任务句柄的地址);`

函数的具体解释可以查看官方文档或者询问AI，这里不过多赘述

```c
//初始任务的句柄
TaskHandle_t start_task_Handler;
//初始任务声明
void start_Task(void *param);

void freeRTOS_Start(void)
{
    //创建初始任务
	BaseType_t res = xTaskCreate(start_Task ,"create_allTasks" ,256 ,NULL ,2 ,&start_task_Handler);
	//判断是否创建完成	
	if(res == pdPASS)
	{
		Usart1_printf("startTask_create success \r\n");
	}
	//开启任务调度
	vTaskStartScheduler();
}
```

**创建好任务并判断是否创建完成后，必须开启任务调度`vTaskStartScheduler()`，否则系统会只执行这个初始任务**

**初始任务的参数列表必须要和上面示例的一致，因为创建时有一个向该函数传递参数的步骤，所以不能为void**

这里面说的“句柄”，可以简单理解为一个指向这个任务的指针，通过这个指针可以获取到这个任务的相关信息，不用深究

#### 4.2.2 业务逻辑任务

业务逻辑任务由初始任务进行创建

```c
//业务逻辑任务的句柄
TaskHandle_t task1_Handler;
TaskHandle_t task2_Handler;
TaskHandle_t task3_Handler;

//业务逻辑任务的声明
void Task1(void *param);
void Task2(void *param);
void Task3(void *param);

//初始任务的实现
void start_Task(void *param)
{
    //进入代码临界区
	taskENTER_CRITICAL();
	
	xTaskCreate(Task1 ,"myTask1" ,256 ,NULL ,2 ,&task1_Handler);
	xTaskCreate(Task2 ,"myTask2" ,256 ,NULL ,2 ,&task2_Handler);
	xTaskCreate(Task3 ,"myTask3" ,256 ,NULL ,2 ,&task3_Handler);
	//将业务逻辑任务创建完毕就删除自身任务，不用再运行，防止业务逻辑任务多次被创建
	vTaskDelete(NULL);
	//退出代码临界区
	taskEXIT_CRITICAL();
}

//业务逻辑函数实现（示例）
void Task1(void *param)
{
	
}

void Task2(void *param)
{
	
}

void Task3(void *param)
{
	
}

```

上面所谓的“代码临界区”，**由于系统会不断切换任务，这里初始任务主要目的就是创建其他业务逻辑任务，因此最好是一次都创建好然后再切换，防止创建到一半就切换**，主要使用的就是`taskENTER_CRITICAL();`和`taskEXIT_CRITICAL();`函数

#### 4.2.3 main函数

main函数中不需要使用死循环，内容参考以下即可：

```c
#include "stm32f10x.h"
#include "systic.h"
#include "myusart.h"

#include "free_demo.h"

int main()
{
	systick_init();
	//硬件外设初始化，比如LED之类的
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	Usart1_Init(115200);
	//必须添加
	freeRTOS_Start();
}


```

#### 4.2.4 简单示例

任务1：LED1闪烁，周期为0.5s

任务2：LED2闪烁，周期为0.5s

任务3：如果按键1按下，则删除任务1

`freeRTOS_demo.c`中的代码（LED和按键的设置仅供参考，具体IO配置需要结合实际板子资源）：

```c
#include "stm32f10x.h"                  // Device header

#include "myusart.h"
#include "Led.h"
#include "Key.h"

#include "freeRTOS_demo.h"
#include "FreeRTOS.h"
#include "task.h"//包含创建、挂起、恢复、删除任务

TaskHandle_t start_mytask_Handler;

TaskHandle_t myTask1_Handler;
TaskHandle_t myTask2_Handler;
TaskHandle_t myTask3_Handler;

void start_mytask(void *param);

void myTask1(void *param);
void myTask2(void *param);
void myTask3(void *param);

void freeRTOS_start(void)
{
	//初始任务为创建其他任务
	BaseType_t res =  xTaskCreate(
																//任务函数
																start_mytask,
																//任务描述
																"create_allTasks",
																//任务所分配的堆栈字数
																256,
																//给任务传递的参数
																NULL,
																//任务执行优先级，数字越大优先级越高
																2,
																//任务的句柄
																&start_mytask_Handler
	);
	
	if(res == pdPASS)
	{
		Usart1_printf("start Task create Success");
	}
	
	//任务调度
	vTaskStartScheduler();
	
}

void start_mytask(void *param)
{
	//三个子任务都创建完毕后再运行
	
	taskENTER_CRITICAL();
	
	//task1:led1闪烁
	xTaskCreate(myTask1 ,"Led1" ,256 ,NULL ,2 ,&myTask1_Handler);
	//task2:led2闪烁
	xTaskCreate(myTask2 ,"Led2" ,256 ,NULL ,2 ,&myTask2_Handler);
	//task3:key检测
	xTaskCreate(myTask3 ,"Led3" ,256 ,NULL ,2 ,&myTask3_Handler);
	
	//创建完成后删除自己
	vTaskDelete(NULL);
	
	taskEXIT_CRITICAL();
	
}

void myTask1(void *param)
{
	while(1)
	{
		Led_On(LED1);
		vTaskDelay(500);
		Led_Off(LED1);
		vTaskDelay(500);
	}
}	

void myTask2(void *param)
{	
	while(1)
	{
		Led_On(LED2);
		vTaskDelay(500);
		Led_Off(LED2);
		vTaskDelay(500);
	}
}

void myTask3(void *param)
{
	uint8_t KeyNum = 0;
	while(1)
	{
		KeyNum = get_KeyNum();
		if(KeyNum == 1)
		{
			vTaskDelete(myTask1_Handler);
		}
	}
}
```

`main.c`内容：

```c
#include "stm32f10x.h"
#include "systic.h"
#include "myusart.h"
#include "Key.h"
#include "Led.h"
#include "freeRTOS_demo.h"

int main()
{
	systick_init();
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
	Usart1_Init(115200);
	Key_Init();
	Led_Init();
	
	freeRTOS_start();
	
   //return 0;
}
```

附：

`led.c`内容：

```c
#include "stm32f10x.h"                  // Device header
#include "Led.h"

void Led_Init(void)
{
	//PA0-PA7 低电平触发
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA ,ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 |GPIO_Pin_2 |GPIO_Pin_3 |GPIO_Pin_4 |GPIO_Pin_5 |GPIO_Pin_6 |GPIO_Pin_7;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	
	GPIO_Init(GPIOA ,&GPIO_InitStructure);
	
	//初始默认关闭
	GPIO_SetBits(GPIOA ,GPIO_Pin_0);
	GPIO_SetBits(GPIOA ,GPIO_Pin_1);
	GPIO_SetBits(GPIOA ,GPIO_Pin_2);
	GPIO_SetBits(GPIOA ,GPIO_Pin_3);
	GPIO_SetBits(GPIOA ,GPIO_Pin_4);
	GPIO_SetBits(GPIOA ,GPIO_Pin_5);
	GPIO_SetBits(GPIOA ,GPIO_Pin_6);
	GPIO_SetBits(GPIOA ,GPIO_Pin_7);
}

uint8_t getLedState(uint8_t Led_Num)
{
	switch(Led_Num)
	{
		case LED1:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_0);
		
		case LED2:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_1);
		
		case LED3:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_2);
		
		case LED4:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_3);
		
		case LED5:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_4);
		
		case LED6:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_5);
		
		case LED7:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_6);
		
		case LED8:
			return GPIO_ReadOutputDataBit(GPIOA ,GPIO_Pin_7);
	}
}

void Led_On(uint8_t Led_Num)
{
	switch(Led_Num)
	{
		case LED1:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_0);
		break;
		case LED2:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_1);
		break;
		case LED3:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_2);
		break;
		case LED4:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_3);
		break;
		case LED5:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_4);
		break;
		case LED6:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_5);
		break;
		case LED7:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_6);
		break;
		case LED8:
			GPIO_ResetBits(GPIOA ,GPIO_Pin_7);
		break;
	}
}

void Led_Off(uint8_t Led_Num)
{
	switch(Led_Num)
	{
		case LED1:
			GPIO_SetBits(GPIOA ,GPIO_Pin_0);
		break;
		case LED2:
			GPIO_SetBits(GPIOA ,GPIO_Pin_1);
		break;
		case LED3:
			GPIO_SetBits(GPIOA ,GPIO_Pin_2);
		break;
		case LED4:
			GPIO_SetBits(GPIOA ,GPIO_Pin_3);
		break;
		case LED5:
			GPIO_SetBits(GPIOA ,GPIO_Pin_4);
		break;
		case LED6:
			GPIO_SetBits(GPIOA ,GPIO_Pin_5);
		break;
		case LED7:
			GPIO_SetBits(GPIOA ,GPIO_Pin_6);
		break;
		case LED8:
			GPIO_SetBits(GPIOA ,GPIO_Pin_7);
		break;
	}
}

```

附：

`key.c`内容：

```c
#include "stm32f10x.h"                  // Device header
#include "Key.h"
#include "systic.h"

//PA12-15 低电平有效

void Key_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA ,ENABLE);
	//PA13和14是SWCLK SWDIO，需要使用普通GPIO模式需要关闭调试模式
	//使能AFIO
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO ,ENABLE);
	//关闭调试功能
	GPIO_PinRemapConfig(GPIO_Remap_SWJ_JTAGDisable ,ENABLE);
	GPIO_PinRemapConfig(GPIO_Remap_SWJ_Disable ,ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12 |GPIO_Pin_13 |GPIO_Pin_14 |GPIO_Pin_15;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	
	GPIO_Init(GPIOA ,&GPIO_InitStructure);
	
}

uint8_t get_KeyNum(void)
{
	uint8_t KeyNum = 0;
	
	if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_12) == 0)//按下
	{
		delay_us(20);
		while(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_12) == 0);
		delay_us(20);//松手消抖
		if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_12) == 1)
		{
			KeyNum = 1;
		}
	}
	else if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_13) == 0)
	{
		delay_us(20);
		while(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_13) == 0)
		delay_us(20);
		if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_13) == 1)
		{
			KeyNum = 2;
		}
	}
	else if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_14) == 0)
	{
		delay_us(20);
		while(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_14) == 0)
		delay_us(20);
		if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_14) == 1)
		{
			KeyNum = 3;
		}
	}
	else if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_15) == 0)
	{
		delay_us(20);
		while(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_15) == 0)
		delay_us(20);
		if(GPIO_ReadInputDataBit(GPIOA ,GPIO_Pin_15) == 1)
		{
			KeyNum = 4;
		}
	}
	return KeyNum;
}

```

