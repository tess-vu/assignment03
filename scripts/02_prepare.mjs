/**
 * Script to transform raw AirNow data files into BigQuery-compatible formats.
 *
 * This script reads the raw .dat files downloaded by 01_extract.mjs and converts
 * them into CSV, JSON-L, and Parquet formats suitable for loading into
 * BigQuery as external tables.
 *
 * Hourly observation data is converted to: CSV, JSON-L, Parquet
 * Site location data is converted to: CSV, JSON-L, GeoParquet (with point geometry)
 *
 * Usage:
 *     node scripts/02_prepare.mjs
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '..', 'data');

const HOURLY_COLUMNS = [
  'valid_date',
  'valid_time',
  'aqsid',
  'site_name',
  'gmt_offset',
  'parameter_name',
  'reporting_units',
  'value',
  'data_source',
];


// --- Hourly observation data ---

/**
 * Convert raw hourly .dat files for a date to a single CSV file.
 *
 * Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
 * combines them into a single dataset, assigns column names,
 * and writes to data/prepared/hourly/<date>.csv.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 */
async function prepareHourlyCsv(dateStr) {
  throw new Error('Implement this function.');
}

/**
 * Convert raw hourly .dat files for a date to newline-delimited JSON.
 *
 * Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
 * combines them, and writes one JSON object per line to
 * data/prepared/hourly/<date>.jsonl.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 */
async function prepareHourlyJsonl(dateStr) {
  throw new Error('Implement this function.');
}

/**
 * Convert raw hourly .dat files for a date to Parquet format.
 *
 * Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
 * combines them, and writes to data/prepared/hourly/<date>.parquet.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 */
async function prepareHourlyParquet(dateStr) {
  throw new Error('Implement this function.');
}


// --- Site location data ---

/**
 * Convert monitoring site locations to CSV.
 *
 * Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
 * so there is one row per site (the raw file has one row per
 * site-parameter combination), and writes to
 * data/prepared/sites/site_locations.csv.
 *
 * Uses the most recent date's file from data/raw/.
 */
async function prepareSiteLocationsCsv() {
  throw new Error('Implement this function.');
}

/**
 * Convert monitoring site locations to newline-delimited JSON.
 *
 * Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
 * so there is one row per site (the raw file has one row per
 * site-parameter combination), and writes to
 * data/prepared/sites/site_locations.jsonl.
 *
 * Uses the most recent date's file from data/raw/.
 */
async function prepareSiteLocationsJsonl() {
  throw new Error('Implement this function.');
}

/**
 * Convert monitoring site locations to GeoParquet with point geometry.
 *
 * Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
 * so there is one row per site (the raw file has one row per
 * site-parameter combination), creates point geometries from
 * latitude and longitude, and writes to
 * data/prepared/sites/site_locations.geoparquet.
 *
 * Uses the most recent date's file from data/raw/.
 */
async function prepareSiteLocationsGeoparquet() {
  throw new Error('Implement this function.');
}


// Prepare site locations (only need to do this once)
console.log('Preparing site locations...');
await prepareSiteLocationsCsv();
await prepareSiteLocationsJsonl();
await prepareSiteLocationsGeoparquet();

// Prepare hourly data for each day in July 2024 (backfill)
const startDate = new Date('2024-07-01');
const endDate = new Date('2024-07-31');

let currentDate = startDate;
while (currentDate <= endDate) {
  const dateStr = currentDate.toISOString().split('T')[0];
  console.log(`Preparing hourly data for ${dateStr}...`);
  await prepareHourlyCsv(dateStr);
  await prepareHourlyJsonl(dateStr);
  await prepareHourlyParquet(dateStr);
  currentDate.setDate(currentDate.getDate() + 1);
}

console.log('Done.');
