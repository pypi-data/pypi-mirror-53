from setuptools import setup, find_packages


setup(
    name="bandori_play",
    version="0.0.0",
    description="Play and download bandori's music.",
    author="kazukazuprogram",
    author_email="dbycvil8yiyf7xnlxvh7@yahoo.co.jp",
    maintainer='kazukazuprogram',
    maintainer_email="dbycvil8yiyf7xnlxvh7@yahoo.co.jp",
    install_requires=["requests", "bs4"],
    packages=find_packages(),
    license="MIT",
    package_dir={"bandori_play": "bandori_play"},
    package_data={"bandori_play": ["bin\\*.exe"]},
    entry_points={
        "console_scripts": [
            "bandp = bandori_play.__init__:start",
        ]
    }
)
