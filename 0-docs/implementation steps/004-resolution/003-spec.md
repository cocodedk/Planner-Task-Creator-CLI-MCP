# Resolution Module Specification

**Functions**:
- `case_insensitive_match(items: List[dict], key: str, value: str) -> List[dict]`
- `list_user_plans(token: str) -> List[dict]`
- `list_plan_buckets(plan_id: str, token: str) -> List[dict]`
- `resolve_plan(token: str, plan: str) -> dict`
- `resolve_bucket(token: str, plan_id: str, bucket: str) -> dict`

**case_insensitive_match Implementation**:
- Filter list of dictionaries by case-insensitive key value match
- Return filtered list

**list_user_plans Implementation**:
1. GET `/me/planner/plans`
2. For each plan, if owner group ID exists, fetch group details to get displayName
3. Return plans list with optional groupName field

**list_plan_buckets Implementation**:
1. GET `/planner/plans/{planId}/buckets`
2. Return buckets list from response

**resolve_plan Implementation**:
1. If input matches GUID pattern, return `{"id": plan}`
2. Fetch user plans
3. Find exact case-insensitive matches by "title" field
4. If exactly 1 match, return it
5. If multiple matches, raise ValueError with Ambiguous error JSON
6. If no matches, raise ValueError with NotFound error JSON including all candidates

**resolve_bucket Implementation**:
1. If input matches GUID pattern, return `{"id": bucket}`
2. Fetch plan buckets
3. Find exact case-insensitive matches by "name" field
4. If exactly 1 match, return it
5. If multiple matches, raise ValueError with Ambiguous error JSON
6. If no matches, raise ValueError with NotFound error JSON including all candidates

**Error JSON Format**:
```json
{
  "code": "NotFound|Ambiguous",
  "message": "Human readable message",
  "candidates": [{"id": "...", "title|name": "...", ...}]
}
```
