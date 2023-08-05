from scopeton import compat, glob, constants
from scopeton.scopeTools import ScopetonException


def Inject():
    def inject_decorator(fn):
        annotations_signature = compat.getMethodSignature(fn).annotations
        args_signature = compat.getMethodSignature(fn).args
        # TODO: add exception description
        def inject_wrapper(*args, **kwargs):
            scope = glob.lastScope
            nkwargs = {}
            nargs = [args[0]]
            for arg_name in args_signature:
                if arg_name == "self":
                    continue
                if arg_name not in annotations_signature:
                    raise ScopetonException("Not annotated inject argument: {}".format(arg_name))
                arg_type = annotations_signature[arg_name]
                arg_to_inject = scope.getInstance(arg_type)
                nargs.append(arg_to_inject)

            return fn(*nargs, **nkwargs)

        setattr(inject_wrapper, constants.INJECT_FLAG, 1)
        return inject_wrapper

    return inject_decorator
