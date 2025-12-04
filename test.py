from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
import config as conf

# ✅ Исправлены импорты (файлы в корне, не в папке generators)

post_gen = PostGenerator(
    conf.openai_key,
    tone="позитивный и весёлый",
    topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
)

content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

img_gen = ImageGenerator(conf.openai_key)
image_url = img_gen.generate_image(img_desc)

print("=== СГЕНЕРИРОВАННЫЙ ПОСТ ===")
print(content)
print("\n=== URL ИЗОБРАЖЕНИЯ ===")
print(image_url)