# -*- coding:Utf-8 -*-
###############################################################################
## Lutris
##
## Copyright (C) 2009 Mathieu Comandon strycore@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import os
import subprocess
from runner import Runner


class mednafen(Runner):
    def __init__(self,settings=None):
        self.executable = "mednafen"
        self.machine = """Atari Lynx, GameBoy (Color), GameBoy Advance, NES, PC Engine(TurboGrafx 16), SuperGrafx, Neo Geo Pocket (Color), PC-FX, and WonderSwan (Color)"""
        self.description = """Use Mednafen"""
        self.package = "mednafen"
        machine_choices = [("NES","nes"),
                           ("PC Engine","pce"),
                           ("Game Boy Advance","gba")]
        self.game_options = [{"option": "rom", "type":"single","label":"Rom file"},
        {"option":"machine","type":"one_choice","label":"Machine type","choices": machine_choices }]
        self.runner_options = [{"option":"fs","type":"bool","label":"Fullscreen"}]

        if settings:
            #self.romdir = settings["path"]
            self.rom = settings["game"]["rom"]
            self.machine = settings["game"]["machine"]
            #Defaults
            fullscreen = "1"
            xres = str(1680)
            yres = str(1050)
            if "mednafen" in settings.config:
                if "fs" in settings.config["mednafen"]:
                    if not settings.config["mednafen"]["fs"]:
                        fullscreen = "0"

            self.options = ["-fs",fullscreen,
                            "-"+self.machine+".xres",xres,"-"+self.machine+".yres",yres,
                            "-"+self.machine+".stretch","1","-"+self.machine+".special","hq4x",
                            "-"+self.machine+".videoip","1"]


    def find_joysticks(self):
        output = subprocess.Popen(["mednafen","dummy"],stdout=subprocess.PIPE).communicate()[0]
        ouput = str.split(output,"\n")
        found = False
        joy_list = []
        for line in ouput:
            if found and "Joystick" in line:
                joy_list.append(line)
            else:
                found = False
            if "Initializing joysticks" in line:
                found = True

        for joy in joy_list:
            index = joy.find("Unique ID:")
            self.joy_ids.append(joy[index+11:])


    def play(self):
        self.joy_ids = []
        self.find_joysticks()
        nes_controls = ["-nes.input.port1.gamepad.a","\"joystick "+self.joy_ids[0]+" 00000001\"",
                             "-nes.input.port1.gamepad.b","\"joystick "+self.joy_ids[0]+" 00000002\"",
                             "-nes.input.port1.gamepad.start","\"joystick "+self.joy_ids[0]+" 00000009\"",
                             "-nes.input.port1.gamepad.select","\"joystick "+self.joy_ids[0]+" 00000008\"",
                             "-nes.input.port1.gamepad.up","\"joystick "+self.joy_ids[0]+" 0000c001\"",
                             "-nes.input.port1.gamepad.down","\"joystick "+self.joy_ids[0]+" 00008001\"",
                             "-nes.input.port1.gamepad.left","\"joystick "+self.joy_ids[0]+" 0000c000\"",
                             "-nes.input.port1.gamepad.right","\"joystick "+self.joy_ids[0]+" 00008000\""
                            ]
        gba_controls = ["-gba.input.port1.gamepad.a","\"joystick "+self.joy_ids[0]+" 00000001\"",
                             "-gba.input.port1.gamepad.b","\"joystick "+self.joy_ids[0]+" 00000002\"",
                             "-gba.input.port1.gamepad.start","\"joystick "+self.joy_ids[0]+" 00000009\"",
                             "-gba.input.port1.gamepad.select","\"joystick "+self.joy_ids[0]+" 00000008\"",
                             "-gba.input.port1.gamepad.up","\"joystick "+self.joy_ids[0]+" 0000c001\"",
                             "-gba.input.port1.gamepad.down","\"joystick "+self.joy_ids[0]+" 00008001\"",
                             "-gba.input.port1.gamepad.left","\"joystick "+self.joy_ids[0]+" 0000c000\"",
                             "-gba.input.port1.gamepad.right","\"joystick "+self.joy_ids[0]+" 00008000\""
                            ]

        pce_controls = ["-pce.input.port1.gamepad.i","\"joystick "+self.joy_ids[0]+" 00000001\"",
                        "-pce.input.port1.gamepad.ii","\"joystick "+self.joy_ids[0]+" 00000002\"",
                        "-pce.input.port1.gamepad.run","\"joystick "+self.joy_ids[0]+" 00000009\"",
                        "-pce.input.port1.gamepad.select","\"joystick "+self.joy_ids[0]+" 00000008\"",
                        "-pce.input.port1.gamepad.up","\"joystick "+self.joy_ids[0]+" 0000c001\"",
                        "-pce.input.port1.gamepad.down","\"joystick "+self.joy_ids[0]+" 00008001\"",
                        "-pce.input.port1.gamepad.left","\"joystick "+self.joy_ids[0]+" 0000c000\"",
                        "-pce.input.port1.gamepad.right","\"joystick "+self.joy_ids[0]+" 00008000\""
                       ]

        if self.machine == "pce":
            controls = pce_controls
        elif self.machine == "nes":
            controls = nes_controls
        elif self.machine == "gba":
            controls = gba_controls
        else:
            controls = []
        for control in controls:
            self.options.append(control)

        #os.chdir(self.romdir)
        command = [self.executable]
        for option in self.options:
            command.append(option)
        command.append("\""+self.rom+"\"")
        return command