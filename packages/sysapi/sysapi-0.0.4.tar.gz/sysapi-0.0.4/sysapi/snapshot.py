from typing import List, Optional
from pydantic import BaseModel, FilePath

class SnapshotModel(BaseModel):
    name: str
    # path: FilePath = None
    # TODO: For early dev, deactivate path testing
    path: str


## TODO: Move this to unit tests...
test_snapshots = [ ]

for snap in ['@initial', '@first', '@second', '@current']:
    test_snapshots.append(SnapshotModel(name=snap, path='/zpool/shared/filesystem'+snap ))



def get_snapshots() -> List[str]:
    return [s.name for s in test_snapshots]

def get_snapshot(snapshot: str)-> Optional[SnapshotModel]:
    return next((s for s in test_snapshots if s.name == snapshot), None)