from setuptools import setup, find_packages

setup(
    name="tf_attention_layer",
    version="0.1.1",
    packages=find_packages(include=["tf_attention_layer", "tf_attention_layer.*"]),
    url="https://github.com/howl-anderson/tf_attention_layer",
    license="MIT",
    install_requires=["tensorflow", "tokenizer_tools"],
    tests_require=["pytest", "numpy", "keras", "pandas"],
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    description="Attention layer for TensorFlow 1.x",
)
