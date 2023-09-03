from setuptools import setup, find_packages

setup(
    name="Pytinerary",
    version="0.1",
    description="Timetable-based journey planner",
    url="http://github.com/RTopolowski/pytinerary",
    author="Robert Topolowski",
    author_email="robert.topolowski@topolowski.com",
    license="MIT",
    packages=["pytinerary"],
    test_suite="tests",
    zip_safe=False,
)
