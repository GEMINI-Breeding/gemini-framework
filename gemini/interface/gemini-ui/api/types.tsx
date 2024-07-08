export type Experiment = {
    id: string;
    experiment_name: string;
    experiment_start_date: Date;
    experiment_end_date: Date;
    experiment_info: object;
}

export type Season = {
    id: string;
    season_name: string;
    season_start_date: Date;
    season_end_date: Date;
    season_info: object;
}

export type Site = {
    id: string;
    site_name: string;
    site_city: string;
    site_country: string;
    site_info: object;
}

export type Cultivar = {
    id: string;
    cultivar_population: string;
    cultivar_accession: string;
    cultivar_info: object;
}

export type Plot = {
    id: string;
    plot_number: number;
    plot_row_number: number;
    plot_column_number: number;
    plot_info: object;
    plot_geometry_info: object;
    experiment_id: string;
    season_id: string;
    site_id: string;
    experiment: Experiment;
    season: Season;
    site: Site;
}

export type Trait = {
    id: string;
    trait_name: string;
    trait_units: string;
    trait_level_id: number;
    trait_metrics: object;
    trait_info: object;
}

export type SensorPlatform = {
    id: string;
    sensor_platform_name: string;
    sensor_platform_info: object;
}

export type Sensor = {
    id: string;
    sensor_name: string;
    sensor_type_id: number;
    sensor_data_type_id: number;
    sensor_data_format_id: number;
}


export type Resource = {
    id: string;
    resource_uri: string;
    resource_file_name: string;
    is_external: boolean;
    resource_info: object;
    resource_data_format_id: number;
    resource_experiment_id: string;
}

export type Model = {
    id: string;
    model_name: string;
    model_url: string;
    model_info: object;
}

export type Procedure = {
    id: string;
    procedure_name: string;
    procedure_info: object;
}

export type Script = {
    id: string;
    script_name: string;
    script_url: string;
    script_extension: string;
    script_info: object;
}

export type Dataset = {
    id: string;
    collection_date: Date;
    dataset_name: string;
    dataset_info: object;
    dataset_type_id: number;
}

export type RecordBase = {
    id: string;
    timestamp: Date;
    collection_date: Date;
    record_info: object;
}

export type DatasetRecord = RecordBase & {
    dataset_id: string;
    dataset_name: string;
    dataset_data: object;
}

export type SensorRecord = RecordBase & {
    sensor_id: string;
    sensor_name: string;
    sensor_data: object;
}

export type TraitRecord = RecordBase & {
    trait_id: string;
    trait_name: string;
    trait_value: number;
}

export type JobInfo = {
    key: string;
    function: string;
    queue: string;
    progress: number;
    attempts: number;
    status: string;
    process_ms: number;
    start_ms: number;
    total_ms: number;
    result: any;
    error: string;
    meta: object;
}

