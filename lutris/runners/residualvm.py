# -*- coding: utf-8 -*-
import os
import subprocess

from lutris import settings
from lutris.runners.runner import Runner

RESIDUALVM_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".residualvmrc")


class residualvm(Runner):
    """Runs various 3D point-and-click adventure games, like Grim Fandango and Escape from Monkey Island."""
    human_name = "ResidualVM"
    platform = "3D point-and-click games"
    game_options = [
        {
            'option': 'game_id',
            'type': 'string',
            'label': "Game identifier"
        },
        {
            'option': 'path',
            'type': 'directory_chooser',
            'label': "Game files location"
        },
        {
            "option": "subtitles",
            "label": "Enable subtitles (if the game has voice)",
            "type": "bool"
        }
    ]
    runner_options = [
        {
            "option": "windowed",
            "label": "Windowed mode",
            "type": "bool"
        },
        {
            "option": "soft-renderer",
            "label": "Software renderer",
            "type": "bool"
        },
        {
            "option": "show-fps",
            "label": "Display FPS information",
            "type": "bool"
        }
    ]

    tarballs = {
        'i386': "residualvm-0.2.1-linux32.tar.gz",
        'x64': "residualvm-0.2.1-linux64.tar.gz",
    }

    @property
    def game_path(self):
        return self.game_config.get('path')

    def get_executable(self):
        return os.path.join(settings.RUNNER_DIR, 'ResidualVM/ResidualVM')

    def get_residualvm_data_dir(self):
        root_dir = os.path.dirname(self.get_executable())
        return os.path.join(root_dir, 'data')

    def play(self):
        command = [
            self.get_executable(),
            "--extrapath=\"%s\"" % self.get_residualvm_data_dir(),
            "--themepath=\"%s\"" % self.get_residualvm_data_dir(),
        ]

        # Options

        if self.game_config.get("subtitles"):
            command.append("--subtitles")

        if self.runner_config.get("windowed"):
            command.append("--no-fullscreen")
        else:
            command.append("--fullscreen")

        if self.runner_config.get("soft-renderer"):
            command.append("--soft-renderer")
        else:
            command.append("--no-soft-renderer")

        if self.runner_config.get("show-fps"):
            command.append("--show-fps")
        else:
            command.append("--no-show-fps")
        # /Options

        command.append("--path=\"%s\"" % self.game_path)
        command.append(self.game_config.get('game_id'))

        launch_info = {'command': command}

        return launch_info

    def get_game_list(self):
        """ Return the entire list of games supported by ResidualVM """
        residual_output = subprocess.Popen(
            [self.get_executable(), "--list-games"], stdout=subprocess.PIPE
        ).communicate()[0]
        game_list = str.split(residual_output, "\n")
        game_array = []
        game_list_start = False
        for game in game_list:
            if game_list_start:
                if len(game) > 1:
                    dir_limit = game.index(" ")
                else:
                    dir_limit = None
                if dir_limit is not None:
                    game_dir = game[0:dir_limit]
                    game_name = game[dir_limit + 1:len(game)].strip()
                    game_array.append([game_dir, game_name])
            # The actual list is below a separator
            if game.startswith("-----"):
                game_list_start = True
        return game_array
