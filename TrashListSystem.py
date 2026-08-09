from typing import Dict
from pathlib import Path
import json

class TLSystem:

    @staticmethod
    def GetTrashListPath() -> Path:
        return Path("data/TrashList.json")

    @staticmethod
    def GetTrashes() -> Dict[str, str]:
        tlPath = TLSystem.GetTrashListPath()

        if not tlPath.exists():
            tlPath.open(mode="w")
            tlPath.write_text("{}")

        trashList = tlPath.read_text(encoding="utf-8")
        return dict(json.loads(trashList))

    @staticmethod
    def AddTrash(userID: int | str, reason: str) -> None:
        trashList = TLSystem.GetTrashes()
        userID = str(userID)

        if trashList.get(userID) is not None:
            return

        trashList[userID] = reason
        TLSystem.SendTrashListUpdate(
            trashList, f"{userID} added to trashlist due to {reason}"
        )

    @staticmethod
    def RemoveTrash(userID: int | str, reason: str) -> None:
        trashList = TLSystem.GetTrashes()
        userID = str(userID)

        if trashList.get(userID) is None:
            return

        trashList.pop(userID)
        TLSystem.SendTrashListUpdate(
            trashList, f"{userID} removed from trashlist due to {reason}"
        )

    @staticmethod
    def ClearTrashList() -> None:
        trashList = TLSystem.GetTrashes()
        trashList.clear()
        TLSystem.SendTrashListUpdate(
            trashList, "trashlist cleared"
        )

    @staticmethod
    def UpdateTrashList(trashList: Dict[str, str]) -> None:
        tlPath = TLSystem.GetTrashListPath()

        tlPath.write_text(
            json.dumps(trashList, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    @staticmethod
    def SendTrashListUpdate(trashList: Dict[str, str], action: str) -> None:
        TLSystem.UpdateTrashList(trashList)
        changes = Path("data/TrashListChanges.txt")

        if not changes.exists():
            changes.open(mode="w").seek(0)

        changes = changes.open(mode="a+", encoding="utf-8")
        changes.write(action + "\n")