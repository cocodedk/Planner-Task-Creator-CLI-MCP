# Listing and Discovery

## List All Plans

```bash
$ python planner.py list-plans

[
  {
    "id": "plan-id-1",
    "title": "Work Projects",
    "owner": "group-id-1",
    "groupName": "Engineering Team"
  },
  {
    "id": "plan-id-2",
    "title": "Personal Tasks",
    "owner": "group-id-2",
    "groupName": "My Personal Group"
  }
]
```

## List Buckets in a Plan

```bash
$ python planner.py list-buckets --plan "Work Projects"

[
  {
    "id": "bucket-id-1",
    "name": "To Do",
    "planId": "plan-id-1"
  },
  {
    "id": "bucket-id-2",
    "name": "In Progress",
    "planId": "plan-id-1"
  },
  {
    "id": "bucket-id-3",
    "name": "Done",
    "planId": "plan-id-1"
  }
]
```

## Using Plan IDs

```bash
# List buckets by plan ID
python planner.py list-buckets \
  --plan "12345678-1234-1234-1234-123456789abc"
```
