# Testing

## Step 1: Initialize Authentication

```bash
python planner.py init-auth
```

You should see:
```
Authentication Required
Please visit: https://microsoft.com/devicelogin
Enter code: ABCD1234
```

1. Open the URL in a browser
2. Enter the code shown
3. Complete the authentication flow
4. Return to your terminal

## Step 2: List Your Plans

```bash
python planner.py list-plans
```

You should see JSON output with your available plans.

## Step 3: Set Defaults

```bash
python planner.py set-defaults --plan "Your Plan Name" --bucket "Your Bucket Name"
```

## Step 4: Create a Test Task

```bash
python planner.py add --title "Test task from CLI"
```

You should see JSON output with the task ID and URL.
