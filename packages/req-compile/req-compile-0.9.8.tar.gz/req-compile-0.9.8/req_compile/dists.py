from __future__ import print_function

import collections
import copy
import itertools
import logging

import six

from req_compile import utils
from req_compile.utils import normalize_project_name, merge_requirements, filter_req, reduce_requirements


class DependencyNode(object):
    def __init__(self, key, req_name, metadata, extra=None):
        """

        Args:
            key:
            req_name:
            metadata (RequirementContainer):
            extra:
        """
        self.key = key
        self.metadata = metadata
        self.req_name = req_name
        self.extra = extra
        self.dependencies = {}  # Dict[DependencyNode, pkg_resources.Requirement]
        self.reverse_deps = set()  # Set[DependencyNode]
        self.repo = None

    def __repr__(self):
        return self.key

    def __str__(self):
        if self.metadata is None:
            return self.key + ' [UNSOLVED]'
        if self.metadata.meta:
            return self.metadata.name
        return '=='.join(str(x) for x in self.metadata.to_definition(
            (self.extra,)
            if self.extra else None))

    def build_constraints(self):
        req = None
        for node in self.reverse_deps:
            if self in node.dependencies:
                req = merge_requirements(req, node.dependencies[self])

        if req is None:
            if self.metadata is None:
                req = utils.parse_requirement(self.key)
            else:
                req = utils.parse_requirement(self.metadata.name)
            if self.extra:
                req.extras = (self.extra,)
                # Reparse to create a correct hash
                req = utils.parse_requirement(str(req))
        return req


def _build_constraints(root_node, exclude=None):
    constraints = []
    for node in root_node.reverse_deps:
        if node.req_name != exclude:
            req = node.dependencies[root_node]
            specifics = ' (' + str(req.specifier) + ')' if req.specifier else ''
            source = node.metadata.name + ('[' + node.extra + ']' if node.extra else '')
            constraints += [source + specifics]
    return constraints


class DistributionCollection(object):
    def __init__(self):
        self.nodes = {}  # Dict[str, DependencyNode]
        self.logger = logging.getLogger('req_compile.dists')

    @staticmethod
    def _build_key(name, extra=None):
        return utils.normalize_project_name(name) + (('[' + extra + ']') if extra else '')

    def add_dist(self, metadata, source, reason):  # pylint: disable=too-many-branches
        """
        Add a distribution

        Args:
            metadata (RequirementContainer|str): Distribution info to add
            source (DependencyNode, optional): The source of the distribution
            reason (pkg_resources.Requirement, optional):
        """
        self.logger.debug('Adding dist: %s %s %s', metadata, source, reason)

        if reason is not None and len(reason.extras) > 1:
            self.logger.debug('There reason this dist as included had extras')
            result = None
            for extra in reason.extras:
                new_req = copy.copy(reason)
                new_req.extras = (extra,)
                result = self.add_dist(metadata, source, new_req)
            return result

        has_metadata = False
        if isinstance(metadata, six.string_types):
            req_name = metadata
        else:
            has_metadata = True
            req_name = metadata.name

        extra = reason.extras[0] if reason is not None and reason.extras else None
        key = DistributionCollection._build_key(req_name, extra)

        if key in self.nodes:
            node = self.nodes[key]
        else:
            node = DependencyNode(key, req_name, None, extra)
            self.nodes[key] = node

        if extra:
            # Add a reference back to the root req
            base_node = self.add_base(node, reason, req_name)
        else:
            base_node = node

        nodes = {base_node}
        if has_metadata:
            self.update_dists(base_node, metadata)

            # Apply the same metadata to all extras
            for reverse_node in base_node.reverse_deps:
                if utils.normalize_project_name(reverse_node.req_name) == utils.normalize_project_name(req_name):
                    self.update_dists(reverse_node, metadata)
                    nodes.add(reverse_node)

        self._discard_metadata_if_necessary(base_node, reason, req_name)

        if source is not None and source.key in self.nodes:
            node.reverse_deps.add(source)
            source.dependencies[node] = reason

        if base_node.key not in self.nodes:
            raise ValueError('The node {} is gone, while adding'.format(base_node.key))

        return nodes if has_metadata else set()

    def _discard_metadata_if_necessary(self, base_node, reason, req_name):
        if base_node.metadata is not None and not base_node.metadata.meta and reason is not None:
            if not reason.specifier.contains(base_node.metadata.version,
                                             prereleases=True):
                self.logger.debug('Existing solution (%s) invalidated by %s', base_node.metadata, reason)
                # Discard the metadata
                self.remove_dists(base_node, remove_upstream=False)

                for reverse_node in base_node.reverse_deps:
                    if reverse_node.req_name == req_name:
                        self.remove_dists(reverse_node, remove_upstream=False)

    def add_base(self, node, reason, req_name):
        if reason is not None:
            non_extra_req = copy.copy(reason)
            non_extra_req.extras = ()
            non_extra_req = utils.parse_requirement(str(non_extra_req))
        else:
            non_extra_req = utils.parse_requirement(req_name)

        self.add_dist(req_name, node, non_extra_req)
        return self[req_name]

    def update_dists(self, node, metadata):
        node.metadata = metadata
        for req in metadata.requires(node.extra):
            # This adds a placeholder entry
            self.add_dist(req.name, node, req)

    def remove_dists(self, node, remove_upstream=True):
        self.logger.debug('Removing dist(s): %s (upstream = %s)', node, remove_upstream)

        if isinstance(node, collections.Iterable):
            for single_node in node:
                self.remove_dists(single_node)
            return

        if node.key not in self.nodes:
            return

        if remove_upstream:
            del self.nodes[node.key]
            for reverse_dep in node.reverse_deps:
                del reverse_dep.dependencies[node]

        for dep in node.dependencies:
            if remove_upstream or dep.req_name != node.req_name:
                dep.reverse_deps.remove(node)
                if not dep.reverse_deps:
                    self.remove_dists(dep)

        if not remove_upstream:
            node.dependencies = {}
            node.metadata = None

    def build(self, roots):
        results = self.generate_lines(roots)
        return [utils.parse_requirement('=='.join([result[0][0], str(result[0][1])])) for result in results]

    def visit_nodes(self, roots, max_depth=None, reverse=False, _visited=None, _cur_depth=0):
        if _visited is None:
            _visited = set()

        if reverse:
            next_nodes = itertools.chain(*[root.reverse_deps for root in roots])
        else:
            next_nodes = itertools.chain(*[root.dependencies.keys() for root in roots])
        for node in next_nodes:
            if node in _visited:
                continue

            yield node
            _visited.add(node)

            if max_depth is None or _cur_depth < max_depth - 1:
                results = self.visit_nodes([node], reverse=reverse, max_depth=max_depth,
                                           _visited=_visited, _cur_depth=_cur_depth + 1)
                for result in results:
                    yield result

    def generate_lines(self, roots, req_filter=None, _visited=None):
        """
        Generate the lines of a results file from this collection
        Args:
            roots (iterable[DependencyNode]): List of roots to generate lines from
            req_filter (Callable): Filter to apply to each element of the collection.
                Return True to keep a node, False to exclude it
            _visited (set): Internal set to make sure each node is only visited once
        Returns:
            (list[str]) List of rendered node entries in the form of
                reqname==version   # reasons
        """
        if _visited is None:
            _visited = set()
        req_filter = req_filter or (lambda _: True)

        results = []
        for node in itertools.chain(*[root.dependencies.keys() for root in roots]):
            if node in _visited:
                continue

            _visited.add(node)

            if isinstance(node.metadata, DistInfo) and not node.extra:
                extras = []
                constraints = _build_constraints(node, exclude=node.metadata.name)
                for reverse_dep in node.reverse_deps:
                    if reverse_dep.metadata.name == node.metadata.name:
                        if reverse_dep.extra is None:
                            # print('Reverse dep with none extra: {}'.format(reverse_dep))
                            pass
                        else:
                            extras.append(reverse_dep.extra)
                        constraints.extend(_build_constraints(reverse_dep))

                req_expr = node.metadata.to_definition(extras)
                constraint_text = ', '.join(sorted(constraints))
                if not node.metadata.meta and req_filter(node):
                    results.append((req_expr, constraint_text))

            results.extend(self.generate_lines([node], req_filter=req_filter, _visited=_visited))

        return results

    def __contains__(self, project_name):
        return normalize_project_name(project_name) in self.nodes

    def __iter__(self):
        return iter(self.nodes.values())

    def __getitem__(self, project_name):
        return self.nodes[normalize_project_name(project_name)]


class RequirementContainer(object):
    """A container for a list of requirements"""
    def __init__(self, name, reqs, meta=False):
        self.name = name
        self.reqs = list(reqs)
        self.origin = None
        self.meta = meta

    def requires(self, extra=None):
        return reduce_requirements(req for req in self.reqs
                                   if filter_req(req, extra))

    def to_definition(self, extras):
        raise NotImplementedError()


class RequirementsFile(RequirementContainer):
    def __init__(self, filename, reqs):
        super(RequirementsFile, self).__init__(filename, reqs, meta=True)

    def __repr__(self):
        return 'RequirementsFile({})'.format(self.name)

    @staticmethod
    def from_file(full_path):
        reqs = utils.reqs_from_files([full_path])
        return RequirementsFile(full_path, reqs)

    def __str__(self):
        return self.name

    def to_definition(self, extras):
        return self.name, None


class DistInfo(RequirementContainer):
    """Metadata describing a distribution of a project"""

    def __init__(self, name, version, reqs, meta=False):
        """
        Args:
            name (str): The project name
            version (pkg_resources.Version): Parsed version of the project
            reqs (Iterable): The list of requirements for the project
            meta (bool): Whether or not hte requirement is a meta-requirement
        """
        super(DistInfo, self).__init__(name, reqs, meta=meta)
        self.version = version
        self.source = None

    def __str__(self):
        return '{}=={}'.format(*self.to_definition(None))

    def to_definition(self, extras):
        req_expr = '{}{}'.format(
            self.name,
            ('[' + ','.join(sorted(extras)) + ']') if extras else '')
        return req_expr, self.version

    def __repr__(self):
        return self.name + ' ' + str(self.version) + '\n' + '\n'.join([str(req) for req in self.reqs])
