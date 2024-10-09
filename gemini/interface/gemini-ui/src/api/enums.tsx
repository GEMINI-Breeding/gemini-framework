export enum GEMINIDataTypes {
    Default = 0,
    Text = 1,
    Web = 2,
    Document = 3,
    Image = 4,
    Audio = 5,
    Video = 6,
    Binary = 7,
    Other = 8
}


export enum GEMINIDataFormats {
    Default = 0,
    TXT = 1,
    JSON = 2,
    CSV = 3,
    TSV = 4,
    XML = 5,
    HTML = 6,
    PDF = 7,
    JPEG = 8,
    PNG = 9,
    GIF = 10,
    BMP = 11,
    TIFF = 12,
    WAV = 13,
    MP3 = 14,
    MPEG = 15,
    AVI = 16,
    MP4 = 17,
    OGG = 18,
    WEBM = 19,
    NPY = 20
}

export enum GEMINIDataTypeFormats {
    Text = 1,
    Web = 6,
    Document = 7,
    Image = 8,
    Audio = 13,
    Video = 15,
    Other = 20
}

export enum GEMINITraitLevels {
    Default = 0,
    Plot = 1,
    Plant = 2
}

export enum GEMINISensorTypes {
    Default = 0,
    RGB = 1,
    NIR = 2,
    Thermal = 3,
    Multispectral = 4,
    Weather = 5,
    GPS = 6,
    Calibration = 7,
    Depth = 8
}

export enum GEMINIDatasetTypes {
    Default = 0,
    Sensor = 1,
    Trait = 2,
    Procedure = 3,
    Script = 4,
    Model = 5,
    Other = 6
}
