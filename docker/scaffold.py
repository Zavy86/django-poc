"""Generate the local Django starter and register additional apps."""

import argparse
import ast
import keyword
from pathlib import Path

from django.core.management import call_command


TEMPLATES = Path(__file__).parent / "templates"
SETTINGS = Path("config/settings.py")
TESTS = Path.cwd().parent / "tests"


def test_directory(name):
    directory = TESTS / name
    directory.mkdir(parents=True, exist_ok=True)
    (TESTS / "__init__.py").touch(exist_ok=True)
    (directory / "__init__.py").touch(exist_ok=True)
    return directory


def installed_apps(source):
    for statement in ast.parse(source).body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "INSTALLED_APPS"
            for target in statement.targets
        ):
            if not isinstance(statement.value, ast.List):
                break
            values = ast.literal_eval(statement.value)
            if all(isinstance(value, str) for value in values):
                return statement.value, values
    raise ValueError("config/settings.py must define INSTALLED_APPS as a list of strings")


def register_app(name):
    source = SETTINGS.read_text()
    node, values = installed_apps(source)
    app_source = ast.parse(Path(name, "apps.py").read_text())
    config_class = next(item.name for item in app_source.body if isinstance(item, ast.ClassDef))
    entry = f"{name}.apps.{config_class}"
    if entry in values or name in values:
        return
    values.append(entry)
    lines = source.splitlines(keepends=True)
    start = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
    end = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
    replacement = "[\n" + "".join(f"    {value!r},\n" for value in values) + "]"
    SETTINGS.write_text(source[:start] + replacement + source[end:])


def project(name):
    if any(Path.cwd().iterdir()):
        raise ValueError("app/src/ must be empty before running make generate")
    for test_path in (
        TESTS / name / "test_index.py",
        TESTS / "config/test_admin.py",
        TESTS / "config/test_welcome.py",
    ):
        if test_path.exists():
            raise ValueError(f"{test_path} already exists")
    call_command("startproject", "config", ".")
    SETTINGS.write_text((TEMPLATES / "settings.py").read_text())
    Path("config/views.py").write_text((TEMPLATES / "welcome.py").read_text())
    Path("config/urls.py").write_text(
        (TEMPLATES / "urls.py").read_text().replace("__APP_NAME__", name)
    )


def app(name):
    # Check the configuration before creating files.
    installed_apps(SETTINGS.read_text())
    call_command("startapp", name)
    Path(name, "tests.py").unlink()
    test_directory(name)
    register_app(name)


def hello(name):
    test_path = test_directory(name) / "test_index.py"
    with test_path.open("x") as test_file:
        test_file.write(
            (TEMPLATES / "test_index.py").read_text().replace("__APP_NAME__", name)
        )
    for filename in ("test_admin.py", "test_welcome.py"):
        with (test_directory("config") / filename).open("x") as test_file:
            test_file.write((TEMPLATES / filename).read_text())
    Path(name, "views.py").write_text((TEMPLATES / "views.py").read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("project", "app", "hello"))
    parser.add_argument("name")
    args = parser.parse_args()
    if not args.name.isidentifier() or keyword.iskeyword(args.name) or args.name == "config":
        parser.error("Choose a valid Python app name other than config")
    try:
        {"project": project, "app": app, "hello": hello}[args.command](args.name)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
