# SQLoad

A simple utility tool that scan SQL files with queries separated by comments into python dicts.


# Usage
Given a file called `queries.sql` with the following content:

```sql
-- find-all-by-name
SELECT * FROM users WHERE name = :name

-- find-one-by-id
SELECT * FROM users WHERE id = 10 LIMIT 1

-- find-users-join-products
SELECT * FROM users u
    INNER JOIN products p ON u.id = p.user_id
    WHERE u.id = 1
    LIMIT 1
```

You can load those queries into dicts as follow:

```python
from sqload import load

q = load('queries.sql')


assert q['find-all-by-name'] == "SELECT * FROM users WHERE name = :name"
```