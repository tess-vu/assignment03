# Assignment 03 — Motivation: Who Needs This Data, and Why?

In this class, we're building **cloud-based, data-centric products** — tools and systems whose primary purpose is to help someone make a decision using data. These decisions aren't one-time research questions. They're **recurring, operational decisions** — things that real people need to decide again and again, and where having current, well-organized data changes the action they take.

The data pipeline components you'll build in this assignment are the kind of behind-the-scenes infrastructure that powers the tools people use to make these decisions.

## The Data: EPA Air Quality Monitoring

The EPA operates a network of thousands of air quality monitors across the United States. These monitors continuously measure pollutants like PM2.5 (fine particulate matter), ozone, and nitrogen dioxide. The data is published as bulk CSV files and updated twice a year.

Raw CSV files on a government website are not a data _product_. They're a data _source_. To turn them into something actionable, someone has to:

1. **Extract** the data (download and unzip the files)
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

## The connection to this assignment

The EPA publishes raw monitoring data as bulk CSV files. But the people making the decisions above need that data in a form they can **query**, **map**, and **act on** — quickly and repeatedly. Someone has to build the pipeline that takes those CSVs, converts them into efficient formats, loads them into cloud storage, and makes them queryable in a data warehouse.

**That's exactly what this assignment asks you to do.**
