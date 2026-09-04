from typing import Dict
from pathlib import Path
import disnake
import json

class PunishedSystem:

    @staticmethod
    def GetPunishedListPath() -> Path:
        return Path("data/TrashList.json")

    @staticmethod
    def GetPunished() -> Dict[str, str]:
        tlPath = PunishedSystem.GetPunishedListPath()

        if not tlPath.exists():
            tlPath.open(mode="w")
            tlPath.write_text("{}")

        trashList = tlPath.read_text(encoding="utf-8")
        return dict(json.loads(trashList))

    @staticmethod
    def AddPunished(member: disnake.Member, reason: str) -> None:
        trashList = PunishedSystem.GetPunished()
        userID = str(member.id)

        if trashList.get(userID) is not None:
            return

        trashList[userID] = reason
        PunishedSystem.PunishedListUpdate(
            trashList, f"{userID} added to trashlist due to {reason}"
        )

    @staticmethod
    def RemovePunished(member: disnake.Member, reason: str) -> None:
        trashList = PunishedSystem.GetPunished()
        userID = str(member.id)

        if trashList.get(userID) is None:
            return

        trashList.pop(userID)
        PunishedSystem.PunishedListUpdate(
            trashList, f"{userID} removed from trashlist due to {reason}"
        )

    @staticmethod
    def ClearPunishedList() -> None:
        trashList = PunishedSystem.GetPunished()
        trashList.clear()
        PunishedSystem.PunishedListUpdate(
            trashList, "trashlist cleared"
        )

    @staticmethod
    def UpdatePunishedList(trashList: Dict[str, str]) -> None:
        tlPath = PunishedSystem.GetPunishedListPath()

        tlPath.write_text(
            json.dumps(trashList, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    @staticmethod
    def PunishedListUpdate(trashList: Dict[str, str], action: str) -> None:
        PunishedSystem.UpdatePunishedList(trashList)
        changes = Path("data/TrashListChanges.txt")

        if not changes.exists():
            changes.open(mode="w").seek(0)

        changes = changes.open(mode="a+", encoding="utf-8")
        changes.write(action + "\n")