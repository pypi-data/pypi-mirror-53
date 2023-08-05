# -*- coding: utf-8 -*-
# @author: Federico Cerchiari <federicocerchiari@gmail.com>
"""Main Tempy classes"""
from html import escape
from collections import deque, Iterable
from copy import copy
from functools import wraps
from numbers import Number

from .exceptions import (
    TagError,
    WrongContentError,
    WrongArgsError,
    DOMModByKeyError,
    DOMModByIndexError,
)
from .tempyrepr import REPRFinder
import inspect


class DOMNavigator:
    @property
    def root(self):
        return self.parent.root if self.parent else self

    def _find_content(self, cont_name):
        """Search for a content_name in the content data, if not found the parent is searched."""
        try:
            a = self.content_data[cont_name]
            return a
        except KeyError:
            if self.parent:
                return self.parent._find_content(cont_name)
            else:
                # Fallback for no content (Raise NoContent?)
                return ""

    def _get_non_tempy_contents(self):
        """Returns rendered Contents and non-DOMElement stuff inside this Tag."""
        for thing in filter(
            lambda x: not issubclass(x.__class__, DOMElement), self.childs
        ):
            yield thing

    def find(self, selector=None, names=None):
        """
        @param:
            selector => css selector / given as list (returns matching elements)
                        or TempyClass name (returns instances of this class)
            names => returns attributes of elements with given name
        """
        if selector is None and names is None:
            found_elements = self.childs[:]
            for child in self.childs:
                if issubclass(child.__class__, DOMElement) and len(child.childs) > 0:
                    found_elements += child.find(selector, names)
            return found_elements

        found_elements_selector = []
        if selector is not None and inspect.isclass(selector):
            for child in self.childs:
                if isinstance(child, selector):
                    found_elements_selector.append(child)
                if issubclass(child.__class__, DOMElement) and len(child.childs) > 0:
                    found_elements_selector += child.find(selector, names)

        elif selector is not None and isinstance(selector, str):
            for child in self.childs:
                if (
                    inspect.isclass(child) and selector == child.__name__
                ) or selector == child.__class__.__name__:
                    found_elements_selector.append(child)
                if issubclass(child.__class__, DOMElement) and len(child.childs) > 0:
                    found_elements_selector += child.find(selector, names)

        found_elements_names = []
        if names is not None:
            for child in self.childs:
                if hasattr(child, "_name") and names == child._name:
                    found_elements_names.append(child)
                if issubclass(child.__class__, DOMElement) and len(child.childs) > 0:
                    found_elements_names += child.find(selector, names)

        if selector is not None and names is not None:
            set_selector = set(found_elements_selector)
            set_names = set(found_elements_names)
            found_elements = list(set_selector.intersection(set_names))
        else:
            found_elements = (
                found_elements_selector
                if selector is not None
                else found_elements_names
            )

        return found_elements

    def children(self):
        """Returns Tags and Content Placehorlders childs of this element."""
        return filter(lambda x: isinstance(x, DOMElement), self.childs)

    def contents(self):
        """Returns this elements childs list, unfiltered."""
        return self.childs

    def first(self):
        """Returns the first child"""
        return self.childs[0]

    def last(self):
        """Returns the last child"""
        return self.childs[-1]

    def next(self):
        """Returns the next sibling."""
        return self.parent.childs[self._own_index + 1]

    def next_all(self):
        """Returns all the next siblings as a list."""
        return self.parent.childs[self._own_index + 1:]

    def prev(self):
        """Returns the previous sibling."""
        return self.parent.childs[self._own_index - 1]

    def prev_all(self):
        """Returns all the previous siblings as a list."""
        return self.parent.childs[: self._own_index]

    def siblings(self):
        """Returns all the siblings of this element as a list."""
        return list(filter(lambda x: id(x) != id(self), self.parent.childs))

    def get_parent(self):
        """Returns this element's father"""
        return self.parent

    def slice(self, start=None, end=None, step=None):
        """Slice of this element's childs as childs[start:end:step]"""
        return self.childs[start:end:step]

    def bft(self):
        """ Generator that returns each element of the tree in Breadth-first order"""
        queue = deque([self])
        while queue:
            node = queue.pop()
            yield node
            if hasattr(node, "childs"):
                queue.extendleft(node.childs)

    def dfs_preorder(self, reverse=False):
        """Generator that returns each element of the tree in Preorder order.
        Keyword arguments:
        reverse -- if true, the search is done from right to left."""
        stack = deque()
        stack.append(self)
        while stack:
            node = stack.pop()
            yield node
            if hasattr(node, "childs"):
                if reverse:
                    stack.extend(node.childs)
                else:
                    stack.extend(node.childs[::-1])

    def dfs_inorder(self, reverse=False):
        """Generator that returns each element of the tree in Inorder order.
        Keyword arguments:
        reverse -- if true, the search is done from right to left."""
        stack = deque()
        visited = set()
        visited.add(self)
        if reverse:
            stack.append(self.childs[0])
            stack.append(self)
            stack.extend(self.childs[1:])
        else:
            stack.extend(self.childs[1:])
            stack.append(self)
            stack.append(self.childs[0])
        while stack:
            node = stack.pop()
            if node in visited or not node.childs:
                yield node
            else:
                stack.append(node)
                visited.add(node)
                if hasattr(node, "childs"):
                    if reverse:
                        stack.extend(node.childs)
                    else:
                        stack.extend(node.childs[::-1])

    def dfs_postorder(self, reverse=False):
        """Generator that returns each element of the tree in Postorder order.
        Keyword arguments:
        reverse -- if true, the search is done from right to left."""
        stack = deque()
        stack.append(self)
        visited = set()
        while stack:
            node = stack.pop()
            if node in visited:
                yield node
            else:
                visited.add(node)
                stack.append(node)
                if hasattr(node, "childs"):
                    if reverse:
                        stack.extend(node.childs)
                    else:
                        stack.extend(node.childs[::-1])


class DOMModifier:
    def content_receiver(reverse=False):
        """Decorator for content adding methods.
        Takes args and kwargs and calls the decorated method one time for each argument provided.
        The reverse parameter should be used for prepending (relative to self) methods.
        """

        def _receiver(func):
            @wraps(func)
            def wrapped(inst, *tags, **kwtags):
                verse = (1, -1)[int(reverse)]
                kwtags = kwtags.items()
                i = 0
                for typ in (tags, kwtags)[::verse]:
                    for item in typ:
                        if typ is kwtags:
                            name, item = item
                        else:
                            name, item = None, item
                        if isinstance(item, DOMElement) and name:
                            # Is the DOMGroup is a single DOMElement and we have a name we set his name accordingly
                            item._name = name
                        inst._stable = False
                        func(inst, i, item, name)
                        i += 1
                return inst

            return wrapped

        return _receiver

    def _insert(self, dom_group, idx=None, prepend=False, name=None):
        """Inserts a DOMGroup inside this element.
        If provided at the given index, if prepend at the start of the childs list, by default at the end.
        If the child is a DOMElement, correctly links the child.
        If the DOMGroup have a name, an attribute containing the child is created in this instance.
        """
        if idx and idx < 0:
            idx = 0
        if prepend:
            idx = 0
        else:
            idx = idx if idx is not None else len(self.childs)
        if dom_group is not None:
            if not isinstance(dom_group, Iterable) or isinstance(
                dom_group, (DOMElement, str)
            ):
                dom_group = [dom_group]
            for i_group, elem in enumerate(dom_group):
                if elem is not None:
                    # Element insertion in this DOMElement childs
                    self.childs.insert(idx + i_group, elem)
                    # Managing child attributes if needed
                    if issubclass(elem.__class__, DOMElement):
                        elem.parent = self
                    if name:
                        setattr(self, name, elem)

    @content_receiver()
    def __call__(self, _, child, name=None):
        """Calling the object will add the given parameters as childs"""
        self._insert(child, name=name)

    def __add__(self, other):
        """Addition produces a copy of the left operator, containig the right operator as a child."""
        return self.clone()(other)

    def __iadd__(self, other):
        """In-place addition adds the right operand as left's child"""
        return self(other)

    def __sub__(self, other):
        """Subtraction produces a copy of the left operator, with the right operator removed from left.childs."""
        if other not in self:
            raise ValueError("%s is not in %s" % (other, self))
        ret = self.clone()
        ret.pop(other._own_index)
        return ret

    def __isub__(self, other):
        """removes the child."""
        if other not in self:
            raise ValueError("%s is not in %s" % (other, self))
        return self.pop(other._own_index)

    def __mul__(self, n):
        """Returns a list of clones."""
        if not isinstance(n, int):
            raise TypeError
        if n < 0:
            raise ValueError("Negative multiplication not permitted.")
        return [self.clone() for i in range(n)]

    def __imul__(self, n):
        """Clones the element n times."""
        if not self.parent:
            return self * n
        if n == 0:
            self.parent.pop(self._own_index)
            return self
        return self.after(self * (n - 1))

    @content_receiver()
    def after(self, i, sibling, name=None):
        """Adds siblings after the current tag."""
        self.parent._insert(sibling, idx=self._own_index + 1 + i, name=name)
        return self

    @content_receiver(reverse=True)
    def before(self, i, sibling, name=None):
        """Adds siblings before the current tag."""
        self.parent._insert(sibling, idx=self._own_index - i, name=name)
        return self

    @content_receiver(reverse=True)
    def prepend(self, _, child, name=None):
        """Adds childs to this tag, starting from the first position."""
        self._insert(child, prepend=True, name=name)
        return self

    def prepend_to(self, father):
        """Adds this tag to a father, at the beginning."""
        father.prepend(self)
        return self

    @content_receiver()
    def append(self, _, child, name=None):
        """Adds childs to this tag, after the current existing childs."""
        self._insert(child, name=name)
        return self

    def append_to(self, father):
        """Adds this tag to a parent, after the current existing childs."""
        father.append(self)
        return self

    def wrap(self, other):
        """Wraps this element inside another empty tag."""
        if other.childs:
            raise TagError(self, "Wrapping in a non empty Tag is forbidden.")
        if self.parent:
            self.before(other)
            self.parent.pop(self._own_index)
        other.append(self)
        return self

    def wrap_many(self, *args, strict=False):
        """Wraps different copies of this element inside all empty tags
        listed in params or param's (non-empty) iterators.

        Returns list of copies of this element wrapped inside args
        or None if not succeeded, in the same order and same structure,
        i.e. args = (Div(), (Div())) -> value = (A(...), (A(...)))

        If on some args it must raise TagError, it will only if strict is True,
        otherwise it will do nothing with them and return Nones on their positions"""

        for arg in args:
            is_elem = arg and isinstance(arg, DOMElement)
            is_elem_iter = (
                not is_elem and arg and isinstance(arg, Iterable) and isinstance(iter(arg).__next__(), DOMElement)
            )
            if not (is_elem or is_elem_iter):
                raise WrongArgsError(
                    self,
                    "Argument {} is not DOMElement nor iterable of DOMElements".format(
                        arg
                    ),
                )

        wcopies = []
        failure = []

        def wrap_next(tag, idx):
            nonlocal wcopies, failure
            next_copy = self.__copy__()
            try:
                return next_copy.wrap(tag)
            except TagError:
                failure.append(idx)
                return next_copy

        for arg_idx, arg in enumerate(args):
            if isinstance(arg, DOMElement):
                wcopies.append(wrap_next(arg, (arg_idx, -1)))
            else:
                iter_wcopies = []
                for iter_idx, t in enumerate(arg):
                    iter_wcopies.append(wrap_next(t, (arg_idx, iter_idx)))
                wcopies.append(type(arg)(iter_wcopies))

        if failure and strict:
            raise TagError(
                self,
                "Wrapping in a non empty Tag is forbidden, failed on arguments " +
                ", ".join(
                    list(
                        map(
                            lambda idx: str(idx[0])
                            if idx[1] == -1
                            else "[{1}] of {0}".format(*idx),
                            failure,
                        )
                    )
                ),
            )
        return wcopies

    def wrap_inner(self, other):
        self.move_childs(other)
        self(other)
        return self

    def replace_with(self, other):
        """Replace this element with the given DOMElement."""
        self.after(other)
        self.parent.pop(self._own_index)
        return other

    def remove(self):
        """Detach this element from his father."""
        if self._own_index is not None and self.parent:
            self.parent.pop(self._own_index)
        return self

    def _detach_childs(self, idx_from=None, idx_to=None):
        """Moves all the childs to a new father"""
        idx_from = idx_from or 0
        idx_to = idx_to or len(self.childs)
        removed = self.childs[idx_from:idx_to]
        for child in removed:
            if issubclass(child.__class__, DOMElement):
                child.parent = None
        self.childs[idx_from:idx_to] = []
        return removed

    def move_childs(self, new_father, idx_from=None, idx_to=None):
        removed = self._detach_childs(idx_from=idx_from, idx_to=idx_to)
        new_father(removed)
        return self

    def move(self, new_father, idx=None, prepend=None, name=None):
        """Moves this element from his father to the given one."""
        self.parent.pop(self._own_index)
        new_father._insert(self, idx=idx, prepend=prepend, name=name)
        new_father._stable = False
        return self

    def pop(self, arg=None):
        """Removes the child at given position or by name (or name iterator).
            if no argument is given removes the last."""
        self._stable = False
        if arg is None:
            arg = len(self.childs) - 1
        if isinstance(arg, int):
            try:
                result = self.childs.pop(arg)
            except IndexError:
                raise DOMModByIndexError(self, "Given index invalid.")
            if isinstance(result, DOMElement):
                result.parent = None
        else:
            result = []
            if isinstance(arg, str):
                arg = [arg]
            for x in arg:
                try:
                    result.append(getattr(self, x))
                except AttributeError:
                    raise DOMModByKeyError(
                        self, "Given search key invalid. No child found."
                    )
            if result:
                for x in result:
                    self.childs.remove(x)
                    if isinstance(x, DOMElement):
                        x.parent = False
        return result

    def empty(self):
        """Remove all this tag's childs."""
        self._stable = False
        self._detach_childs()
        return self


class DOMElement(DOMNavigator, DOMModifier, REPRFinder):
    """Takes care of the tree structure using the "childs" and "parent" attributes.
    Manages the DOM manipulation with proper valorization of those two.
    """

    _from_factory = False

    def __init__(self, **kwargs):
        super().__init__()
        self._name = None
        self.childs = []
        if not getattr(self, 'parent', None):
            self.parent = None
        self.content_data = kwargs
        self._stable = True
        for cls in reversed(self.__class__.__mro__[:-6]):
            init = getattr(cls, "init", None)
            if init and init.__name__ in cls.__dict__:
                init(self)

    def __repr__(self):
        return "<%s.%s %s.%s%s%s>" % (
            self.__module__,
            type(self).__name__,
            id(self),
            " Son of %s." % type(self.parent).__name__ if self.parent else "",
            " %d childs." % len(self.childs) if self.childs else "",
            " Named %s" % self._name if self._name else "",
        )

    def __hash__(self):
        return id(self)

    def __bool__(self):
        # Is it normal that without explicit __bool__ definition
        # custom classes evaluates to False?
        return True

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        comp_dicts = [
            {
                "name": t._name,
                "childs": [id(c) for c in t.childs if isinstance(c, DOMElement)],
                "content_data": t.content_data,
            }
            for t in (self, other)
        ]
        return comp_dicts[0] == comp_dicts[1]

    def __getitem__(self, i):
        return self.childs[i]

    def __iter__(self):
        return iter(self.childs)

    def __next__(self):
        return next(iter(self.childs))

    def __reversed__(self):
        return iter(self.childs[::-1])

    def __contains__(self, x):
        return x in self.childs

    def __len__(self):
        return len(self.childs)

    def __copy__(self):
        return self.__class__()(
            copy(c) if isinstance(c, DOMElement) else c for c in self.childs
        )

    def to_code(self, pretty=False):
        ret = []
        prettying = "\n" + ("\t" * self._depth) if pretty else ""
        childs_to_code = []
        for child in self.childs:
            if issubclass(child.__class__, DOMElement):
                child_code = child.to_code(pretty=pretty)
                childs_to_code.append(child_code)
            else:
                childs_to_code.append('"""%s"""' % child)

        childs_code = ""
        if childs_to_code:
            childs_code = "(%s%s%s)" % (prettying, ", ".join(childs_to_code), prettying)
        class_code = ""
        if self._from_factory:
            class_code += "T."
            if getattr(self, "_void", False):
                class_code += "Void."
        class_code += self.__class__.__name__
        ret.append("%s(%s)%s" % (class_code, self.to_code_attrs(), childs_code))
        return "".join(ret)

    @property
    def _depth(self):
        return 0 if self.is_root else self.parent._depth + 1

    @property
    def is_root(self):
        return self.root == self

    @property
    def _own_index(self):
        if self.parent:
            try:
                return [id(t) for t in self.parent.childs].index(id(self))
            except ValueError:
                return -1
        return -1

    @property
    def index(self):
        """Returns the position of this element in the parent's childs list.
        If the element have no parent, returns None.
        """
        return self._own_index

    @property
    def stable(self):
        if all(c.stable for c in self.childs) and self._stable:
            self._stable = True
            return self._stable
        else:
            self._stable = False
            return self._stable

    @property
    def length(self):
        """Returns the number of childs."""
        return len(self.childs)

    @property
    def is_empty(self):
        """True if no childs"""
        return self.length == 0

    def _iter_child_renders(self, pretty=False):
        for child in self.childs:
            if isinstance(child, str):
                yield escape(child)
            elif isinstance(child, Number):
                yield str(child)
            elif issubclass(child.__class__, DOMElement):
                if isinstance(child, Escaped):
                    yield child._render
                else:
                    yield child.render(pretty=pretty)
            elif not issubclass(child.__class__, DOMElement):
                tempyREPR_cls = self._search_for_view(child)
                if tempyREPR_cls:
                    # If there is a TempyREPR class defined in the child class we make a DOMElement out of it
                    # this abomination is used to avoid circular imports
                    class Patched(tempyREPR_cls, DOMElement):
                        def __init__(s, obj, *args, **kwargs):
                            # Forced adoption of the patched element as son of us
                            s.parent = self
                            # MRO would init only the tempyREPR_cls, we force DOMElement init too
                            DOMElement.__init__(s, **kwargs)
                            super().__init__(obj)
                    yield Patched(child).render(pretty=pretty)
                else:
                    yield escape(str(child))

    def render(self, *args, **kwargs):
        """Placeholder for subclass implementation"""
        raise NotImplementedError

    def render_childs(self, pretty=False):
        """Public api to render all the childs using Tempy rules"""
        return "".join(self._iter_child_renders(pretty=pretty))

    def data(self, key=None, **kwargs):
        """Adds or retrieve extra data to this element, this data will not be rendered.
        Every tag have a _data attribute (dict), if key is given _data[key] is returned.
        Kwargs are used to udpate this Tag's _data."""
        self.content_data.update(kwargs)
        if key:
            return self.content_data[key]
        if not kwargs:
            return self.content_data
        return self

    def inject(self, contents=None, **kwargs):
        """
        Adds content data in this element. This will be used in the rendering of this element's childs.
        Multiple injections on the same key will override the content (dict.update behavior).
        """
        if contents and not isinstance(contents, dict):
            raise WrongContentError(self, contents, "contents should be a dict")
        self._stable = False
        if not contents:
            contents = {}
        if kwargs:
            contents.update(kwargs)
        self.content_data.update(contents)
        return self

    def clone(self):
        """Returns a deepcopy of this element."""
        return copy(self)


class Escaped(DOMElement):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self._render = content
