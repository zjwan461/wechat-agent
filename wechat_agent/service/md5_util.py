import hashlib

def calculate_md5(text):
    # 创建MD5对象
    md5_hash = hashlib.md5()

    # 更新哈希对象，需要先将字符串编码为字节
    md5_hash.update(text.encode('utf-8'))

    # 获取十六进制哈希值
    return md5_hash.hexdigest()