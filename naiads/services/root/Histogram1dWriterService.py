# coding=utf-8

import json
from array import *
from time import strftime

from ROOT import TH1F

from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType, Mimetype


class Histogram1dWriterService(Engine):

    def get_author(self):
        return "Ricardo Oyarzun <oyarzun@jlab.org>"

    def get_description(self):
        return "1D Histogram writer service, writes a ROOT file with Histogram"

    def get_states(self):
        pass

    def get_output_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def execute(self, engine_data):

        if engine_data.mimetype == Mimetype.STRING:
            json_object = json.loads(engine_data.get_data())

            limits = self._get_limits(json_object["xAxis"]["centers"])
            histo_name = json_object["annotation"]["Title"]

            histo = TH1F("histogram", histo_name, 100, limits[0], limits[1])
            histo.SetContent(self._convert_to_root_array(json_object["counts"]))
            histo.SetError(self._convert_to_root_array(json_object["errors"]))

            histo.SaveAs(self._create_filename(histo_name))
            return histo

        return None

    def execute_group(self, inputs):
        pass

    def reset(self):
        pass

    def destroy(self):
        pass

    def get_version(self):
        return "v1.0"

    def get_input_data_types(self):
        return ClaraUtils.build_data_types(EngineDataType.STRING())

    def configure(self, engine_data):
        pass

    def _convert_to_root_array(self, list_array):
        return array('d', list_array)

    def _create_filename(self, hname):
        timestamp_str = strftime("%Y%m%d%H%M%S")
        return hname + "_" + timestamp_str + ".root"

    def _get_limits(self, list_array):
        return [float(list_array[0]), float(list_array[-1])]