from rest_framework.routers import SimpleRouter


class Router(SimpleRouter):

    def __init__(self, *args, **kwargs):
        super(Router, self).__init__(*args, **kwargs)

    def custom_register(self, viewset, prefix=None, basename=None, base_name=None, *args, **kwargs):
        path = getattr(viewset, 'path')  # s
        name = getattr(viewset, 'custom_name')  # pk
        detail_suffix = getattr(viewset, 'detail_suffix')
        basename = (basename or '') + "_" + path
        basename = basename.lstrip("_")
        prefix = prefix or path
        parent_prefix = kwargs.pop("parent_prefix", base_name) or prefix
        if not name or not path:
            raise AttributeError("viewset must have path attribute and name attribute")
        prefix = "{parent_prefix}/{prefix}".format(
            parent_prefix=parent_prefix,
            prefix=prefix
        )
        prefix = prefix.strip('/')
        if prefix == "%s/%s" % (path, path):
            prefix = path
        self.register(prefix=prefix, viewset=viewset, basename=basename, base_name=base_name)
        parent_prefix = "{parent_prefix}{variable_parent_name}/(?P<{parent_name_detail}>[^/.]+)".format(
            parent_prefix=parent_prefix,
            parent_name_detail=name + ("_%s" % detail_suffix if detail_suffix else ""),
            variable_parent_name="" if path == parent_prefix else "/" + path
        )
        for nested_viewset in viewset.nested_viewsets:
            path = getattr(nested_viewset, 'path', False)
            name = getattr(nested_viewset, 'custom_name', False)
            if not name or not path:
                raise AttributeError("viewset must have path attribute and name attribute")
            self.custom_register(prefix=path,
                                 viewset=nested_viewset,
                                 base_name=base_name,
                                 basename=basename,
                                 parent_prefix=parent_prefix)


router = Router()

