# VoiceCreator - VCR

import disnake
from typing import Dict
import json


class VoiceSystem:
    @staticmethod
    def GetVoiceCreators() -> Dict[str, str]:
        with open("data/VCModes.json", "r", encoding="utf-8") as f:
            return dict(json.load(f))


    @staticmethod
    def GetVoiceCreatorEmojis() -> Dict[str, str]:
        with open("data/VCEmojis.json", "r", encoding="utf-8") as f:
            return dict(json.load(f))


    @staticmethod
    def GetVoiceCreatorEmoji(channel: disnake.VoiceChannel) -> str:
        emojis, vcrs = VoiceSystem.GetVoiceCreatorEmojis(), VoiceSystem.GetVoiceCreators()
        vcrMode = vcrs[str(channel.id)]
        return emojis[vcrMode]


    @staticmethod
    def GetVoiceNumber(name: str, category: disnake.CategoryChannel) -> int:
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
    def IsVoiceCreatorExist(channel: disnake.VoiceChannel) -> bool:
        return str(channel.id) in VoiceSystem.GetVoiceCreators()


    @staticmethod
    def SetVoiceCratorMode(channel: disnake.VoiceChannel, mode: str):
        vcrs = VoiceSystem.GetVoiceCreators()
        vcrs[str(channel.id)] = mode

        with open("data/VCModes.json", "w", encoding="utf-8") as f:
            json.dump(vcrs, f, indent=4, ensure_ascii=False)