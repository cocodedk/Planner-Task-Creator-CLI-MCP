# 008-integration/003: Performance Testing & Optimization

## Goal
Verify performance meets requirements and optimize if needed.

## Performance Requirements (from PRD)

- Operation completion: < 3 seconds
- Extension memory: < 50MB
- MCP server startup: < 1 second
- No UI blocking operations

## Test Cases

### Operation Timing
- [ ] getPlans timing (baseline, empty, 10+ plans)
- [ ] getTasks timing (empty plan, 10 tasks, 50+ tasks)
- [ ] createTask timing
- [ ] updateTask timing
- [ ] deleteTask timing (without confirmation)
- [ ] Full workflow timing (create → update → delete)

### Resource Usage
- [ ] Extension memory usage (at rest)
- [ ] Extension memory usage (during operations)
- [ ] MCP server memory usage
- [ ] CPU usage during operations

### Concurrency
- [ ] Multiple operations in quick succession
- [ ] Multiple plans/tasks at once
- [ ] Concurrent AI agent requests

## Measurement Approach

1. **Add timing instrumentation**
   - Start/end timestamps for each operation
   - Log timing at each layer
   - Identify bottlenecks

2. **Collect metrics**
   - Run each operation 10 times
   - Calculate mean, median, p95, max
   - Identify outliers

3. **Profile bottlenecks**
   - Use Chrome DevTools for extension
   - Use Node.js profiler for MCP server
   - Identify slow operations

## Optimization Targets

If any operation exceeds 3 seconds:

1. **API call optimization**
   - Reduce request payload size
   - Parallel requests where possible
   - Connection keep-alive

2. **Parsing optimization**
   - Lazy parsing
   - Stream processing for large responses
   - Cache parsed results

3. **Transport optimization**
   - Message batching
   - Compression
   - Connection pooling

## Acceptance Criteria

- [ ] All operations complete in < 3 seconds (p95)
- [ ] Extension memory < 50MB
- [ ] Server startup < 1 second
- [ ] No UI blocking
- [ ] Performance documented
- [ ] **CRITICAL**: All files still under 200 lines

## Dependencies
- Completes after: 008-integration/002-error-scenarios

## Time Estimate
2-3 hours

## Notes
Don't optimize prematurely. Measure first, then optimize only bottlenecks.
