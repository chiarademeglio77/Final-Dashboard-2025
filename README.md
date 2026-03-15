This dashboard ( Also visible here https://final-dashboard-2025-zosyxwzsxrgniy874rqpyj.streamlit.app/) is a high-level technical and operational oversight tool designed to track the recovery and stabilization of the STC Autoscuola ERP 2025 project as it reaches Week 29. It translates complex development data—such as Schedule Performance Index (SPI) and Sprint Velocity—into business-centric metrics to help leadership understand exactly how fast the team is moving and where capacity risks remain.

The visual layout focuses on three key pillars: delivery speed, operational efficiency, and software quality. By showcasing a clear transition from high-latency handovers and slow bug resolution in the early stages to the current state of high-velocity sprints and rapid defect fixes, the dashboard serves as proof of a successful process turnaround. Ultimately, it identifies remaining high-risk technical hurdles, such as critical security vulnerabilities, to ensure that the final push toward release is data-driven and transparent. 

Accompanying this dashboard is the STC Commentary file, which serves as a practical blueprint for our analytical team. From a business perspective, this document is essential because it establishes a 'communication standard,' ensuring that every technical metric is translated into consistent, strategic insights for the board. Technically, the STC Commentary provides a step-by-step example of how an analyst uses the dashboard to explain the current situation to leadership. 

![Dashboard Preview](Dashboard%20STC.jpg)

## **STC Leadership Dashboard Sample Analysis**

Let’s walk through the **STC Leadership Dashboard** for the Autoscuola ERP 2025 project, focusing on our status for **Week 29**.

Starting at the top left with our **SPI (Schedule Performance Index)**, we are currently looking at a value of **0.85**. In business terms, this is our "speedometer": it tells us that for every hour of work we planned to finish by this date, we have only actually completed about **51 minutes**. Technically, this is the ratio of Earned Value to Planned Value. While we are currently **0.15 behind our target**, the recovery trend you see below shows we started much lower and are steadily regaining momentum.

Moving to the right, our **Defect Health** shows a total of 19 bugs found during UAT. From a business perspective, this represents our "stability gate." We have **2 Critical, 5 High, and 12 Medium defects**. These are manually logged during testing cycles to ensure the software is safe for release.

Next, the **Handover Lag** is sitting at **4.1 Hours**. This is a critical metric for our internal efficiency, measuring the "idle time" between when a developer finishes a task and when it is picked up for testing. Technically, it’s the average timestamp difference between "Done" and "In Testing" statuses. We are slightly above our **4.0-hour target**, which acts as a yellow flag for potential bottlenecks in our workflow.

Finally, on the top right, we have a **Sprint Velocity of 79%**. For the business, this indicates our **"reliability."** Technically, it is the percentage of Story Points completed versus those committed at the start of the sprint. A **79% score suggests a Capacity Risk**, meaning we are over-promising what we can actually deliver in a two-week window.

---

## **Performance & Task Audit**

Moving down to our first main section, **Performance & Task Audit**, we have a dual-view of our timeline.

On the left, the **SPI Recovery Trend** chart illustrates our journey from a rocky start in May (where we were at a critical 0.40) to our current 0.85. This line graph is calculated by plotting the weekly aggregate of project progress. The upward slope is a positive business sign, indicating that our recent process improvements are working and we are trending toward a "healthy" 1.0.

To the right of the trend line is our **Task Audit Console**. This table provides the granular "who and what" behind the numbers. Under **Completed This Week**, you can see tasks like "Shift Planning Fixes" and "Enrollment Design" achieved a **perfect 1.00 SPI**, meaning they were finished exactly on time. Below that, the **Ongoing** section highlights where our delays are coming from. For instance, the "Configure VAT Rules" task has an **SPI of 0.45**, having taken 22 days against a 10-day plan. Technically, the color-coding you see—red for high variance and green for zero variance—is a dynamic calculation based on the **Variance (Days)** column, which is simply the difference between actual days taken and the original estimate.

---

## **Regional Efficiency & Sprint Metrics**

Moving further down into the **Regional Efficiency & Sprint Metrics** section, we transition from overall health to the actual mechanics of our delivery teams.

Looking at the **Technical Intake** donut chart on the left, we can see the complexity of the work we are currently absorbing. From a business perspective, this represents our **"workload composition"**—it's vital for understanding if we are being weighed down by heavy lifting or moving through smaller tasks. Currently, you'll notice that over **41% of our intake consists of "XL" tickets**. Technically, this is calculated by aggregating the T-shirt size estimates of every ticket as it enters our intake phase.

Moving to the center, the **Handover Lag** line chart is perhaps our most encouraging visual today. This is our **"collaboration friction"** metric, measuring the idle time between a developer finishing a task and a tester picking it up. After a high of over 20 hours in early sprints, the line takes a sharp dive at Sprint 5, finally settling below our **4.0-hour target**. This is technically calculated as the average time delta between the "Resolved" and "In Testing" status timestamps, and it signifies that our regional teams have successfully eliminated a major bottleneck.

To the right, the **Sprint Velocity Heatmap** gives us a clear look at our **"team reliability."** Business leaders should look at this as a predictability map. While the early sprints show a lot of red and orange—where teams were only hitting about **60% of their commitments**—the most recent columns are almost entirely solid green, with many workstreams achieving **100% velocity**. This is technically the ratio of story points completed versus those committed during sprint planning, and it proves that our capacity forecasting is now highly accurate.

---

## **Quality Assurance & Bug Tracking**

Finally, let’s look at our **"readiness for market"** in the bottom row. On the left, the **Defect Resolution Speed (MTTR)** scatter plot tracks our responsiveness to failure. From a business standpoint, we want to see bubbles moving down and to the right. You can see that earlier in the project, we had large bubbles sitting high on the Y-axis, meaning bugs were taking **15 to 25 days to fix**. However, as of mid-June, the bubbles have plummeted, with most fixes now taking **under 5 days**. Technically, each bubble is a defect where the Y-axis represents the Mean Time to Repair, and the colors are mapped directly to the workstream responsible.

To conclude, the **Critical Defect Resolution Log** on the right is our **"high-risk inventory."** This table identifies the specific technical hurdles, like **SQL Injection vulnerabilities** or **Database deadlocks**, that could block our release. It technically pulls only those records tagged as "Critical" severity and sorts them by resolution time, ensuring that the most complex and long-standing risks are always at the top of our hit list.
