import pynvml

# 初始化库
pynvml.nvmlInit()

# 获取GPU数量
gpu_count = pynvml.nvmlDeviceGetCount()
print(f"检测到 {gpu_count} 块NVIDIA GPU：\n")

# 遍历每块GPU，打印详细信息
for i in range(gpu_count):
    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
    # 基础信息
    gpu_name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
    gpu_uuid = pynvml.nvmlDeviceGetUUID(handle).decode('utf-8')
    # 显存信息（单位：字节，转换为GB）
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    mem_used = mem_info.used / 1024**3
    mem_total = mem_info.total / 1024**3
    mem_free = mem_info.free / 1024**3
    # 使用率和温度
    gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
    
    # 打印格式化信息
    print(f"=== GPU {i}: {gpu_name} ===")
    print(f"UUID: {gpu_uuid}")
    print(f"显存使用: {mem_used:.2f} GB / {mem_total:.2f} GB (剩余: {mem_free:.2f} GB)")
    print(f"GPU使用率: {gpu_util}%")
    print(f"GPU温度: {gpu_temp}°C\n")

# 释放资源
pynvml.nvmlShutdown()