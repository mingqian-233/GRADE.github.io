from PIL import Image

def make_background_transparent(input_path, output_path, rgb_min, rgb_max):
    # 打开图片并转为 RGBA 模式
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        r, g, b, a = item
        # 判断当前像素是否在背景 RGB 区间内
        if (rgb_min[0] <= r <= rgb_max[0] and
            rgb_min[1] <= g <= rgb_max[1] and
            rgb_min[2] <= b <= rgb_max[2]):
            # 背景像素设为完全透明
            new_data.append((r, g, b, 0))
        else:
            # 保留原像素
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"处理完成，已保存为: {output_path}")

if __name__ == "__main__":
    # 输入输出路径
    input_img = "/mnt/nas-new/home/yangxue/lmx/image/GRADE.github.io/static/images/logo.png"   # 替换为你的图片路径
    output_img = "/mnt/nas-new/home/yangxue/lmx/image/GRADE.github.io/static/images/logo_transparent.png"

    # 背景 RGB 区间（根据这张图的白色背景微调）
    rgb_min = (240, 240, 240)
    rgb_max = (255, 255, 255)

    make_background_transparent(input_img, output_img, rgb_min, rgb_max)