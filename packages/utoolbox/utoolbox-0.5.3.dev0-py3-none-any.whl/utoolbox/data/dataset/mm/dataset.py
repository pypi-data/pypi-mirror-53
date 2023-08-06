import json
import logging
import os

import imageio

from utoolbox.data.datastore import (
    SparseVolumeDatastore,
    SparseTiledVolumeDatastore,
)
from ..base import MultiChannelDataset
from .error import NoMetadataInTileFolderError, NoSummarySectionError

logger = logging.getLogger(__name__)


class MicroManagerDataset(MultiChannelDataset):
    """
    Representation of Micro-Manager dataset stored in sparse stack format.

    Args:
        root (str): source directory of the dataset
        merge (bool, optional): return merged result for tiled dataset
        force_stack (bool, optional): force the dataset to be interpreted as stacks
    """

    def __init__(self, root, merge=True, force_stack=False):
        if not os.path.exists(root):
            raise FileNotFoundError("invalid dataset root")
        if merge and force_stack:
            logger.warning("force output as stack, merging request is ignored")
        self._tiled, self._force_stack = None, force_stack
        self._merge = merge
        super().__init__(root)

    def _load_metadata(self):
        meta_dir = self.root
        # select the first folder that contains `metadata.txt`
        for _path in os.listdir(self.root):
            _path = os.path.join(meta_dir, _path)
            if os.path.isdir(_path):
                meta_dir = _path
                break
        if meta_dir == self.root:
            raise NoMetadataInTileFolderError()
        logger.debug('using metadata from "{}"'.format(meta_dir))
        meta_path = os.path.join(meta_dir, "metadata.txt")

        with open(meta_path, "r") as fd:
            # discard frame specific info
            metadata = json.load(fd)["Summary"]

        # use 'InitialPositionList' to determine tiling config
        try:
            grids = metadata["InitialPositionList"]
            self._tiled = len(grids) > 1
        except (KeyError, TypeError):
            self._tiled = False
        if self._tiled:
            # extract tile shape
            tx, ty = -1, -1
            for grid in grids:
                if grid["GridColumnIndex"] > tx:
                    tx = grid["GridColumnIndex"]
                if grid["GridRowIndex"] > ty:
                    ty = grid["GridRowIndex"]
            self._tile_shape = (ty + 1, tx + 1)
            logger.info("dataset is a {} grid".format(self._tile_shape))

            # extract prefix without position info
            prefix = os.path.commonprefix([grid["Label"] for grid in grids])
            i = prefix.rfind("_")
            if i > 0:
                prefix = prefix[:i]
            logger.debug('folder prefix "{}"'.format(prefix))
            self._folder_prefix = prefix
        else:
            # shortcut to the actual data source
            self._root = meta_dir

        try:
            return metadata
        except KeyError:
            raise NoSummarySectionError()

    def _find_channels(self):
        return self.metadata["ChNames"]

    def _load_channel(self, channel):
        if self._tiled and not self._force_stack:
            return SparseTiledVolumeDatastore(
                self.root,
                read_func=imageio.imread,
                folder_pattern="{}*".format(self._folder_prefix),
                file_pattern="*_{}_*".format(channel),
                tile_shape=self._tile_shape,
                tile_order="F",
                merge=self._merge,
                extensions=['tif']
            )
        else:
            return SparseVolumeDatastore(
                self.root,
                read_func=imageio.imread,
                sub_dir=False,
                pattern="*_{}_*".format(channel),
                extensions=['tif']
            )

