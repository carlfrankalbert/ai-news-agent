# Tests

## Expand Button Test

Tests the "vis alle" / "vis færre" button functionality.

### Running the Test

#### Option 1: Open in Browser
```bash
# Open the test file directly
open tests/test_expand_button.html
```

#### Option 2: Serve via HTTP Server
```bash
# Start a local server
cd tests
python3 -m http.server 8001

# Open in browser
open http://localhost:8001/test_expand_button.html
```

### What the Test Verifies

The test checks the expand button functionality according to requirements:

**Normal Case (more than 3 items):**
1. ✅ **Initial State**: Only first 3 items are visible, button is NOT expanded
2. ✅ **Initial Text**: Button shows "Vis alle (X)" where X is total number of hidden items
3. ✅ **Initial Rows**: Items beyond the first 3 are collapsed (hidden)
4. ✅ **Expand on Click**: Button becomes expanded when clicked
5. ✅ **Text on Expand**: Button text changes to "Vis færre" (Show less)
6. ✅ **Rows on Expand**: All remaining items become visible
7. ✅ **Collapse on Second Click**: Button is NOT expanded after second click
8. ✅ **Text on Collapse**: Button text changes back to "Vis alle (X)"
9. ✅ **Rows on Collapse**: Only first 3 items remain visible after collapse

**Edge Case (3 or fewer items):**
10. ✅ **Button Hidden**: Button should not be rendered/visible when list has 3 items
11. ✅ **No Hidden Rows**: No rows should be hidden when there are 3 or fewer items
12. ✅ **Button Hidden**: Button should not be rendered/visible when list has 2 items

### Test Results

The test will display:
- ✓ Green checkmarks for passed tests
- ✗ Red X marks for failed tests
- Summary with total tests, passed, failed, and success rate

### Expected Behavior

**Normal Case (6 items):**
- **Initial**: Only rows 1-3 visible, button shows "Vis alle (3)", rows 4-6 are hidden
- **After First Click**: Button shows "Vis færre", all rows (1-6) are visible
- **After Second Click**: Button shows "Vis alle (3)" again, only rows 1-3 visible, rows 4-6 hidden

**Edge Case (3 items):**
- **Initial**: All 3 rows visible, button is hidden (not rendered)

**Edge Case (2 items):**
- **Initial**: All 2 rows visible, button is hidden (not rendered)

