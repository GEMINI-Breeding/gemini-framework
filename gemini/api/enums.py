from enum import Enum

class GEMINIDataFormat(Enum):
  Default = 0
  TXT = 1
  JSON = 2
  CSV = 3
  TSV = 4
  XML = 5
  HTML = 6
  PDF = 7
  JPEG = 8
  PNG = 9
  GIF = 10
  BMP = 11
  TIFF = 12
  WAV = 13
  MP3 = 14
  MPEG = 15
  AVI = 16
  MP4 = 17
  OGG = 18
  WEBM = 19
  Other = 20

class GEMINISensorType(Enum):
  Default = 0
  RGB = 1
  NIR = 2
  Thermal = 3
  Multispectral = 4
  Weather = 5
  GPS = 6
  Calibration = 7
  Depth = 8

class GEMINIDatasetType(Enum):
  Default = 0
  Sensor = 1
  Trait = 2
  Script = 3
  Model = 4
  Procedure = 5
  Other = 6

class GEMINIDataType(Enum):
  Default = 0
  Text = 1
  Web = 2
  Document = 3
  Image = 4
  Audio = 5
  Video = 6
  Binary = 7
  Other = 8

class GEMINITraitLevel(Enum):
  Default = 0
  Plot = 1
  Plant = 2

