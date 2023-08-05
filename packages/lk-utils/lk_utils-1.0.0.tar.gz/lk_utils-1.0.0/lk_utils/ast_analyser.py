from _ast import *
from ast import parse as ast_parse, walk as ast_walk


class AstAnalyser:
    root = None
    
    def load(self, text: str):
        self.root = ast_parse(text)
    
    def lkdo(self):
        """
        made for lk_logger.
        """
        out = []
        for node in ast_walk(self.root):
            if hasattr(node, 'col_offset') and node.col_offset > 0:
                if isinstance(node, Str):
                    out.append('')
                elif isinstance(node, Name):
                    out.append(node.id)
                # TODO TEST
                # print(type(node), node.col_offset, self.eval_node(node))
        return out
    
    def get_ast_indents(self):
        """
        refer: {lkdemo}/ast_demo.py
        
        IN: self.file
            self.root
        OT: {lino: indent}
                lino: int. count from 1 but not consecutive. the linos are
                    already sorted by ascending order.
                indent: int. the column offset, assert all of them would be
                    integral multiple of 4, e.g. 0, 4, 8, 12, ... and no
                    exception.
        """
        lino_indent = {}
        
        for node in ast_walk(self.root):
            if not (hasattr(node, 'lineno') and hasattr(node, 'col_offset')):
                continue
            if node.lineno in lino_indent:
                continue
            if node.col_offset == -1:
                # 说明这个节点是 docstring
                continue
            lino_indent[node.lineno] = node.col_offset
        
        # sort linos
        sorted_lino_indent = {
            k: lino_indent[k]
            for k in sorted(lino_indent.keys())
        }
        
        return sorted_lino_indent
    
    def get_ast_tree(self):
        """
        IN: self.root
        OT: dict. {
                lino: [(node_type, node_value), (...), ...], ...
            }
                lino: int. count from 1 but not consecutive. the linos are
                    already sorted by ascending order.
                node_type: str. refer to _ast class types, e.g. "<class '_ast
                    .Import'>", "<class '_ast.FunctionDef'>", ...
                node_value: str/dict. e.g. 'os.path.abspath', {'os': 'os'}, ...
        """
        out = {}
        
        for node in ast_walk(self.root):
            if not hasattr(node, 'lineno'):
                continue
            x = out.setdefault(node.lineno, [])
            x.append((str(type(node)), self.eval_node(node)))
        
        # sort linos
        sorted_out = {
            k: out[k]
            for k in sorted(out.keys())
        }
        
        return sorted_out
    
    def eval_node(self, node):
        result = None
        
        while result is None:
            # lk.loga(type(node))
            # ------------------------------------------------ output result
            if isinstance(node, arg):
                """
                _fields = ('arg', 'annotation')
                    arg        -> str
                    annotation -> None / _ast.Name

                e.g. 1:
                    source_code = `def main(x, y):`
                    -> node.arg = 'x', node.annotation = None
                       node.arg = 'y', node.annotation = None

                e.g. 2:
                    source_code = `def main(self, x: dict):`
                    -> node.arg = 'self', node.annotation = None
                       node.arg = 'x', node.annotation = eval(node.annotation)
                       = 'dict'
                """
                # print('[arg fields]', node.arg, node.annotation)
                result = node.arg
                # | k, v = node.arg, node.annotation
                # | if v is not None:
                # |     v = self.eval_node(v)
                # | result = {k: v}
            elif isinstance(node, ClassDef):
                result = node.name
            elif isinstance(node, FunctionDef):
                result = node.name
            elif isinstance(node, Name):
                result = node.id
            elif isinstance(node, Str):
                result = node.s
            # ------------------------------------------------ compound obj
            elif isinstance(node, Assign):
                result = {}
                a, b = node.targets, node.value
                k = self.eval_node(b)
                for i in a:
                    v = self.eval_node(i)
                    result[v] = k
            elif isinstance(node, Attribute):
                """
                _fields = ('value', 'attr', 'ctx')
                    value -> _ast.Name / _ast.Attribute
                    attr  -> str
                    ctx   -> _ast.Load
                """
                # print('[Attribute fields]', node.value, node.attr, node.ctx)
                v = node.attr
                k = self.eval_node(node.value)
                result = k + '.' + v
                # | result = node.attr
            elif isinstance(node, Import):
                result = {}  # {module: import_name_or_asname}
                for imp in node.names:
                    if imp.asname is None:
                        result[imp.name] = imp.name
                    else:
                        result[imp.name] = imp.asname
            elif isinstance(node, ImportFrom):
                result = {}  # {module: import_name_or_asname}
                module = node.module
                for imp in node.names:
                    if imp.asname is None:
                        result[module + '.' + imp.name] = imp.name
                    else:
                        result[module + '.' + imp.name] = imp.asname
            # ------------------------------------------------ take reloop
            elif isinstance(node, Call):
                """
                _fields = ('func', 'args', 'keywords')
                    func     -> _ast.Attribute / _ast.Name
                    args     -> [] (empty list) / [_ast.Call]
                    keywords -> [] (empty list)
                """
                # print('[Call fields]', node.func, node.args, node.keywords)
                node = node.func
            elif isinstance(node, Expr):
                node = node.value
            elif isinstance(node, Subscript):
                node = node.value
            else:
                # noinspection PyProtectedMember
                result = str(node._fields)
        
        return result


def test():
    a = """lk.loga('头像宽高信息', crop_zone)"""
    
    # test_list = (
    #     "lk.loga('头像宽高信息', crop_zone)"
    #
    # )
    
    analyser = AstAnalyser()
    analyser.load(a)
    b = analyser.lkdo()
    print(f'b = {b}')


if __name__ == '__main__':
    test()
