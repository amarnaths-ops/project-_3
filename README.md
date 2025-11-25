
README.md — Fragment Offset × Length Matrix Generator

Overview

Project_3.py is a command-line tool that reads BED-like fragment coordinates from STDIN, loads them into a temporary in-memory SQLite database, computes fragment offset and length, aggregates counts for each (offset, length) pair, and prints a tab-separated matrix to STDOUT.

This script is designed for downstream analyses such as building 2D fragment matrices, fragment density plots, or as input for heatmap-style visualization.


---

What the Script Does

1. Reads lines from STDIN (e.g., a BED file).


2. Extracts start and end positions.


3. Stores them in an in-memory SQLite table.


4. Runs an SQL query that computes:

offset = (start + end) / 2

fragment_length = end - start



5. Filters lengths in the range (0, 1000].


6. Aggregates counts for each (offset, fragment_length).


7. Prints results in sorted, tab-separated format.




---

Input Format (STDIN)

The script expects space- or tab-separated fields where:

column1   start   end   ...

Example input lines:

chr1 100 150
chr1 120 160
chr1 300 320
chr1 100 130
chr1 120 150

Only column 2 (start) and column 3 (end) are used.


---

Output Format (STDOUT)

The script prints:

offset    fragment_length    count

Where:

offset = midpoint of fragment = (start + end) / 2

fragment_length = end – start

count = number of fragments with this (offset, length) combination



---

How to Run

Option 1: Pipe a file

cat fragments.bed | python Project_3.py > matrix.tsv

Option 2: Direct input (typing)

python Project_3.py
chr1 100 150
chr1 120 160
...
(CTRL + D to finish)


---

Example Input → Output

Below is a small demo using 5 input lines.


---

Example Input

chr1 100 150
chr1 120 160
chr1 300 320
chr1 100 130
chr1 120 150

Compute Offsets and Lengths

start	end	length	offset

100	150	50	125
120	160	40	140
300	320	20	310
100	130	30	115
120	150	30	135


Grouped counts:

(offset=115, length=30) → 1

(offset=125, length=50) → 1

(offset=135, length=30) → 1

(offset=140, length=40) → 1

(offset=310, length=20) → 1



---

Example Output

offset	fragment_length	count
115	30	1
125	50	1
135	30	1
140	40	1
310	20	1

This is exactly the format your script prints.


---

Performance Notes

Uses an in-memory SQLite database → fast and memory-efficient.

Inserts fragments in batches for optimal performance.

Suitable for tens of millions of fragments depending on system memory.

SQL handles all aggregation work.
