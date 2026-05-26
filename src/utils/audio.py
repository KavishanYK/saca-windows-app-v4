"""
Shared audio playback utilities for SACA.
All pages import _play / _play_sequence / stop_all from here so there is
a single active-player list and stop_all() can silence everything at once.
"""
from __future__ import annotations

import os

from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


def _audio_path(filename: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(
        os.path.join(base, "..", "..", "assets", "audio", filename)
    )


# Shared list of every in-flight QMediaPlayer instance
_active: list[QMediaPlayer] = []


def stop_all() -> None:
    """Stop and discard every currently playing audio player."""
    for p in list(_active):
        try:
            p.stop()
        except Exception:
            pass
    _active.clear()


def play(filename: str) -> None:
    """Fire-and-forget single-file playback."""
    path = _audio_path(filename)
    if not os.path.exists(path):
        return
    player = QMediaPlayer()
    audio_out = QAudioOutput()
    audio_out.setVolume(1.0)
    player.setAudioOutput(audio_out)
    player.setSource(QUrl.fromLocalFile(path))
    player._audio_out = audio_out
    _active.append(player)

    def _on_status(status: QMediaPlayer.MediaStatus, p=player):
        if status == QMediaPlayer.EndOfMedia:
            if p in _active:
                _active.remove(p)

    player.mediaStatusChanged.connect(_on_status)
    player.play()


def play_sequence(filenames: list[str], on_complete=None) -> None:
    """Play files one after another; call on_complete when the last one ends."""
    if not filenames:
        if on_complete:
            on_complete()
        return
    first, *rest = filenames
    path = _audio_path(first)
    if not os.path.exists(path):
        play_sequence(rest, on_complete)   # skip missing, keep going
        return
    player = QMediaPlayer()
    audio_out = QAudioOutput()
    audio_out.setVolume(1.0)
    player.setAudioOutput(audio_out)
    player.setSource(QUrl.fromLocalFile(path))
    player._audio_out = audio_out
    _active.append(player)

    def _on_status(status: QMediaPlayer.MediaStatus, p=player):
        if status == QMediaPlayer.EndOfMedia:
            if p in _active:
                _active.remove(p)
            play_sequence(rest, on_complete)

    player.mediaStatusChanged.connect(_on_status)
    player.play()
