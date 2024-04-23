<div class="markdown prose w-full break-words dark:prose-invert dark">
    <hr>
    <h2>Technology Stack Overview</h2>
    <p>Our application leverages a modern technology stack designed for performance, scalability, and ease of
        development. Below is an overview of the primary technologies employed across various aspects of the
        application:</p>
    <h3>Frontend</h3>
    <ul>
        <li><strong>Angular</strong>: A platform and framework for building single-page client applications using HTML
            and TypeScript. Angular provides a comprehensive solution for developing efficient and sophisticated web
            applications.
        </li>
    </ul>
    <h3>Backend</h3>
    <ul>
        <li><strong>FastAPI</strong>: A modern, fast (high-performance) web framework for building APIs with Python 3.12
            based on standard Python type hints. FastAPI integrates seamlessly with our frontend Angular application,
            providing robust backend services.
        </li>
    </ul>
    <h3>Databases</h3>
    <ul>
        <li><strong>PostgreSQL</strong>: A powerful, open-source object-relational database system that uses and extends
            the SQL language combined with many features that safely store and scale the most complicated data
            workloads.
        </li>
        <li><strong>MongoDB</strong>: A NoSQL database known for its high performance, availability, and scalability.
            MongoDB stores data in flexible, JSON-like documents, meaning data structure can change over time.
        </li>
    </ul>
    <h3>Cache</h3>
    <ul>
        <li><strong>Redis</strong>: An in-memory data structure store, used as a database, cache, and message broker.
            Redis supports data structures such as strings, hashes, lists, sets, and more, enabling high-speed access
            and data management.
        </li>
    </ul>
    <h3>Reverse Proxy</h3>
    <ul>
        <li><strong>NGINX</strong>: An HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy
            server, known for its high performance, stability, rich feature set, simple configuration, and low resource
            consumption.
        </li>
    </ul>
    <h3>Testing</h3>
    <ul>
        <li><strong>Cypress</strong>: An all-in-one testing framework, assertion library, with mocking and stubbing,
            perfect for end-to-end testing of our Angular applications.
        </li>
    </ul>
    <h3>Message Queue</h3>
    <ul>
        <li><strong>RabbitMQ/Kafka</strong>: Used for building real-time data processing pipelines and streaming apps.
            It provides a robust, unified platform that allows for high-throughput, fault-tolerant handling of streams
            of data.
        </li>
    </ul>
    <h3>Observability</h3>
    <ul>
        <li><strong>Prometheus &amp; Grafana</strong>: For monitoring and alerting toolkit specifically designed for
            time series data. Grafana allows for visualization and monitoring of metrics collected from various parts of
            the application.
        </li>
        <li><strong>Elastic Stack</strong>: Comprising Elasticsearch, Logstash, and Kibana, provides real-time insight
            into application performance and security analytics through log aggregation and visualization.
        </li>
    </ul>
    <h3>DevOps</h3>
    <ul>
        <li><strong>Docker</strong>: A set of platform-as-a-service products that use OS-level virtualization to deliver
            software in packages called containers.
        </li>
        <li><strong>Kubernetes</strong>: An open-source system for automating deployment, scaling, and management of
            containerized applications.
        </li>
        <li><strong>CI/CD</strong>: Continuous Integration and Continuous Delivery processes that allow for the
            automated testing and deployment of applications.
        </li>
    </ul>
    <h3>Security</h3>
    <ul>
        <li><strong>OAuth2 &amp; OpenID Connect</strong>: Standards for authorization and authentication that allow for
            the implementation of secured access to application resources.
        </li>
    </ul>
    <h3>Search</h3>
    <ul>
        <li><strong>Elasticsearch</strong>: A distributed, RESTful search and analytics engine capable of addressing a
            growing number of use cases.
        </li>
        <li><strong>Algolia</strong>: A hosted search engine capable of delivering real-time results from the first
            keystroke.
        </li>
    </ul>
    <h3>Analytics</h3>
    <ul>
        <li><strong>Apache Spark</strong>: A unified analytics engine for large-scale data processing, with built-in
            modules for streaming, SQL, machine learning, and graph processing.
        </li>
    </ul>
    <h3>User Experience</h3>
    <ul>
        <li><strong>User Interaction Analysis (Hotjar or FullStory)</strong>: Tools that provide insights into user
            behavior and interaction patterns on the web application, allowing for continuous improvement of the user
            experience.
        </li>
    </ul>
    <h3>Additional Technologies</h3>
    <ul>
        <li><strong>Web Application Firewall (WAF)</strong>, <strong>Selenium</strong> for browser compatibility tests,
            <strong>GraphQL</strong> as an alternative to RESTful APIs, <strong>PWA Technologies</strong> for offline
            capabilities, and <strong>State Management</strong> tools for Angular apps further enrich our application’s
            architecture.
        </li>
    </ul>
    <hr>
    </div>

<div class="markdown w-full break-words">
    <h2>User Management</h2>
    <ul>
        <li><strong>Register User</strong>: Allows new users to create an account.</li>
        <li><strong>Login User</strong>: Authenticates a user and grants access to the system.</li>
        <li><strong>Get User Profile</strong>: Retrieves the profile information of a user.</li>
        <li><strong>Update User Profile</strong>: Enables users to modify their profile details.</li>
        <li><strong>Delete User Profile</strong>: Allows users to delete their account.</li>
        <li><strong>Hibernate User Profile</strong>: Temporarily deactivates a user account.</li>
    </ul>
    <h2>Tool Listings</h2>
    <ul>
        <li><strong>List All Tools</strong>: Displays all available tools.</li>
        <li><strong>Add a Tool</strong>: Enables addition of a new tool to the listing.</li>
        <li><strong>Tool Profile</strong>: Retrieves detailed information of a specific tool.</li>
        <li><strong>User Tools</strong>: Lists tools associated with a specific user.</li>
        <li><strong>Update Tool Availability</strong>: Changes the availability status of a tool.</li>
        <li><strong>Update Tool</strong>: Allows modification of tool details.</li>
        <li><strong>Delete Tool</strong>: Removes a tool from the listing.</li>
        <li><strong>Tool Categories</strong>: Lists all tool categories.</li>
    </ul>
    <h2>Rentals</h2>
    <ul>
        <li><strong>Rent Tool</strong>: Initiates a tool rental process.</li>
        <li><strong>Rent Offer</strong>: Presents a rental offer for a specific tool.</li>
        <li><strong>Return a Tool</strong>: Facilitates the return process of a rented tool.</li>
        <li><strong>Rental Details</strong>: Provides detailed information on a rental.</li>
        <li><strong>Extend Rental</strong>: Allows the extension of the rental period.</li>
        <li><strong>Tool Calendar</strong>: Displays the availability calendar for a tool.</li>
        <li><strong>Delete Rental Offer</strong>: Removes a rental offer.</li>
        <li><strong>Rate and Review a Tool</strong>: Enables users to leave feedback on tools.</li>
    </ul>
    <h2>Admin Features</h2>
    <ul>
        <li><strong>Get All Rentals</strong>: Lists all rentals for admin review.</li>
        <li><strong>Manage Tool Categories</strong>: Allows admin to add, list, or remove tool
            categories.
        </li>
        <li><strong>View All Users</strong>: Lists all users in the system for
            admin.
        </li>
        <li><strong>Add User / Add Privileged User</strong>: Admin can create new users or privileged
            accounts.
        </li>
        <li><strong>Update User Status</strong>: Changes the status of a user
            account.
        </li>
        <li><strong>Delete User</strong>: Admin can delete user accounts.</li>
        <li><strong>Manage Rules and
            Permissions</strong>: Admin can adjust rules and permissions.
        </li>
    </ul>
    <h2>Maintenance and ServiceTracking</h2>
    <ul>
        <li><strong>Report Tool Issue / Schedule Maintenance / View Scheduled Maintenance / Cancel
            Scheduled Maintenance / Update Scheduled Maintenance / View Tool Issues / Update Tool Issue Status /
            Maintenance
            History / Assign Maintenance Task / Report Tool Issue by User</strong>: These endpoints allow reporting of
            tool
            issues, scheduling and managing maintenance tasks, and viewing maintenance history and tool
            issues.
        </li>
    </ul>
    <h2>Security Enhancements</h2>
    <ul>
        <li><strong>Enable Two-Factor Authentication</strong>:
            Enhances security by adding a second layer of authentication.
        </li>
        <li><strong>Audit Logs</strong>: Allows admins
            to view a record of system activities.
        </li>
    </ul>
</div>


