keynotes = [ 
    {
        'type'    : 'Keynote',
        'slug'    : 'keynote_1',
        'image'   : 'oleg.jpg',
        'speaker' : 'Oleg Bartunov',
        'title'   : 'Postgres Innovations',
        'short_bio' : """
                        Oleg Bartunov has been involved in PostgreSQL development since 1996 (he introduced locale support). He is a major developer and a member of the PGDG. He is the major contributor for user-defined index access methods GiST, GIN and SP-GiST, built-in full-text search facilities in PostgreSQL and a number of popular extensions like intarray, ltree, hstore, pg_trgm, jsquery and rum access method. His latest contributions are jsonb and implementation of SQL/JSON.
                    """,
        'long_bio'  : """
                            Oleg Bartunov has been involved in PostgreSQL development since 1996 (he introduced locale support). He is a major developer and a member of the PGDG. Together with his colleague Teodor Sigaev he developed infrastructure for implementing user-defined index access methods GiST, GIN and SP-GiST, built-in full-text search facilities in PostgreSQL (formerly known as tsearch2) and a number of popular extensions like intarray, ltree, hstore, pg_trgm, jsquery and rum access method. His latest contributions are jsonb and implementation of SQL/JSON. His current project is pluggable TOAST API and  scalable JSONB/JSON.

                            Oleg graduated from the Astronomy department of the Physics department at Lomonosov's Moscow State University. During his professional work at Sternberg Astronomical Institute (SAI MSU) he realized he needed a free and powerful open-source database like PostgreSQL (Postgres95 that time). Since then he extensively used PostgreSQL in his scientific work and many other projects. Oleg is an active member of the Russian PostgreSQL community, he advocated the adoption of PostgreSQL by the astronomical community.
                        """,
        'abstract'  : """
                       PostgreSQL, commonly referred to as Postgres, is a free and open-source relational database management system that has been in development for over 30 years. This talk aims to delve into the innovations that have been introduced in Postgres over the years, including the initial design of Postgres, the historical background of some innovative features, and the future horizons of Postgres.
                        """
    },
    {
        'type'    : 'Keynote',
        'slug'    : 'keynote_2',
        'image'   : 'chris.jpg',
        'speaker' : 'Chris Travers',
        'title'   : 'What Database Teams Can Learn from Flight Safety?',
        'short_bio' : """
                            Chris has 24 years of experience with PostgreSQL as an application developer, database administrator, and database engineer.  He has also worked as an engineering manager for teams maintaining critical environments.  Chris's teams have managed PostgreSQL environments into the petabytes, and he has significant experience with mission-critical operations both as an individual contributor and as a manager. 
                    """,
        'long_bio'  : """
                            Chris has 24 years of experience with PostgreSQL as an application developer, database administrator, and database engineer.  He has also worked as an engineering manager for teams maintaining critical environments.  Chris's teams have managed PostgreSQL environments into the petabytes, and he has significant experience with mission-critical operations both as an individual contributor and as a manager.  One particularly important contribution was the implementation of human factors or crew resource management training at Adjust, where he used to work.  Chris has become a strong believer that our industry shortcomings can be resolved by looking at how other critical industries, such as airlines, avoid and manage incidents.
                            
                        """,
        'abstract'  : """
                            Sixty years ago, the airline industry blamed 90% of aircraft accidents on pilot error.  Today the percentage is similar, and yet flying is nearly a hundred times safer.  This means that the aviation industry has become better at preventing human error from causing accidents as quickly as they have become better at preventing and mitigating mechanical and technical faults.  Yet, our industry still makes very little effort to understand the kinds of mistakes people make or why.   This is a talk about how to dramatically reduce human error in database operations by leveraging the lessons from aviation based on experience implementing such programs.  In this program we will discuss some common causes of human error and how we are often complicit in making that more likely, as well as concrete steps we need to take as an industry to make that less likely, as well as how to go about trying to implement such change.
                        """
    },
]

workshops = [
    {
        'type'    : 'Workshop',
        'slug'    : 'workshop_jashan',
        'image'   : 'jashan.jpeg',
        'speaker' : 'Jashanpreet Singh',
        'title'   : 'Dockerize your PostgreSQL: A Step-by-Step Guide for Easy Deployment and Management',
        'long_bio'     : """
                        Jashanpreet is a highly skilled Full Stack Developer with over 5 years of experience in developing 
                        robust applications. He has worked on a variety of projects, spanning different industries and domains. 
                        Throughout his career, Jashanpreet has consistently chosen Postgres as his primary database 
                        due to its open-source nature, outstanding performance, ease of use, and versatility 
                        in handling various use cases such as geospatial and financial data.
                    """, 
        'abstract' : """
                        While most of you have worked with postgres, you might or might not have also come across docker. <br>
                        While postgres is a powerful open-source relational database management system, Docker is a containerization tool that allows developers to package applications and dependencies into a single, portable unit.<br>
                        Docker can be super helpful when spinning up a quick dev environment or more complex use cases like standard postgres installation among all your server, developer systems and more. <br>
                        And you'll realize it's super easy to work with too, in this talk we'll cover:<br>
                        - Basics of docker and postgres (just for refresh) <br>
                        - Spinning up a postgres docker instance <br>
                        - Using docker exec and psql to access the database <br>
                        - Loading a large chunk of data in the database <br>
                        - Building your own postgres docker image with your own extensions. modifications and more<br>
                        - Creating a docker-compose file to add pgAdmin4 instance with postgres for easy dev setup <br>

                        After this talk, you'll have a full understanding of how to use docker to quickly spin up new postgres instances or manage postgres in servers.
                    """

    },
    {
        'type'    : 'Workshop',
        'slug'    : 'workshop_krishna',
        'image'   : 'krishna.jpeg',
        'speaker' : 'Krishna lodha',
        'title'   : 'PostgREST - Create APIs from PostgreSQL Directly',
        'long_bio'     : """
                    Krishna is a self-taught Web GIS Developer with a deep love for Open Source technologies. 
                    When not coding, he can be found creating video tutorials and writing blogs on 
                    various open-source tech stacks. He can be found on YouTube and their personal blogs,
                    where he shares his extensive knowledge of web development and GIS.
                    """, 
        'abstract' : """
                    PostgREST is a powerful open-source tool that allows developers to automatically 
                    generate a RESTful API from a PostgreSQL database. 
                    In this talk, we will explore the capabilities of PostgREST and how it can be used 
                    to quickly and easily create APIs directly from PostgreSQL. We will start by 
                    introducing the basics of RESTful APIs and how they work. We will then dive into 
                    the installation and configuration of PostgREST, and explore its capabilities for 
                    automatically generating API endpoints based on database tables and views. 
                    We will also cover various aspects of API design, including authentication, authorization, 
                    and documentation. <br>
                    Attendees will leave with a solid understanding of how to use PostgREST
                      to create powerful and secure APIs from PostgreSQL, 
                      and how it can be leveraged to streamline the development of modern web applications.
                    """

    }
]

talks = [
    {
        'type'    : 'talk',
        'slug'    : 'egor',
        'image'   : 'egor.jpg',
        'speaker' : 'Egor Rogov',
        'title'   : 'A retrospective look at the statistics',
        'long_bio'  : """
                            Egor Rogov is the author of “PostgreSQL Internals” book and co-author of “Postgres: The First Experience” booklet. 
                            Egor graduated from Computer Science Faculty of Lomonosov Moscow State University and 
                            has more than 15 years of Database Management Systems experience as an application developer and project manager. 
                            Since 2015 Egor works on educational programs in Postgres Professional company. 
                        """,
        'abstract'  : """
                            To build a decent query plan, the optimizer has to understand statistical characteristics of underlying data, which requires to find a balance between accuracy and the volume of gathered statistics. It is important to get a grasp of the concept, because selectivity misestimates are known to be a frequent cause of poor query plans.
                            <br><br>
                            I will show how the structure of the collected statistics has evolved and become more complicated over time: what the optimizer relied on back in its early days and what is at his disposal now with the new release of PostgreSQL. I will also talk about how to manage statistics and whether it is necessary to think about it at all.
                        """
    },
    {
        'type'    : 'talk',
        'slug'    : 'pavel',
        'image'   : 'pavel.jpg',
        'speaker' : 'Pavel Tolmachev',
        'title'   : 'Query plans. Reading, comprehension and acceleration',
        'long_bio'  : """
                            As an experienced programmer, Pavel Tolmachev have worked with  PostgreSQL, 
                            C#, WinForms, WPF, ASP.NET, and Oracle PL/SQL. 
                            He have been involved in the implementation of electronic document management systems 
                            and have also worked as a teacher, instructing students, administrators, and application programmers.
                            <br>
                            Currently, he is engaged in educational programs in Postgres Professional, 
                            where he write articles, workshops, training courses, make presentations, and more. 
                            Since his student days, he have had a keen interest in DBMS, 
                            and  especially enjoyed studying the workings of the optimizer.
                        """,
        'abstract'  : """
                            SQL is a declarative programming language used to create and manipulate objects in relational databases but it doesn't describe how to get the data. The query optimizer (called simply the optimizer or planner) is a built-in database component that determines the most efficient method for a SQL statement to access requested data. 
                            <br>
                            PostgreSQL devises a query plan for each query it receives. We can use the EXPLAIN command to see what query plan the optimizer creates for any query. Plan-reading is an art that requires some experience to master.
                            <br><br>
                            In this report, I will talk about: <br>
                            - EXPLAIN command;<br>
                            - its various parameters;<br>
                            - plan structure;<br>
                            - its different plan nodes and elements;<br>
                            - and using indexes and other techniques for Query Performance Tuning.<br>
                            <br><br>
                            I will demonstrate all my examples on our free demo database for PostgreSQL. The subject field of this database is airline flights across various airports.
                        """
    },
    {
        'type'    : 'Talk',
        'slug'    : 'umair',
        'image'   : 'umair.jpeg',
        'speaker' : 'Umair Shahid',
        'title'   : 'Clustering in PostgreSQL: Because one database server is never enough (and neither is two)',
        'long_bio'  : """                           
                        Umair Shahid is a 20-year veteran of the PostgreSQL community with a passion for 
                        solving real-world problems with technology. 
                        He actively advocates for PostgreSQL around the world, speaking at conferences, 
                        being a part of organizing teams, and leading local user groups. 
                        Umair is the founder of Stormatics - an organization dedicated to providing PostgreSQL 
                        solutions for the enterprise. 
                        Previously, he has been a part of major pure-play PostgreSQL organizations 
                        like EDB, 2ndQuadrant, & OpenSCG.
                    """,
        'abstract'  : """
                            In the world of database management, high availability and disaster recovery are 
                            key considerations for any organization that wants to ensure reliable access 
                            to its critical data. Clustering in PostgreSQL is one of the most effective ways to 
                            achieve both. In this talk, we will explore the ins and outs of PostgreSQL clustering, 
                            including the benefits and challenges of different clustering approaches, 
                            and how to set up a highly available and disaster-resilient PostgreSQL cluster.
                            <br>
                            We will dive into topics such as synchronous vs. asynchronous replication, load balancing, 
                            failover, and disaster recovery. We will also touch on some open source tools 
                            that are readily available to aid in PostgreSQL cluster management.
                        """
    },
    {
        'type'    : 'Talk',
        'slug'    : 'jashan_talk',
        'image'   : 'jashan.jpeg',
        'speaker' : 'Jashanpreet Singh',
        'title'   : 'Mastering Time Series Data Management with Postgres + TimescaleDB',
        'long_bio'     : """
                        Jashanpreet is a highly skilled Full Stack Developer with over 5 years of experience in developing 
                        robust applications. He has worked on a variety of projects, spanning different industries and domains. 
                        Throughout his career, Jashanpreet has consistently chosen Postgres as his primary database 
                        due to its open-source nature, outstanding performance, ease of use, and versatility 
                        in handling various use cases such as geospatial and financial data.
                    """, 
        'abstract'  : """
                            Time series data is a type of data that is collected over time, often in regular intervals. It is commonly used in various applications such as financial trading, IoT, sensor data, weather data, etc.
                            While postgres can handle any data effectively, when it comes to time-series data, timescaleDB is a class apart. Built as an extension of postgres, timescaleDB is one of the most popular extensions in postgres and that excludes its popularity in handling time-series data. 
                            <br>
                            In this talk, we'll discuss:<br>
                            - What is timescaleDB? <br>
                            - Setting and installing timescaleDB (we'll use docker image)<br>
                            - Load real-world data into the database<br>
                            - Creating a hypertable. What's happening under the hood? and compare to a normal postgres table <br>
                            - Using Continous Aggregates <br>
                            - Using timescaleDB compression <br>
                            - A path forward <br>
                            <br><br>
                            After this talk, you'll have an understanding of some nuances, challenges around time-series and how to handle it effectively using timescaleDB
                        """
    },
    {
        'type'    : 'Talk',
        'slug'    : 'dev',
        'image'   : 'dev.jpg',
        'speaker' : 'Devraj Gautam',
        'title'   : 'Adding the Cherry of NoSQL on Top of Relational Cake',
        'long_bio'  : """
                           Over the past 14 years, Devraj has developed a diverse skillset in software engineering, 
                           project/product management, system architecture analysis, and design. 
                           He have built scalable software and data solutions across a range of domains and industries, 
                           from small startups to large enterprise organizations.
                            <br>
                            As a co-founder of Cloudtai, he plays a critical role in designing 
                            innovative solutions and making key technical decisions. 
                            He is passionate about writing reusable software components 
                            that can be shared with the team and providing mentorship to 
                            help others grow and develop their skills.
                            <br>
                            With a strong focus on agile methodologies such as Scrum, 
                            He has extensive experience in managing complex projects for both national and international clients. 
                            He is driven to deliver high-quality products that meet business goals and exceed expectations. 
                        """,
        'abstract'  : """
                            Most of us build applications in the standard relational database schemas in Postgre SQL. There might be
                            scenarios where you want no-SQL data storage for unstructured data in your application. SOll, you can't
                            use the modern No-SQL-based database because of various reasons.
                            <br>In this talk, I will discuss the scenarios when you can use the JSON data in Postgre SQL to store
                            unstructured data so that you can leverage the same standard relaOonal database for your unstructured
                            data. We will explore various problem scenarios when you can store unstructured data and provide an
                            efficient solution to the problems. The talk will cover the possible database model to store data and
                            queries needed to retrieve data for the solution to the problem.
                            <br> The Otle takes a metaphor of cake and cheery cake in the sense that you have a whole database with
                            relaOonal database objects. You want to top it with cheery, meaning achieving better efficiency by
                            storing non-structured data in JSON when needed. This talk is not about designing a totally No-SQL
                            unstructured database but is about using the capabilities of JSON to store and retrieve unstructured
                            data when needed at same reaping the benefits of relational data storage.
                        """
    },
    {
        'type'    : 'Talk',
        'slug'    : 'sandip',
        'image'   : 'sandip.jpg',
        'speaker' : 'Sandip Basnet',
        'title'   : 'Database in a Microservice with PostgreSQL',
        'long_bio'  : """
                           Sandip is a dedicated software engineer who has spent the last 5 years designing 
                           and building scalable and robust backend solutions. His expertise in JavaScript ecosystem,  
                           combined with his knowledge of databases, makes him a versatile backend developer 
                           who is comfortable working with a range of technologies. He believes in identifying issues 
                           and finding creative solutions that deliver tangible results.
                            <br>
                            Beyond his work as a backend developer, Sandip has a passion for exploring the outdoors. 
                            He enjoys traveling to the mountains and going on bike rides to explore the beautiful 
                            scenery around him. His love for adventure and exploring new places has taught him valuable 
                            skills such as adaptability, problem-solving, and teamwork.
 
                        """,
        'abstract'  : """
                            
                            Microservices architecture has gained significant popularity in recent years for its ability to 
                            break down software into smaller, more manageable components. In the database realm, microservices 
                            offer several advantages, including the ability to scale and manage data more efficiently 
                            and to reduce downtime during upgrades and maintenance.
                            <br>
                            On the talk we'll discuss on  the overview of microservices architecture and 
                            its benefits in the context of database management , 
                            Practices for designing and implementing a microservices-based database architecture such as
                            multi-schema databases, shared-nothing architectures, and event-driven architectures etc.
                            <br><br>
                            The talk will help  the developers, architects, and database administrators who are interested in exploring 
                            new approaches to database management in a microservices environment using PostgreSQL.
                            <br>
                            The session will provide practical guidance and real-world examples for implementing 
                            a microservices-based database architecture, as well as opportunities for discussion and questions from the audience.

                        """
    },
     {
        'type'    : 'Talk',
        'slug'    : 'krishna_talk',
        'image'   : 'krishna.jpeg',
        'speaker' : 'Krishna lodha',
        'title'   : 'PostGIS - Using location data in PostgreSQL',
        'long_bio'     : """
                        Krishna is a self-taught Web GIS Developer with a deep love for Open Source technologies. 
                        When not coding, he can be found creating video tutorials and writing blogs on 
                        various open-source tech stacks. He can be found on YouTube and their personal blogs,
                        where he shares his extensive knowledge of web development and GIS.
                    """, 
        'abstract'  : """
                        This talk explores the use of location data in PostgreSQL, 
                        a powerful open-source relational database management system. 
                        We will delve into the basics of PostgreSQL's spatial extensions PostGIS, 
                        and explore various ways of handling and querying location data in the database. 
                        We will also discuss how to leverage PostGIS's capabilities to store, 
                        manipulate, and analyze geospatial data effectively. 
                        <br>
                        Attendees will leave with a solid understanding of how to work with location 
                        data in PostgreSQL and how to apply it to their own projects.
                    """
    },
    
     
    
    {
        'type'    : 'talk',
        'slug'    : 'talk_chris',
        'image'   : 'chris.jpg',
        'speaker' : 'Chris Travers',
        'title'   : 'Crazy Things You Can Do with PostgreSQL Indexes',
        
        'long_bio'  : """
                            Chris has 24 years of experience with PostgreSQL as an application developer, database administrator, and database engineer.  He has also worked as an engineering manager for teams maintaining critical environments.  Chris's teams have managed PostgreSQL environments into the petabytes, and he has significant experience with mission-critical operations both as an individual contributor and as a manager.  One particularly important contribution was the implementation of human factors or crew resource management training at Adjust, where he used to work.  Chris has become a strong believer that our industry shortcomings can be resolved by looking at how other critical industries, such as airlines, avoid and manage incidents.                    
                        """,
        'abstract'  : """
                            With the rise of NoSQL databases, a number of falsehoods have flourished regarding how to choose a database engine. This talk focuses specifically on Redis and PostgreSQL, and why one might choose one or the other.
                            <br>
                            At small scales, we can often get by thinking of database servers as black boxes, but as we scale, the internals and architecture become more and more important. This talk focuses on behavior of these systems at scale and under load.
                            <br>
                            In this presentation you will learn:<br>
                            - How Redis and PostgreSQL differ architecturally <br>
                            - How differences in architecture affect scalability and performance <br>
                            - Cases here Redis is the clear winner <br>
                            - Cases where PostgreSQL is the clear winner<br>
                            <br>
                            Additionally, some notes will be offered in terms of where PostgreSQL can improve in to compete with the sorts of workloads that generally favor Redis.
                        """
    }, 
    {
        'type'    : 'Talk',
        'slug'    : 'rho',
        'image'   : 'rho.jpg',
        'speaker' : 'Rohit Man Amatya',
        'title'   : 'Bye Bye Wordpress: Migrating data from MySQL to Postgress',
        'long_bio'  : """
                        With a background in the design and development of hardware and
                        software products, Rohit Man Amatya has hands-on experience working with open source
                        platforms. He is also an instructor, delivering training and workshops
                        on developer tools and techniques to helping professionals improve
                        their skills.
                    """,
        'abstract'  : """
                        The World Press platform is frequently used for both personal and business blogging purposes. However, businesses may eventually decide to transition to their own customized Content Management System (CMS). While it is easier to migrate the existing system to a new one while keeping the database intact, deciding to change the database as well is a significant decision. By default, World Press uses MySQL.
                        <br><br>
                        Our team recently moved from World Press to our own CMS for our blogging website and made the decision to migrate from MySQL to PostgreSQL. In this discussion, we will share our experience on the process of migrating from a WordPress blog to Postgres with Flask.
                    """
    },
    {
        'type'    : 'Talk',
        'slug'    : 'talk_oleg',
        'image'   : 'oleg.jpg',
        'speaker' : 'Oleg Bartunov',
        'title'   : 'SQL/JSON in PostgreSQL 16',
        'long_bio'  : """
                            Oleg Bartunov has been involved in PostgreSQL development since 1996 (he introduced locale support). He is a major developer and a member of the PGDG. Together with his colleague Teodor Sigaev he developed infrastructure for implementing user-defined index access methods GiST, GIN and SP-GiST, built-in full-text search facilities in PostgreSQL (formerly known as tsearch2) and a number of popular extensions like intarray, ltree, hstore, pg_trgm, jsquery and rum access method. His latest contributions are jsonb and implementation of SQL/JSON. His current project is pluggable TOAST API and  scalable JSONB/JSON.

                            Oleg graduated from the Astronomy department of the Physics department at Lomonosov's Moscow State University. During his professional work at Sternberg Astronomical Institute (SAI MSU) he realized he needed a free and powerful open-source database like PostgreSQL (Postgres95 that time). Since then he extensively used PostgreSQL in his scientific work and many other projects. Oleg is an active member of the Russian PostgreSQL community, he advocated the adoption of PostgreSQL by the astronomical community.
                        """,
        'abstract'  : """
                            As time goes by, there is a growing trend in the use of JSON and JSONB in production databases. 
                            Moreover, PostgreSQL is continuously adding new NoSQL-related (support of json, jsonb etc.) 
                            features. 
                            <br>In this presentation, the latest advancements in PostgreSQL 16 
                             regarding JSON will be discussed, with a particular focus 
                            on the new features that have been recently adopted.
                        """
    },

    # {
    #     'type'    : 'talk',
    #     'slug'    : ' ',
    #     'image'   : ' .jpg',
    #     'speaker' : '   ',
    #     'title'   : ' ',
    #     'long_bio'  : """
                            
    #                     """,
    #     'abstract'  : """
                            
    #                     """
    # },
   

]
