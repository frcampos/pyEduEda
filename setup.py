from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

setup(
    name="convimagens",
    version="1.0",
    description="Converter imagens para a resolução especifica e compressão para a Web em formato jpg",
    executables=executables, options={
        "cimagens_exe": {
            "includes": ["Pillow"]
        }
    }
)
