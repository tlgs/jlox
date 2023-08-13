"""We do a little bit of metaprogramming."""
import sys


def define_ast(output_dir, base_name, types):
    path = f"{output_dir}/{base_name}.java"

    with open(path, "w") as f:
        f.write("package com.jlox.lox;\n")
        f.write("\n")
        f.write("import java.util.List;\n")
        f.write("\n")
        f.write(f"abstract class {base_name} {{\n")

        define_visitor(f, base_name, types)

        # The AST classes.
        for t in types:
            raw_name, raw_fields = t.split(":")
            class_name = raw_name.rstrip()
            fields = raw_fields.lstrip()

            f.write("\n")
            define_type(f, base_name, class_name, fields)

        # The base accept() method.
        f.write("\n")
        f.write("  abstract <R> R accept(Visitor<R> visitor);\n")

        f.write("}\n")


def define_visitor(f, base_name, types):
    f.write("  interface Visitor<R> {\n")

    for t in types:
        raw_name, _ = t.split(":")
        type_name = raw_name.rstrip()
        f.write(
            f"    R visit{type_name}{base_name}({type_name} {base_name.lower()});\n"
        )

    f.write("  }\n")


def define_type(f, base_name, class_name, field_list):
    f.write(f"  static class {class_name} extends {base_name} {{\n")

    # Constructor.
    f.write(f"    {class_name} ({field_list}) {{\n")

    # Store parameters in fields.
    fields = field_list.split(", ")
    for field in fields:
        _, name = field.split()
        f.write(f"      this.{name} = {name};\n")

    f.write("    }\n")

    # Visitor pattern.
    f.write("\n")
    f.write("    @Override\n")
    f.write("    <R> R accept(Visitor<R> visitor) {\n")
    f.write(f"      return visitor.visit{class_name}{base_name}(this);\n")
    f.write("    }\n")

    # Fields.
    f.write("\n")
    for field in fields:
        f.write(f"    final {field};\n")

    f.write("  }\n")


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        return 64

    output_dir = args[0]

    expr_types = [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right",
    ]
    define_ast(output_dir, "Expr", expr_types)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
