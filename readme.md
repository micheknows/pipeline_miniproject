# Ticket Sales Pipeline

This project implements a ticket sales pipeline that allows third-party sellers to upload ticket sales data in CSV format and provides recommendations for popular events based on sales data.

## Requirements

To run this project, you will need:

- Python 3.x
- MySQL server
- `mysql-connector-python` package Install with <pre><code>pip install mysql-connector-python </code></pre>

## Installation

1. Clone this repository:
<pre><code>
git clone https://github.com/micheknows/pipeline_miniproject.git
</code></pre>

2. Create a new MySQL database for the project, called 'pipeline'.

3.  You can create the table if you like, but it will be automatically created, if you do not, according to this:

<pre><code>
CREATE TABLE IF NOT EXISTS ticket_sales (
    ticket_id INT,
    trans_date DATE,
    event_id INT,
    event_name VARCHAR(50),
    event_date DATE,
    event_type VARCHAR(10),
    event_city VARCHAR(20),
    customer_id INT,
    price DECIMAL,
    num_tickets INT,
    PRIMARY KEY (ticket_id)
);
</code></pre>

4.  Update the config.py file with your database credentials:
<pre><code>
DATABASE_CONFIG = {
    'user': 'your-username',
    'password': 'your-password',
    'host': 'localhost',
    'port': 3306,
    'database': 'pipeline'
}
</code></pre>

5.  Run the pipeline script to load the sample data:
<pre><code>
python pipeline.py third_party_sales_1.csv
</code></pre>

## Author
Michelle Rogers

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the LICENSE file for details.

## Acknowledgements
This project was created as part of the Springboard Bootcamp program.