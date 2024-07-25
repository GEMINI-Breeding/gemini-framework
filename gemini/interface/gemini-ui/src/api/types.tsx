export type Experiment = {
    id: string;
    experiment_name: string;
    experiment_info: object;
    experiment_start_date: string;
    experiment_end_date: string;
};

export type Season = {
    id: string;
    season_name: string;
    season_info: object;
    season_start_date: string;
    season_end_date: string;
};

export type Site = {
    id: string;
    site_name: string;
    site_city: string;
    site_state: string;
    site_country: string;
    site_info: object;
};

export type Cultivar = {
    id: string;
    cultivar_accession: string;
    cultivar_population: string;
    cultivar_info: object;
};

export type Sensor = {
    id: string;
    sensor_name: string;
    sensor_info: object;
    sensor_platform_id: number;
    sensor_type_id: number;
    sensor_data_type_id: number;
    sensor_data_format_id: number;
};

export type SensorPlatform = {
    id: string;
    sensor_platform_name: string;
    sensor_platform_info: object;
};

export type Trait = {
    id: string;
    trait_name: string;
    trait_info: object;
    trait_metrics: object;
    trait_level_id: number;
};

export type Plot = {
    id: string;
    plot_id: string;
    plot_number: number;
    plot_row_number: number;
    plot_column_number: number;
    plot_geometry_info: object;
    plot_info: object;
    experiment_name: string;
    season_name: string;
    site_name: string;
};

export type Resource = {
    id: string;
    resource_uri: string;
    resource_file_name: string;
    is_external: boolean;
    resource_info: object;
    resource_data_format_id: number;
    resource_experiment_id: number;
};

export type Model = {
    id: string;
    model_name: string;
    model_url: string;
    model_info: object;
};

export type Procedure = {
    id: string;
    procedure_name: string;
    procedure_info: object;
};

export type Script = {
    id: string;
    script_name: string;
    script_url: string;
    script_extension: string;
    script_info: object;
};

export type Dataset = {
    id: string;
    dataset_name: string;
    collection_date: string;
    dataset_info: object;
    dataset_type_id: number;
};

export type RecordBase = {
    timestamp: string;
    collection_date?: string;
    record_info?: object;
};

export type SensorRecord = RecordBase & {
    sensor_id: string;
    sensor_name: string;
    sensor_data: object;
};

export type DatasetRecord = RecordBase & {
    dataset_id: string;
    dataset_name: string;
    dataset_data: object;
};

export type TraitRecord = RecordBase & {
    trait_id: string;
    trait_name: string;
    trait_value: number;
};
