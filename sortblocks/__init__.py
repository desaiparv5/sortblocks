from pathlib import Path
from typing import Union
import ast as ast
import click


def sort_imports(cst_imports):
    output = []
    imports = []
    for cst_import in cst_imports:
        imports.extend(cst_import.names)

    imports.sort(key=lambda x: x.name)

    for cst_import in imports:
        cst_import = ast.Import(names=[cst_import], alias=None)
        output.append(cst_import)

    return output


def sort_import_from(ast_import_froms):
    output = []
    ast_import_froms.sort(key=lambda x: x.module)
    for ast_import_from in ast_import_froms:
        imports = ast_import_from.names
        imports.sort(key=lambda x: x.name)
        ast_import_from.names = imports
        output.append(ast_import_from)
    return output


def sort_ast_root(ast_root):

    imports = []
    import_froms = []
    function_defs = []
    class_defs = []
    others = []

    output = []

    for node in ast_root.body:
        if isinstance(node, ast.Import):
            imports.append(node)
        elif isinstance(node, ast.ImportFrom):
            import_froms.append(node)
        elif isinstance(node, ast.FunctionDef):
            function_defs.append(node)
        elif isinstance(node, ast.ClassDef):
            class_defs.append(node)
        else:
            others.append(node)

    output.extend(sort_imports(imports))
    output.extend(sort_import_from(import_froms))

    class_defs.sort(key=lambda x: x.name)
    for class_def in class_defs:
        output.append(sort_ast_root(class_def))

    function_defs.sort(key=lambda x: x.name)
    for function_def in function_defs:
        output.append(sort_ast_root(function_def))

    for other in others:
        output.append(other)

    ast_root.body = output
    return ast_root


def sort_blocks(file: Union[str, Path]):
    file = Path(file)
    with open(file) as f:
        parsed_file = ast.parse(f.read())

    return ast.unparse(sort_ast_root(parsed_file))


@click.command()
@click.argument('input', type=click.Path(exists=True), )
@click.option('-o', '--output', type=click.Path())
def main(input, output):

    out_str = sort_blocks(input)

    if output:
        with open(output, 'w') as f:
            f.write(out_str)
    else:
        print(out_str)


if __name__ == "__main__":
    main()
