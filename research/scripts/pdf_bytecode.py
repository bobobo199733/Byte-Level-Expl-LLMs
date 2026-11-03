import dis
import inspect
import importlib.util
from PIL import Image, ImageDraw, ImageFont


INPUT_FILE = "../test_data/outputs/llama/cleaned/t41_p1_r1_llama.py"
FUNCTION_NAME = "group_anagrams"
OUTPUT_FILE = "group_anagrams_bytecode.png"


def load_module_from_file(file_path):
    spec = importlib.util.spec_from_file_location("target_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_text_as_png(lines, output_file):
    font = ImageFont.load_default()

    line_height = 16
    padding = 20

    width = max(font.getbbox(line)[2] for line in lines) + padding * 2
    height = len(lines) * line_height + padding * 2

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        draw.text((padding, y), line, fill="black", font=font)
        y += line_height

    img.save(output_file)


def main():
    module = load_module_from_file(INPUT_FILE)

    func = getattr(module, FUNCTION_NAME)

    source_header = inspect.getsource(func).splitlines()[0]
    bytecode = dis.Bytecode(func).dis()

    lines = [
        source_header,
        "",
        "=== BYTECODE ===",
        "",
        *bytecode.splitlines()
    ]

    save_text_as_png(lines, OUTPUT_FILE)

    print(f"Saved bytecode image to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
