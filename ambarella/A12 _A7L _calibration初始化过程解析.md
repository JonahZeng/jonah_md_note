# A7L如何初始化warp  CA  vignette#

----------

1.  `app_pre_init(void)` 调用 `app_calib_load_data(0)`
2.  `app_calib_load_data(0)`调用` calib_init_stage0()`
3.  `calib_init_stage0()`调用如下函数分别从ROMFS或者NAND加载校正参数到DRAM：

      
          calib_init(CAL_WARP_ID,CALIB_LOAD,FULL_LOAD);
          calib_init(CAL_VIGNETTE_ID,CALIB_LOAD,FULL_LOAD);
          calib_init(CAL_CA_ID,CALIB_LOAD,FULL_LOAD);
4. `int calib_init(u32 cal_id,u8 job_id, u32 partial_id)`加载过程,如下是缩略代码
```c
        int calib_init(u32 cal_id,u8 job_id, u32 partial_id)
         {
	        ......
	        if(job_id == CALIB_LOAD)
	         {
	           if(format==CALIB_SOURCE_ROMFS)//warp ca从这里加载，然后直接结束函数。
	             {
	               calib_partial_load_rom(cal_obj, cal_id, CALIB_TABLE_IDX_INIT, CALIB_TABLE_COUNT_INIT, CALIB_LOAD);
	               reutrn  ；
	             }
	           else if(format==CALIB_SOURCE_NAND)//vignette从这里加载
	            {
	              calib_load(cal_id,partial_id)；
	              (cal_obj->upgrade_func)(cal_obj, p_cal_site)；//检查校正版本
	            }
	            ........
	         }
```		 
5. `app_init(void)` 调用  `app_calib_load_data(1)`
6. `app_calib_load_data(1)`调用`calib_init_stage1()`
```c
       	calib_init(CAL_WARP_ID,CALIB_INIT,FULL_LOAD);   //使用DRAM当中参数初始化WARP
		calib_init(CAL_VIGNETTE_ID,CALIB_INIT,FULL_LOAD);  //使用DRAM当中参数初始化vignette
		
		-----------------------------------------------------------------------------------
		int calib_init(u32 cal_id,u8 job_id, u32 partial_id)
		{
		    .........
		    else   //job_id==CALIB_INIT
	       {
		      if(cal_obj->init_func != NULL) 
		       {
			     (cal_obj->init_func)(cal_obj) ;
	       	   }
           	}
           	..........
		}
		---------------------------------------------------------------------------------------
		//关于init_func函数，如下cal_obj_t结构已经定义 ，比如vignette的初始化函数是vignette_init_func
		cal_obj_t cal_obj_ambarella[] = {
			......
			/* 05 */ {1, CAL_VIGNETTE_ID, CAL_VIGNETTE_SIZE, CAL_VIGNETTE_VER, "VIGNETTE", NULL, vignette_init_func, vignette_upgrade_func, vignette_calib_func },
			......
		};
		
		
		-------------------------------------------------------------------------------------
		//vignette_init_func()继续调用int cal_init_vignette(cal_obj_t *cal_obj)
		int cal_init_vignette(cal_obj_t *cal_obj)
        {
	     ...........
	      u8 *vig_addr = cal_obj->dram_shadow;   //DRAM中参数地址
	     ...........
      
	     //app_vignette_control是全局性的，转换成vignette_param_t  后用
	     //AMP_img_algo_cmd(MW_IA_CAL_VIGNETTE, VIGNETTE_OP_SET_ENABLE, &vig_param);	//vignette enable
	     app_vignette_control.enable = vig_addr[CAL_VIGNETTE_ENABLE];
	     ..........
	     app_vignette_control.gain_table_count = vig_addr[CAL_VIGNETTE_TABLE_COUNT];
	     
	    .............
	     return 0;	
       }
```
　　    
7. `app_post_init(void)`调用`app_calib_load_data(2)`
8. `app_calib_load_data(2)`调用`calib_init_stage2()`
```
           calib_init(CAL_CA_ID,CALIB_INIT,FULL_LOAD);  //CA初始化
```


# A12如何初始化warp CA vignette#

----------


初始化步骤0：
```c
    void AppLib_CalibInitStage0(void)
    {

    AppLib_CalibInitFunc(CAL_STATUS_ID,CALIB_LOAD,CALIB_FULL_LOAD);
    AppLib_CalibInitFunc(CAL_VIGNETTE_ID,CALIB_LOAD,CALIB_FULL_LOAD);
    AppLib_CalibInitFunc(CAL_WARP_ID,CALIB_LOAD,CALIB_FULL_LOAD); //详情见下
    AppLib_CalibInitFunc(CAL_CA_ID,CALIB_LOAD,CALIB_FULL_LOAD);

    }
```    
初始化步骤1：
```c
    void AppLib_CalibInitStage1(void)  //CALIB_INIT!=CALIB_LOAD，所以调用初始化函数从DRAM读数据
    {
    AppLib_CalibInitFunc(CAL_VIGNETTE_ID,CALIB_INIT,0);
    AppLib_CalibInitFunc(CAL_WARP_ID,CALIB_INIT,0);
    AppLib_CalibInitFunc(CAL_CA_ID,CALIB_INIT,0);
    }
```    
函数解析：
```c
    int AppLib_CalibInitFunc(UINT32 CalId,UINT8 JobId, UINT8 SubId)
    {
    ...........
    if (JobId == CALIB_LOAD)
		{
        // Print site Status
        UINT8 format = CalFormat[CalId];

        CalMgrPrint("CalId #%d", CalId);
        if ((PCalSite->Status == CAL_SITE_DONE) || (CalId == CAL_STATUS_ID) ||(format == CALIB_SOURCE_ROMFS))
		{
            
            AppLib_CalibCheckSize(CalId);
            if (format == CALIB_SOURCE_ROMFS) //因为WARP ca是定义成CALIB_SOURCE_ROMFS
				{
                Rval = AppLib_CalibROMLoadTable(CalId, SubId, 1);//从ROM加载到DRAM
                return Rval;
                } 
			else 
				{ // Load calibration data from NAND to DRAM
                #if (CALIB_STORAGE == CALIB_FROM_NAND)
                Rval = AppLib_CalibNandLoadTable(CalId,SubId,1);// vignette从NAND加载到DRAM。
                #else
                Rval = AppLib_CalibSDCardLoad(CalId);
                #endif
                ..................
                }
        }
		..................
     } 
	else { //如果不是CALIB_LOAD,则开始初始化
        if (CalObj->InitFunc != NULL) 
			{
            if ((CalObj->InitFunc)(CalObj) < 0) //直接用初始化CalObj结构里的初始化函数进行初始化。
				{
                CalMgrPrint("[CAL] Site %s %d init fail", CalName, CalId);
                return -1;
                }
            }
        CalMgrPrint("[CAL] Init site %s %d success", CalName, CalId);
    }
    return 0;
}  
```

#结论：
warp CA 和其他校正的区别是存储在ROMFS，首先仍然是要加载到DRAM当中，然后进行下一步的初始化。ROM file system
vignette则是存储在NAND flash当中，首先也是加载到DRAM中，然后进行下一步初始化。

```c
    /*Calibration load data format*/
    
    #define CAL_STATUS_LOAD_FORMAT         (CALIB_SOURCE_NAND)
    #define CAL_AF_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_GYRO_LOAD_FORMAT        (CALIB_SOURCE_NAND)
    #define CAL_MSHUTTER_LOAD_FORMAT    (CALIB_SOURCE_NAND)
    #define CAL_IRIS_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_VIGNETTE_LOAD_FORMAT    (CALIB_SOURCE_NAND)
    #define CAL_FPN_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_WB_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_ISO_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_BLC_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_FLASH_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_AUDIO_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_WARP_LOAD_FORMAT          (CALIB_SOURCE_NAND)
    #define CAL_CA_LOAD_FORMAT             (CALIB_SOURCE_NAND)
    #define CAL_LENSSHIFT_LOAD_FORMAT    (CALIB_SOURCE_NAND)
```    
所以如果定义` #define CAL_WARP_LOAD_FORMAT   CAL_WARP_LOAD_FORMAT       (CALIB_SOURCE_NAND)`的话，初始化函数从NAND读数据，得到的是一个空值，所以warp CA被disable掉了。