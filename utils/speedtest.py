import subprocess

def test_node_speed(node_info):
    # 简单的 ping 测试
    try:
        result = subprocess.run(["ping", "-c", "1", node_info], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        for line in output.splitlines():
            if "time=" in line:
                return line.split("time=")[1].split(" ")[0]
        return "Timeout"
    except Exception:
        return "Error"