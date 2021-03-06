# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Project Phase Version",
    "version": "11.0.1.2.0",
    "category": "Project",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "project_version",
        "project_phase",
    ],
    "data": [
        "views/project_project_view.xml",
        "views/project_phase_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
    "auto_install": True,
}
