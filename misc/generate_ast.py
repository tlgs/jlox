"""We do a little bit of metaprogramming."""
import sys


def define_ast(output_dir, base_name, types) -> None:
    path = f"{output_dir}/{base_name}.java"

    lines = []

    lines.append("package com.jlox.lox;")
    lines.append("")
    lines.append("import java.util.List;")
    lines.append("")
    lines.append(f"abstract class {base_name} {{")

    lines.extend(define_visitor(base_name, types))

    # The AST classes.
    for class_name, fields in types:
        lines.append("")
        lines.extend(define_type(base_name, class_name, fields))

    # The base accept() method.
    lines.append("")
    lines.append("  abstract <R> R accept(Visitor<R> visitor);")

    lines.append("}")

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

    return


def define_visitor(base_name, types) -> list[str]:
    lines = []
    lines.append("  interface Visitor<R> {")

    for type_name, _ in types:
        lines.append(
            f"    R visit{type_name}{base_name}({type_name} {base_name.lower()});"
        )

    lines.append("  }")
    return lines


def define_type(base_name, class_name, field_list) -> list[str]:
    lines = []
    lines.append(f"  static class {class_name} extends {base_name} {{")

    # Constructor.
    lines.append(f"    {class_name} ({field_list}) {{")

    # Store parameters in fields.
    fields = field_list.split(", ")
    for field in fields:
        _, name = field.split()
        lines.append(f"      this.{name} = {name};")

    lines.append("    }")

    # Visitor pattern.
    lines.append("")
    lines.append("    @Override")
    lines.append("    <R> R accept(Visitor<R> visitor) {")
    lines.append(f"      return visitor.visit{class_name}{base_name}(this);")
    lines.append("    }")

    # Fields.
    lines.append("")
    for field in fields:
        lines.append(f"    final {field};")

    lines.append("  }")
    return lines


def main() -> int:
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        return 64

    output_dir = args[0]

    expr_types = [
        ("Assign", "Token name, Expr value"),
        ("Binary", "Expr left, Token operator, Expr right"),
        ("Call", "Expr callee, Token paren, List<Expr> arguments"),
        ("Grouping", "Expr expression"),
        ("Literal", "Object value"),
        ("Logical", "Expr left, Token operator, Expr right"),
        ("Unary", "Token operator, Expr right"),
        ("Variable", "Token name"),
    ]
    define_ast(output_dir, "Expr", expr_types)

    stmt_types = [
        ("Block", "List<Stmt> statements"),
        ("Expression", "Expr expression"),
        ("Function", "Token name, List<Token> params, List<Stmt> body"),
        ("If", "Expr condition, Stmt thenBranch, Stmt elseBranch"),
        ("Print", "Expr expression"),
        ("Return", "Token keyword, Expr value"),
        ("Var", "Token name, Expr initializer"),
        ("While", "Expr condition, Stmt body"),
    ]
    define_ast(output_dir, "Stmt", stmt_types)

    return 0


if __name__ == "__main__":
    sys.exit(main())
