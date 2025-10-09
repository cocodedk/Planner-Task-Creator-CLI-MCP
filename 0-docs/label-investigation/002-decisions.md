# Label Investigation - Decisions

## Current Implementation Decisions

### Label Input Format
**Decision**: Use "LabelN" CSV format (e.g., "Label1,Label3")
**Rationale**:
- Matches Microsoft Planner UI default naming
- Simple and predictable
- Maps directly to API categoryN format
- Works regardless of custom label renaming

### Parse Strategy
**Decision**: Case-insensitive, whitespace-tolerant, filter invalid
**Rationale**:
- User-friendly for typos
- Flexible input handling
- Fail gracefully vs. error on invalid input

### API Mapping
**Decision**: "LabelN" → "categoryN"
**Rationale**:
- Direct 1:1 mapping
- No ambiguity
- Minimal transformation logic

## Potential Enhancement Decisions

### Enhancement 1: Custom Label Names
**Status**: Deferred
**Reason**: Requires additional API calls, adds complexity, current solution works well

### Enhancement 2: Label Listing
**Status**: Recommended for future
**Reason**: Low complexity, high utility for users

### Enhancement 3: Label Validation
**Status**: Deferred
**Reason**: Adds overhead, current fail-silently approach is acceptable

### Enhancement 4: Numeric Shorthand
**Status**: Not recommended
**Reason**: Less explicit, ambiguous with custom names, minimal benefit
