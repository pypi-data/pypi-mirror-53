import re
def handle_args(data):
    """
    data 是一个字典
    1. 遍历字典
    2. 将key下划线转驼峰
    """
    new_data = {}
    for key, value in data.items():
        key = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(),key)
        new_data[key] = value
    return new_data