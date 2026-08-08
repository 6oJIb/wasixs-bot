# VoiceCreator - VCR

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
        num = 1
        for ch in category.channels:
            try: chNum = int(ch.name.split(" - ")[1])
            except ValueError: continue

            if ch.name.startswith(name) and num <= chNum:
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