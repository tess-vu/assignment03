# Assignment 03 — Motivation: Who Needs This Data, and Why?

In this class, we're building **cloud-based, data-centric products** — tools and systems whose primary purpose is to help someone make a decision using data. These decisions aren't one-time research questions. They're **recurring, operational decisions** — things that real people need to decide again and again, and where having current, well-organized data changes the action they take.

The data pipeline components you'll build in this assignment are the kind of behind-the-scenes infrastructure that powers the tools people use to make these decisions.

## The Data: EPA Air Quality Monitoring

The EPA and its partners operate a network of thousands of air quality monitors across the United States and Canada. These monitors continuously measure pollutants like PM2.5 (fine particulate matter), ozone, nitrogen dioxide, and carbon monoxide. The data is made available through two main systems:

- **[AirNow](https://www.airnow.gov/)** publishes **near-real-time** observations — hourly readings from monitoring sites updated throughout the day. The data is available as [bulk file downloads](https://files.airnowtech.org/) organized by date, as well as through a [web services API](https://docs.airnowapi.org/webservices).

- **[AQS (Air Quality System)](https://aqs.epa.gov/aqsweb/airdata/download_files.html)** publishes **quality-assured historical data** — daily, annual, and sample-level summaries going back decades. This data undergoes extensive QA/QC review and can take 6+ months after collection to appear. It's available as [bulk CSV downloads](https://aqs.epa.gov/aqsweb/airdata/download_files.html) and through a [query API](https://aqs.epa.gov/aqsweb/documents/data_api.html).

Both systems publish the same underlying monitoring data, but they serve different purposes and different audiences. That distinction matters — and it's one of the things you'll think about in this assignment.

### From raw files to data products

Raw data files on a government website are not a data _product_. They're a data _source_. To turn them into something actionable, someone has to:

1. **Extract** the data (download the files, parse their format)
2. **Load** it into a system where it can be queried and visualized (a cloud data warehouse like BigQuery)
3. **Transform** it into answers (via SQL queries, dashboards, and maps)

That's the EtLT pattern — and in this assignment, you'll practice the **E** and the **L**.

## Who makes decisions with this data?

Here are examples of real-world, recurring decisions that air quality data supports. Notice that none of these are one-time needs — they're all decisions that come up repeatedly, and the answer changes as the data changes.

### Everyday personal decisions

- **A parent deciding whether their asthmatic child should play outside today.** Like checking the weather to decide on an umbrella, they'd check an AQI dashboard before sending their kid to the park. Many parents of children with respiratory conditions do this daily.

- **A jogger or cyclist choosing their route.** Someone training regularly might check air quality along different corridors — avoiding the route near the refinery on a bad day and picking the waterfront trail instead. This decision recurs with every run.

- **A commuter deciding whether to bike or drive.** On high-AQI days, someone who usually bikes to work might choose to drive or take transit instead to reduce their exposure during heavy exertion.

### Organizational and professional decisions

- **A school administrator deciding whether to hold outdoor recess or PE.** Many school districts have formal AQI thresholds for moving activities indoors. Someone checks the data every morning during wildfire season or high-ozone summer days.

- **A construction site manager deciding what PPE workers need today.** OSHA has air quality thresholds that determine whether respirators are required. A foreman checks the readings each morning before assigning tasks.

- **A public health official deciding whether to issue an air quality advisory.** During wildfire season, county health departments review monitor data daily to decide: _do we send the push notification telling residents to stay indoors?_

### Planning and policy decisions

- **A real estate agent framing a neighborhood for a buyer.** Similar to how agents reference school ratings or walk scores, they might point out: "this block has consistently good air quality compared to the corridor near the highway interchange." This recurs with every showing, and the data shifts seasonally.

- **A school district facilities planner deciding where to site a new school.** They need to evaluate whether candidate sites are chronically exposed to poor air quality. This recurs with each new school siting process — and the data changes as pollution sources open, close, or change.

- **An environmental justice advocate prioritizing communities for outreach.** Organizations regularly check which neighborhoods consistently exceed AQI thresholds to guide door-knocking campaigns, grant applications, or regulatory complaints.

- **An urban planner evaluating a proposed zoning change.** Before approving a rezoning that would put housing near an industrial corridor, a planner might review historical air quality patterns at nearby monitors to assess exposure risk.

## Choosing the right data source

Not all of these decision-makers need the same data. A critical part of building a data product is choosing the right **source** for your use case.

The parent checking AQI before school needs **current, hourly data** — AirNow is the right source. The environmental justice advocate analyzing a decade of pollution trends needs **quality-assured historical data** — AQS is the right source. The real estate agent might be well-served by either, depending on whether they're showing current conditions or long-term patterns.

This is a design decision, not a technical one. The pipeline you build to serve each audience may use different sources, different update frequencies, and different storage strategies — even though all the data comes from the same physical monitors.

## Why build a pipeline instead of using an API directly?

Both AirNow and AQS offer APIs. If the data is already available through an API, why would you go through the trouble of downloading files and building your own pipeline?

This is an important question — and the answer touches on being a **responsible consumer of data services** and building systems that are **reliable and performant**.

### Not all APIs are built for the same purpose

Some APIs are designed to handle high-volume, production traffic — Google's Places API, Mapbox's geocoding service, or commercial weather APIs. These services are built to be called millions of times a day, and their business model depends on it.

Other APIs are designed for **analysts and researchers** making targeted queries, not for powering applications that serve many users. The AQS API falls squarely in this category:

- **Rate limited** — no more than 10 requests per minute, with a requested 5-second pause between requests
- **Row limits** — you're asked to limit queries to 1,000,000 rows each
- **Date range limits** — begin and end dates must fall within the same calendar year
- **Geographic scoping** — you query by site, county, state, or bounding box; there is no "give me everything nationwide" option

If you built a dashboard that called the AQS API every time a user loaded a page, you'd quickly hit rate limits — and you'd be putting unnecessary load on a public service that the EPA operates for free. Public APIs run on taxpayer-funded infrastructure, and hammering them with redundant requests takes resources away from other users.

### Some data sources don't have APIs at all

It's also worth noting that many important data sources are only available as file downloads. GTFS transit schedule data, for example, is published as a zip file — there's no API to query a transit agency's schedule. It would be impractical to re-download, unzip, and parse the full feed every time a user wants to check a bus departure. That's why transit apps ingest the data into their own systems.

The AirNow file products on `files.airnowtech.org` are similar — they're flat files on an S3 bucket, organized by date and hour. There's no API-style query interface for those files; you download them and work with them locally. That's exactly the kind of extraction work that data pipelines are built for.

### The pattern

A well-designed data product typically:

1. **Downloads the source data on a schedule** (hourly for AirNow, twice a year for AQS, etc.)
2. **Stores it in your own cloud storage** (so you control access and availability)
3. **Loads it into a data warehouse** (so you can run fast queries, join with other datasets, and serve many users without hitting anyone else's rate limits)

### When _would_ you use an API directly?

APIs are great for **exploratory work** and **one-off analyses** — for example, checking what PM2.5 data is available for a specific county before deciding whether to include it in your pipeline. They're also the right choice when you need a very small, targeted slice of data that doesn't justify downloading everything, or when you're using a high-capacity commercial API designed for production traffic.

The key principle is: **be a good steward of the data systems you consume.** Understand their intended use, respect their rate limits, and design your systems accordingly.

## The connection to this assignment

In this assignment, you'll work with AirNow's hourly monitoring data — the kind of near-real-time data that powers the everyday decisions described above. You'll **extract** raw files from a public file server, **transform** them from a non-CSV format into multiple BigQuery-compatible formats, and **load** them into cloud storage and a data warehouse — keeping observations and site locations as separate datasets that you join at query time.

Along the way, you'll experience the value of separating extraction from transformation (so you don't re-download 500MB every time you need to re-process), and you'll think about when to join data in your pipeline vs. at query time.

**That's exactly the kind of pipeline thinking that turns raw data files into queryable, mappable data products.**
