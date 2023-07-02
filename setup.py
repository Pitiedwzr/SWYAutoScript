import subprocess
import os

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode().strip()

def setup_minicap():
    # 获取当前脚本的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建adb和minicap的相对路径
    adb_path = os.path.join(script_dir, 'adb', 'adb.exe')
    minicap_path = os.path.join(script_dir, 'bin', 'minicap', 'minicap')
    
    # 推送minicap和minicap.so到设备
    execute_command(f'{adb_path} push {minicap_path} /data/local/tmp/')
    execute_command(f'{adb_path} push {minicap_path}.so /data/local/tmp/')
    
    # 设置minicap文件的权限
    execute_command(f'{adb_path} shell chmod 777 /data/local/tmp/minicap*')
    
    # 获取设备分辨率
    resolution_output = execute_command(f'{adb_path} shell wm size')
    resolution = resolution_output.split()[-1]  # 提取分辨率部分
    
    # 启动minicap
    minicap_command = f'{adb_path} shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {resolution}@{resolution}/0'
    execute_command(minicap_command)
    
    # 设置端口转发
    execute_command(f'{adb_path} forward tcp:1717 localabstract:minicap')

def setup_minitouch():
    # 获取当前脚本的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建adb和minicap的相对路径
    adb_path = os.path.join(script_dir, 'adb', 'adb.exe')
    minitouch_path = os.path.join(script_dir, 'bin', 'minitouch', 'minitouch')
    
    # 推送minitouch到设备
    execute_command(f'{adb_path} push {minitouch_path} /data/local/tmp/')
    
    # 设置minitouch文件的权限
    execute_command(f'{adb_path} shell chmod 777 /data/local/tmp/minitouch')

    # 启动minitouch
    minicap_command = f'{adb_path} shell /data/local/tmp/minitouch'
    execute_command(minicap_command)
    
    # 设置端口转发
    execute_command(f'{adb_path} forward tcp:1111 localabstract:minitouch')

setup_minicap()
setup_minitouch()