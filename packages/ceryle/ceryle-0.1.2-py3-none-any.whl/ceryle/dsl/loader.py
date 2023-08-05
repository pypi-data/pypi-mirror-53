import ast
import ceryle
import ceryle.util as util
import os

from ceryle import Command, Copy, Remove
from ceryle.commands.executable import executable
from ceryle.dsl.parser import parse_tasks
from . import support


class TaskFileLoader:
    def __init__(self, task_file):
        self._task_file = util.assert_type(task_file, str)

    def load(self, global_vars={}, local_vars={}):
        module = util.parse_to_ast(self._task_file)

        body = module.body
        if len(body) == 0:
            return TaskDefinition([], None)

        gvars, lvars = self._prepare_vars(global_vars, local_vars)
        task_node = body[-1]
        if not isinstance(task_node, ast.Expr) or not isinstance(task_node.value, ast.Dict):
            self._eval_task_file(body, gvars, lvars)
            return TaskDefinition([], lvars.get('default'), gvars, lvars)
        else:
            self._eval_task_file(body[:-1], gvars, lvars)
            tasks = eval(compile(ast.Expression(task_node.value), self._task_file, 'eval'), gvars, lvars)
            # print(dir(task_node.value))
            # assignment = ast.Assign(
            #     [ast.Name('_ceryle_tasks',
            #               ast.Store(),
            #               lineno=task_node.lineno,
            #               col_offset=task_node.col_offset)],
            #     task_node.value,
            #     lineno=task_node.lineno,
            #     col_offset=task_node.col_offset + 16)
            # exec(compile(
            #     ast.Module(
            #         [assignment]),
            #     self._task_file,
            #     'exec'),
            #     gvars, lvars)
            # tasks = lvars.pop('_ceryle_tasks')
            context = self._resolve_context(lvars.get('context'))
            return TaskDefinition(parse_tasks(tasks, context), lvars.get('default'), gvars, lvars)

    def _eval_task_file(self, body, gvars, lvars):
        co = compile(ast.Module(body), self._task_file, 'exec')
        exec(co, gvars, lvars)

    def _prepare_vars(self, global_vars, local_vars):
        gvars = global_vars.copy()
        gvars.update(
            ceryle=ceryle,
        )
        lvars = local_vars.copy()
        lvars.update(
            command=Command,
            copy=Copy,
            remove=Remove,
            executable=executable,
            path=support.joinpath,
        )
        return gvars, lvars

    def _resolve_context(self, context):
        if not context:
            return os.path.dirname(os.path.abspath(self._task_file))
        if os.path.isabs(context):
            return context
        return os.path.abspath(os.path.join(os.path.dirname(self._task_file), context))


class TaskDefinition:
    def __init__(self, tasks, default_task=None, global_vars={}, local_vars={}):
        self._tasks = tasks.copy()
        self._default = default_task
        self._globals = global_vars.copy()
        self._locals = local_vars.copy()

    @property
    def tasks(self):
        return self._tasks.copy()

    @property
    def default_task(self):
        return self._default

    @property
    def global_vars(self):
        return self._globals.copy()

    @property
    def local_vars(self):
        return self._locals.copy()

    def find_task_group(self, name):
        util.assert_type(name, str)
        for g in self._tasks:
            if g.name == name:
                return g
        return None
