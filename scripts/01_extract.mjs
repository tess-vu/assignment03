/**
 * Script to extract AirNow data files for a range of dates.
 *
 * This script downloads hourly air quality observation data and monitoring
 * site location data from the EPA's AirNow program. Files are saved into
 * a date-organized folder structure under data/raw/.
 *
 * AirNow files are hosted at:
 *     https://files.airnowtech.org/?prefix=airnow/
 *
 * Usage:
 *     node scripts/01_extract.mjs
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.resolve(__dirname, '..', 'data');

/**
 * Download AirNow data files for a single date.
 *
 * Downloads all 24 HourlyData files (hours 00-23) and the
 * Monitoring_Site_Locations_V2.dat file for the specified date,
 * saving them into data/raw/YYYY-MM-DD/.
 *
 * @param {string} dateStr - Date string in 'YYYY-MM-DD' format.
 *                           For example, '2024-07-01'.
 */
async function downloadDataForDate(dateStr) {
  throw new Error('Implement this function to download AirNow data files.');
}

// Download data for July 2024
const startDate = new Date('2024-07-01');
const endDate = new Date('2024-07-31');

let currentDate = startDate;
while (currentDate <= endDate) {
  const dateStr = currentDate.toISOString().split('T')[0];
  console.log(`Downloading data for ${dateStr}...`);
  await downloadDataForDate(dateStr);
  currentDate.setDate(currentDate.getDate() + 1);
}

console.log('Done.');
