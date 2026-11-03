from pathlib import Path
import dis
import py_compile
import tempfile
import marshal


def convert_python_to_bytecode(py_file: str):
    py_file = Path(py_file)

    if not py_file.exists():
        raise FileNotFoundError(f"File not found: {py_file}")

    # Temporary compiled file
    with tempfile.NamedTemporaryFile(suffix=".pyc", delete=False) as tmp:
        pyc_path = Path(tmp.name)

    try:
        # Compile source -> .pyc
        py_compile.compile(
            file=str(py_file),
            cfile=str(pyc_path),
            doraise=True
        )

        # Read raw .pyc bytes
        raw_data = pyc_path.read_bytes()

        print("=" * 60)
        print("RAW BYTE VALUES (first 100)")
        print("=" * 60)

        byte_values = list(raw_data)
        print("total bytes:", len(raw_data))

        print(byte_values)

        print("\n")

        print("=" * 60)
        print("RAW BINARY (first 30)")
        print("=" * 60)

        binary_values = [format(b, "08b") for b in byte_values[:30]]

        print(binary_values)

        print("\n")

        # Skip .pyc header (16 bytes in modern Python)
        code_object = marshal.loads(raw_data[16:])

        print("=" * 60)
        print("DISASSEMBLED PYTHON BYTECODE")
        print("=" * 60)

        dis.dis(code_object)

    finally:
        if pyc_path.exists():
            pyc_path.unlink()


if __name__ == "__main__":
    file_path = "../outputs/llama/cleaned/t1_p1_r1_llama.py"

    convert_python_to_bytecode(file_path)
