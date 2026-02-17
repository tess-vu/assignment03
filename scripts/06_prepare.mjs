/**
 * Stretch challenge: Prepare merged hourly + site location data.
 *
 * This script joins the hourly observation data with site location data
 * during the prepare step (denormalization), producing files where
 * each observation row includes the site's latitude, longitude, and
 * other geographic metadata.
 *
 * This is the alternative to the approach in Part 4, where hourly data
 * and site locations were kept as separate tables and joined at query
 * time in BigQuery.
 *
 * This is a backfill of the prepare step — you're re-processing the
 * same raw data you already downloaded, but with a different
 * transformation that produces a richer output.
 *
 * Usage:
 *     node scripts/06_prepare.mjs
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '..', 'data');

/**
 * Merge hourly observations with site locations and write as CSV.
 *
 * Reads the hourly .dat files for the given date and the site locations
 * file, joins them on AQSID, and writes to
 * data/prepared/hourly_with_sites/<date>.csv.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 */
async function prepareMergedCsv(dateStr) {
  throw new Error('Implement this function.');
}

/**
 * Merge hourly observations with site locations and write as JSON-L.
 *
 * Reads the hourly .dat files for the given date and the site locations
 * file, joins them on AQSID, and writes to
 * data/prepared/hourly_with_sites/<date>.jsonl.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 */
async function prepareMergedJsonl(dateStr) {
  throw new Error('Implement this function.');
}

/**
 * Merge hourly observations with site locations and write as GeoParquet.
 *
 * Reads the hourly .dat files for the given date and the site locations
 * file, joins them on AQSID, creates point geometries from the site's
 * latitude and longitude, and writes to
 * data/prepared/hourly_with_sites/<date>.geoparquet.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 */
async function prepareMergedGeoparquet(dateStr) {
  throw new Error('Implement this function.');
}

// Backfill: prepare merged data for each day in July 2024
const startDate = new Date('2024-07-01');
const endDate = new Date('2024-07-31');

let currentDate = startDate;
while (currentDate <= endDate) {
  const dateStr = currentDate.toISOString().split('T')[0];
  console.log(`Preparing merged data for ${dateStr}...`);
  await prepareMergedCsv(dateStr);
  await prepareMergedJsonl(dateStr);
  await prepareMergedGeoparquet(dateStr);
  currentDate.setDate(currentDate.getDate() + 1);
}

console.log('Done.');
