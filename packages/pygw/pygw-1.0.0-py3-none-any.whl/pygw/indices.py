from pygw.config import GeoWaveConfiguration
from pygw.base_models import Index

class SpatialIndex(Index):
    """Geotools SpatialIndex."""
    def __init__(self):
        j_spatial_idx_builder = GeoWaveConfiguration().GEOWAVE_PKG.core.geotime.ingest.SpatialDimensionalityTypeProvider.SpatialIndexBuilder()
        j_idx = j_spatial_idx_builder.createIndex()
        super().__init__(j_idx)

    def getName(self):
        return self._java_ref.getName()

class SpatialTemporalIndex(Index):
     """Geotools SpatialTemporalIndex"""
     def __init__(self):
        j_spat_temp_idx_builder = GeoWaveConfiguration().GEOWAVE_PKG.core.geotime.ingest.SpatialTemporalDimensionalityTypeProvider.SpatialTemporalIndexBuilder()
        j_idx = j_spat_temp_idx_builder.createIndex()
        super().__init__(j_idx)
