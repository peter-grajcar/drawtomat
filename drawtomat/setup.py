from distutils.core import setup

setup(
    name="Drawtomat",
    description="Automatic generation of drawings from description",
    version="0.0.1",
    author="Peter Grajcar",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    data_files=[("resources", [
        "resources/predicates.txt",
        "resources/logging.conf",
        "resources/quickdraw",
    ])]
)
