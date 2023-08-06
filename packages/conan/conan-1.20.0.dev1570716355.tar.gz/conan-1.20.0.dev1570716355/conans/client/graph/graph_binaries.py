import os

from conans.client.graph.graph import (BINARY_BUILD, BINARY_CACHE, BINARY_DOWNLOAD, BINARY_MISSING,
                                       BINARY_UPDATE, RECIPE_EDITABLE, BINARY_EDITABLE,
                                       RECIPE_CONSUMER, RECIPE_VIRTUAL, BINARY_SKIP)
from conans.errors import NoRemoteAvailable, NotFoundException, conanfile_exception_formatter
from conans.model.info import ConanInfo, PACKAGE_ID_UNKNOWN
from conans.model.manifest import FileTreeManifest
from conans.model.ref import PackageReference
from conans.util.files import is_dirty, rmdir


class GraphBinariesAnalyzer(object):

    def __init__(self, cache, output, remote_manager):
        self._cache = cache
        self._out = output
        self._remote_manager = remote_manager
        # These are the nodes with pref (not including PREV) that have been evaluated
        self._evaluated = {}  # {pref: [nodes]}

    @staticmethod
    def _check_update(upstream_manifest, package_folder, output, node):
        read_manifest = FileTreeManifest.load(package_folder)
        if upstream_manifest != read_manifest:
            if upstream_manifest.time > read_manifest.time:
                output.warn("Current package is older than remote upstream one")
                node.update_manifest = upstream_manifest
                return True
            else:
                output.warn("Current package is newer than remote upstream one")

    @staticmethod
    def _evaluate_build(node, build_mode):
        ref, conanfile = node.ref, node.conanfile
        with_deps_to_build = False
        # For cascade mode, we need to check also the "modified" status of the lockfile if exists
        # modified nodes have already been built, so they shouldn't be built again
        if build_mode.cascade and not (node.graph_lock_node and node.graph_lock_node.modified):
            for dep in node.dependencies:
                dep_node = dep.dst
                if (dep_node.binary == BINARY_BUILD or
                        (dep_node.graph_lock_node and dep_node.graph_lock_node.modified)):
                    with_deps_to_build = True
                    break
        if build_mode.forced(conanfile, ref, with_deps_to_build):
            conanfile.output.info('Forced build from source')
            node.binary = BINARY_BUILD
            node.prev = None
            return True

    def _evaluate_clean_pkg_folder_dirty(self, node, package_layout, package_folder, pref):
        # Check if dirty, to remove it
        with package_layout.package_lock(pref):
            assert node.recipe != RECIPE_EDITABLE, "Editable package shouldn't reach this code"
            if is_dirty(package_folder):
                node.conanfile.output.warn("Package is corrupted, removing folder: %s"
                                           % package_folder)
                rmdir(package_folder)  # Do not remove if it is EDITABLE
                return

            if self._cache.config.revisions_enabled:
                metadata = package_layout.load_metadata()
                rec_rev = metadata.packages[pref.id].recipe_revision
                if rec_rev and rec_rev != node.ref.revision:
                    node.conanfile.output.warn("The package {} doesn't belong to the installed "
                                               "recipe revision, removing folder".format(pref))
                    rmdir(package_folder)
                return metadata

    def _evaluate_cache_pkg(self, node, package_layout, pref, metadata, remote, remotes, update,
                            package_folder):
        if update:
            output = node.conanfile.output
            if remote:
                try:
                    tmp = self._remote_manager.get_package_manifest(pref, remote)
                    upstream_manifest, pref = tmp
                except NotFoundException:
                    output.warn("Can't update, no package in remote")
                except NoRemoteAvailable:
                    output.warn("Can't update, no remote defined")
                else:
                    if self._check_update(upstream_manifest, package_folder, output, node):
                        node.binary = BINARY_UPDATE
                        node.prev = pref.revision  # With revision
            elif remotes:
                pass  # Current behavior: no remote explicit or in metadata, do not update
            else:
                output.warn("Can't update, no remote defined")
        if not node.binary:
            node.binary = BINARY_CACHE
            metadata = metadata or package_layout.load_metadata()
            node.prev = metadata.packages[pref.id].revision
            assert node.prev, "PREV for %s is None: %s" % (str(pref), metadata.dumps())

    def _evaluate_remote_pkg(self, node, pref, remote, remotes, build_mode):
        remote_info = None
        if remote:
            try:
                remote_info, pref = self._remote_manager.get_package_info(pref, remote)
            except NotFoundException:
                pass
            except Exception:
                node.conanfile.output.error("Error downloading binary package: '{}'".format(pref))
                raise

        # If the "remote" came from the registry but the user didn't specified the -r, with
        # revisions iterate all remotes
        if not remote or (not remote_info and self._cache.config.revisions_enabled):
            for r in remotes.values():
                try:
                    remote_info, pref = self._remote_manager.get_package_info(pref, r)
                except NotFoundException:
                    pass
                else:
                    if remote_info:
                        remote = r
                        break

        if remote_info:
            node.binary = BINARY_DOWNLOAD
            node.prev = pref.revision
            recipe_hash = remote_info.recipe_hash
        else:
            recipe_hash = None
            if build_mode.allowed(node.conanfile):
                node.binary = BINARY_BUILD
            else:
                node.binary = BINARY_MISSING
            node.prev = None

        return recipe_hash, remote

    def _evaluate_is_cached(self, node, pref):
        previous_nodes = self._evaluated.get(pref)
        if previous_nodes:
            previous_nodes.append(node)
            previous_node = previous_nodes[0]
            # The previous node might have been skipped, but current one not necessarily
            # keep the original node.binary value (before being skipped), and if it will be
            # defined as SKIP again by self._handle_private(node) if it is really private
            if previous_node.binary == BINARY_SKIP:
                node.binary = previous_node.binary_non_skip
            else:
                node.binary = previous_node.binary
            node.binary_remote = previous_node.binary_remote
            node.prev = previous_node.prev
            return True
        self._evaluated[pref] = [node]

    def _evaluate_node(self, node, build_mode, update, remotes):
        assert node.binary is None, "Node.binary should be None"
        assert node.package_id is not None, "Node.package_id shouldn't be None"
        assert node.prev is None, "Node.prev should be None"

        if node.package_id == PACKAGE_ID_UNKNOWN:
            node.binary = BINARY_MISSING
            return

        ref, conanfile = node.ref, node.conanfile
        # If it has lock
        locked = node.graph_lock_node
        if locked and locked.pref.id == node.package_id:
            pref = locked.pref  # Keep the locked with PREV
        else:
            assert node.prev is None, "Non locked node shouldn't have PREV in evaluate_node"
            pref = PackageReference(ref, node.package_id)

        # Check that this same reference hasn't already been checked
        if self._evaluate_is_cached(node, pref):
            return

        if node.recipe == RECIPE_EDITABLE:
            node.binary = BINARY_EDITABLE  # TODO: PREV?
            return

        if self._evaluate_build(node, build_mode):
            return

        package_layout = self._cache.package_layout(pref.ref, short_paths=conanfile.short_paths)
        package_folder = package_layout.package(pref)
        metadata = self._evaluate_clean_pkg_folder_dirty(node, package_layout, package_folder, pref)

        remote = remotes.selected
        if not remote:
            # If the remote_name is not given, follow the binary remote, or the recipe remote
            # If it is defined it won't iterate (might change in conan2.0)
            metadata = metadata or package_layout.load_metadata()
            remote_name = metadata.packages[pref.id].remote or metadata.recipe.remote
            remote = remotes.get(remote_name)

        if os.path.exists(package_folder):  # Binary already in cache, check for updates
            self._evaluate_cache_pkg(node, package_layout, pref, metadata,  remote, remotes, update,
                                     package_folder)
            recipe_hash = None
        else:  # Binary does NOT exist locally
            # Returned remote might be different than the passed one if iterating remotes
            recipe_hash, remote = self._evaluate_remote_pkg(node, pref, remote, remotes, build_mode)

        if build_mode.outdated:
            if node.binary in (BINARY_CACHE, BINARY_DOWNLOAD, BINARY_UPDATE):
                if node.binary == BINARY_UPDATE:
                    info, pref = self._remote_manager.get_package_info(pref, remote)
                    recipe_hash = info.recipe_hash
                elif node.binary == BINARY_CACHE:
                    recipe_hash = ConanInfo.load_from_package(package_folder).recipe_hash

                local_recipe_hash = package_layout.recipe_manifest().summary_hash
                if local_recipe_hash != recipe_hash:
                    conanfile.output.info("Outdated package!")
                    node.binary = BINARY_BUILD
                    node.prev = None
                else:
                    conanfile.output.info("Package is up to date")

        node.binary_remote = remote

    @staticmethod
    def _compute_package_id(node, default_package_id_mode):
        conanfile = node.conanfile
        neighbors = node.neighbors()
        direct_reqs = []  # of PackageReference
        indirect_reqs = set()   # of PackageReference, avoid duplicates
        for neighbor in neighbors:
            ref, nconan = neighbor.ref, neighbor.conanfile
            direct_reqs.append(neighbor.pref)
            indirect_reqs.update(nconan.info.requires.refs())
            conanfile.options.propagate_downstream(ref, nconan.info.full_options)
            # Might be never used, but update original requirement, just in case
            conanfile.requires[ref.name].ref = ref

        # Make sure not duplicated
        indirect_reqs.difference_update(direct_reqs)
        # There might be options that are not upstream, backup them, might be
        # for build-requires
        conanfile.build_requires_options = conanfile.options.values
        conanfile.options.clear_unused(indirect_reqs.union(direct_reqs))
        conanfile.options.freeze()

        conanfile.info = ConanInfo.create(conanfile.settings.values,
                                          conanfile.options.values,
                                          direct_reqs,
                                          indirect_reqs,
                                          default_package_id_mode=default_package_id_mode)

        # Once we are done, call package_id() to narrow and change possible values
        with conanfile_exception_formatter(str(conanfile), "package_id"):
            conanfile.package_id()

        info = conanfile.info
        node.package_id = info.package_id()

    def evaluate_graph(self, deps_graph, build_mode, update, remotes, nodes_subset=None, root=None):
        default_package_id_mode = self._cache.config.default_package_id_mode
        for node in deps_graph.ordered_iterate(nodes_subset=nodes_subset):
            self._compute_package_id(node, default_package_id_mode)
            if node.recipe in (RECIPE_CONSUMER, RECIPE_VIRTUAL):
                continue
            self._evaluate_node(node, build_mode, update, remotes)
        deps_graph.private_skip_binaries(nodes_subset=nodes_subset, root=root)
