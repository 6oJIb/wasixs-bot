from typing import Dict
from pathlib import Path
import disnake
import json

class PunishedSystem:

    @staticmethod
    def GetPunishedListPath() -> Path:
        return Path("data/PunishedList.json")

    @staticmethod
    def GetPunished() -> Dict[str, str]:
        tlPath = PunishedSystem.GetPunishedListPath()

        if not tlPath.exists():
            tlPath.open(mode="w")
            tlPath.write_text("{}")

        punishedList = tlPath.read_text(encoding="utf-8")
        return dict(json.loads(punishedList))

    @staticmethod
    def AddPunished(member: disnake.Member, reason: str) -> None:
        punishedList = PunishedSystem.GetPunished()
        userID = str(member.id)

        if punishedList.get(userID) is not None:
            return

        punishedList[userID] = reason
        PunishedSystem.PunishedListUpdate(
            punishedList, f"{userID} added to punished list due to {reason}"
        )

    @staticmethod
    def RemovePunished(member: disnake.Member, reason: str) -> None:
        punishedList = PunishedSystem.GetPunished()
        userID = str(member.id)

        if punishedList.get(userID) is None:
            return

        punishedList.pop(userID)
        PunishedSystem.PunishedListUpdate(
            punishedList, f"{userID} removed from punished list due to {reason}"
        )

    @staticmethod
    def ClearPunishedList() -> None:
        punishedList = PunishedSystem.GetPunished()
        punishedList.clear()
        PunishedSystem.PunishedListUpdate(
            punishedList, "punished list cleared"
        )

    @staticmethod
    def UpdatePunishedList(punishedList: Dict[str, str]) -> None:
        tlPath = PunishedSystem.GetPunishedListPath()

        tlPath.write_text(
            json.dumps(punishedList, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    @staticmethod
    def PunishedListUpdate(punishedList: Dict[str, str], action: str) -> None:
        PunishedSystem.UpdatePunishedList(punishedList)
        changes = Path("data/PunishedListChanges.txt")

        if not changes.exists():
            changes.open(mode="w").seek(0)

        changes = changes.open(mode="a+", encoding="utf-8")
        changes.write(action + "\n")