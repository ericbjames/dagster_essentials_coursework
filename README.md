# Dagster Essentials

This week I looked into Dagster. Specifically I took their ‘Essentials’ course and here 5 cool things I learned.

#1 Dagster projects are built using Python. This makes projects very easy to setup and readable. Take a look the parts that make up this project and UI with some code examples.

![Dagster_Uni_Practice_Diagram_Annotated](https://github.com/ericbjames/dagster_essentials_coursework/assets/101911329/00e60571-ebc9-4d55-9286-f2797b39ea2f)


___

#2 Project organization feels intuitive to me. In our project's main `__init__.py`, we use a single 'defs' variable to contain assets, resources, jobs, schedules, and sensors, all imported from their respective folders, and are ready for Dagster to process.


<img width="1356" alt="dagster project creation init" src="https://github.com/ericbjames/dagster_essentials_coursework/assets/101911329/a88a61d1-1ef4-4e16-89d0-07c365782171">

___

#3 Dagster adopts a unique approach to organizing data products for orchestration, replacing a task-focused method with an asset-centric one. To illustrate this, let's consider the analogy of making a sandwich:

![Uploading Asset_vs_Task_Diagram.png…]()

___

#4 Sensors allow you to automate your pipelines based on a state change like launching a run whenever a file gets dropped into an s3 bucket. If you are interested, I would also look into run_key and cursors which further improve this. ([Docs](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors#evaluation-interval))

___

#5 What about Metadata? Two cool things: First, you can track different metadata levels in your pipeline, such as record counts when assets are materialized. Second, the MetadataValue class supports rich metadata such as markdown, tables, and images for the UI. ([Docs](https://docs.dagster.io/concepts/ops-jobs-graphs/metadata-tags#metadata))
