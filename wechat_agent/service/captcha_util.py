from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import io
import base64


def generate_base64_captcha(length=4, width=120, height=40, font_size=30):
    """
    生成4位验证码图片并返回Base64编码字符串和验证码文本

    返回:
        tuple: (base64_str, captcha_text)
              base64_str: 图片的Base64编码字符串
              captcha_text: 验证码文本内容
    """
    # 创建空白图片和绘图对象
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 生成随机4位字符（字母+数字）
    chars = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(chars) for _ in range(length))

    try:
        # 尝试加载系统字体，如无则使用默认字体
        font = ImageFont.truetype('arial.ttf', font_size)
    except:
        font = ImageFont.load_default()

    # 绘制字符，每个字符位置和颜色随机
    for i, char in enumerate(captcha_text):
        color = (random.randint(30, 100), random.randint(30, 100), random.randint(30, 100))
        draw.text(
            (30 * i + 10, random.randint(5, 10)),
            char,
            font=font,
            fill=color
        )

    # 绘制干扰线
    for _ in range(5):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.line(
            [
                (random.randint(0, width), random.randint(0, height)),
                (random.randint(0, width), random.randint(0, height))
            ],
            fill=color,
            width=2
        )

    # 绘制噪点
    for _ in range(50):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.point(
            [random.randint(0, width), random.randint(0, height)],
            fill=color
        )

    # 添加轻微模糊
    image = image.filter(ImageFilter.GaussianBlur(radius=0.5))

    # 转换为Base64编码
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    img_bytes = buffer.read()
    base64_str = "data:image/png;base64," + base64.b64encode(img_bytes).decode('utf-8')

    return base64_str, captcha_text


# 示例使用
if __name__ == "__main__":
    # 生成验证码
    base64_image, code = generate_base64_captcha()

    # 打印结果（实际应用中会将此返回给前端）
    print(f"验证码文本: {code}")
    print("Base64图片编码:")
    print(base64_image)  # 前端可直接将此作为img标签的src属性值
