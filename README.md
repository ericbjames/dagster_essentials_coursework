# Dagster Essentials

This week I looked into Dagster. Specifically I took their ‘Essentials’ course and here 5 cool things I learned.

#1 Dagster projects are built using Python. This makes projects very easy to setup and readable. Take a look the parts that make up this project and UI with some code examples.

![Annotated final dagster UI diagram.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/7288d008-d1b7-4b5c-8ee4-1503491a4dd7/6995711d-f5c0-47fd-813d-74cc3875030e/Annotated_final_dagster_UI_diagram.png)

___

#2 Project organization feels intuitive to me. In our project's main `__init__.py`, we use a single 'defs' variable to contain assets, resources, jobs, schedules, and sensors, all imported from their respective folders, and are ready for Dagster to process.

![dagster project creation init.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/7288d008-d1b7-4b5c-8ee4-1503491a4dd7/0b687e17-884f-4ea4-8505-a4c0257772be/dagster_project_creation_init.png)

___

#3 Dagster adopts a unique approach to organizing data products for orchestration, replacing a task-focused method with an asset-centric one. To illustrate this, let's consider the analogy of making a sandwich:

![Asset_vs_Task_Diagram.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/7288d008-d1b7-4b5c-8ee4-1503491a4dd7/2ac8f93a-50d1-42ff-81b9-d494a1b1b7ca/Asset_vs_Task_Diagram.png)

___

#4 Sensors allow you to automate your pipelines based on a state change like launching a run whenever a file gets dropped into an s3 bucket. If you are interested, I would also look into run_key and cursors which further improve this. ([Docs](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors#evaluation-interval))

___

#5 What about Metadata? Two cool things: First, you can track different metadata levels in your pipeline, such as record counts when assets are materialized. Second, the MetadataValue class supports rich metadata such as markdown, tables, and images for the UI. ([Docs](https://docs.dagster.io/concepts/ops-jobs-graphs/metadata-tags#metadata))
