import functools
import json


class DynTree(object):
    def __init__(self, v=None):
        if v:
            self.tree = v
        else:
            self.tree = dict()

    def get_deep(self, key):
        return self._get_deep(key, self.tree)

    def _get_deep(self, key, dict_):
        for k, v in dict_.items():
            if k == key:
                return v
            elif isinstance(v, dict):
                found = self._get_deep(key, v)
                if found is not None:
                    return found

    def set_deep(self, key, value, parent):
        ret = self._set_deep(key, value, parent, self.tree)
        if not ret and not self.tree.get(key):
            self.tree[key] = {'value': value, 'parent': parent, 'children': {}}
            ret = True
        return ret

    def _set_deep(self, key, value, parent, dict_):
        for k, v in dict_.items():
            if k == parent:
                if not isinstance(v, dict):
                    v = dict()
                    v['children'] = dict()
                v['children'][key] = {'value': value, 'parent': parent, 'children': {}}
                return True
            elif isinstance(v, dict):
                inserted = self._set_deep(key, value, parent, v)
                if inserted:
                    return inserted

    def insert(self, key, value, parent=None):
        if not parent:
            if not self.tree.get(key):
                self.tree[key] = {'value': value, 'parent': None, 'children': {}}
            else:
                raise Exception('overwriting already exist root node')
        else:
            self.set_deep(key, value, parent)

    def finalize(self):
        # rebuild tree
        to_del = list()
        for k, v in self.tree.items():
            if v.get('parent'):
                inserted = self.set_deep(k, v['value'], v['parent'])
                if inserted:
                    to_del.append(k)
        for d in to_del:
            del self.tree[d]

    def _traverse(self, dict_, index='', cmp=None):
        def tuple_to_cmp(tuple1, tuple2):
            return cmp(tuple1[1]['value'], tuple2[1]['value'])
        loop_index = 0
        for k, v in sorted(dict_.items(), key=functools.cmp_to_key(tuple_to_cmp), reverse=False):
            loop_index += 1
            if index:
                traverse_index = index + '.' + str(loop_index)
            else:
                traverse_index = str(loop_index)
            yield traverse_index, v['value']
            if v.get('children'):
                yield from self._traverse(v['children'], traverse_index, cmp=cmp)

    def items(self, cmp=None):
        if not cmp:
            def cmp_default(e1, e2):
                if e1 < e2:
                    return -1
                elif e1 > e2:
                    return 1
                else:
                    return 0
            cmp = cmp_default
        return [e for e in self._traverse(self.tree, cmp=cmp)]

    def __str__(self):
        return json.dumps(self.tree, indent=4)
