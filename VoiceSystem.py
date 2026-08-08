# VoiceCreator - VCR
from sys import prefix

from disnake import CategoryChannel
from typing import Dict
import json


class VCSystem:
    @staticmethod
    def GetVCRs() -> Dict[str, str]:
        with open("data/VCModes.json", "r", encoding="utf-8") as f:
            return dict(json.load(f))


    @staticmethod
    def GetVCREmojis() -> Dict[str, str]:
        with open("data/VCEmojis.json", "r", encoding="utf-8") as f:
            return dict(json.load(f))


    @staticmethod
    def GetVCREmoji(channelID: int | str):
        emojis, vcrs = VCSystem.GetVCREmojis(), VCSystem.GetVCRs()
        vcrMode = vcrs[str(channelID)]
        return emojis[vcrMode]


    @staticmethod
    def GetVoiceNumber(name: str, category: CategoryChannel):
        used = set()
        channelPrefix = f"{name} - "

        for channel in category.channels:
            if not channel.name.startswith(channelPrefix):
                continue

            try:
                numPart = int(channel.name[len(channelPrefix)])
                used.add(numPart)
            except (ValueError, TypeError):
                continue

        if len(used) == 0 or 1 not in used:
            return 1

        num = 1
        while num in used:
            num += 1

        return num


    @staticmethod
    def IsVCRExists(channelID: int | str) -> bool:
        return str(channelID) in VCSystem.GetVCRs()


    @staticmethod
    def SetVCRMode(channelID: int | str, mode: str):
        vcrs = VCSystem.GetVCRs()
        vcrs[str(channelID)] = mode

        with open("data/VCModes.json", "w", encoding="utf-8") as f:
            json.dump(vcrs, f, ensure_ascii=False, indent=4)